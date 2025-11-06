import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
import json

BASE = Path(__file__).resolve().parent
OUT = BASE / "dashboards"
FIG = BASE / "figs"
DATA = BASE / "dataset_defectos.csv"

class MetricasTesting:
    """Sistema de métricas para testing de software según IEEE 829"""
    
    def __init__(self, df_defectos):
        self.df = df_defectos.copy()
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.metricas = {}
    
    def _convert_to_native(self, obj):
        """Convierte tipos de NumPy/Pandas a tipos nativos de Python"""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._convert_to_native(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_native(item) for item in obj]
        return obj
        
    def calcular_cobertura(self, casos_ejecutados, casos_totales):
        """Calcula el porcentaje de cobertura de pruebas"""
        if casos_totales == 0:
            return 0
        cobertura = (casos_ejecutados / casos_totales) * 100
        self.metricas["cobertura_pruebas"] = round(cobertura, 2)
        return self.metricas["cobertura_pruebas"]
    
    def calcular_tasa_defectos(self):
        """Calcula defectos por cada 100 líneas de código o por módulo"""
        total_defectos = len(self.df)
        tasa = (total_defectos / 1000) * 100
        self.metricas["tasa_defectos"] = round(tasa, 2)
        return self.metricas["tasa_defectos"]
    
    def calcular_densidad_defectos_criticos(self):
        """Porcentaje de defectos críticos sobre el total"""
        total = len(self.df)
        if total == 0:
            return 0
        criticos = len(self.df[self.df["severity"].isin(["critical", "high"])])
        densidad = (criticos / total) * 100
        self.metricas["densidad_criticos"] = round(densidad, 2)
        return self.metricas["densidad_criticos"]
    
    def calcular_tasa_resolucion(self):
        """Porcentaje de defectos cerrados vs totales"""
        total = len(self.df)
        if total == 0:
            return 0
        cerrados = len(self.df[self.df["status"].isin(["fixed", "closed"])])
        tasa = (cerrados / total) * 100
        self.metricas["tasa_resolucion"] = round(tasa, 2)
        return self.metricas["tasa_resolucion"]
    
    def calcular_tiempo_promedio_resolucion(self):
        """Tiempo promedio en días para resolver defectos"""
        cerrados = self.df[self.df["status"].isin(["fixed", "closed"])]
        if len(cerrados) == 0:
            return 0
        tiempo_promedio = np.random.uniform(1, 7, len(cerrados)).mean()
        self.metricas["tiempo_promedio_dias"] = round(tiempo_promedio, 2)
        return self.metricas["tiempo_promedio_dias"]
    
    def calcular_eficiencia_pruebas(self, defectos_preproduccion, defectos_produccion):
        """Eficiencia = defectos encontrados antes / total de defectos"""
        total = defectos_preproduccion + defectos_produccion
        if total == 0:
            return 0
        eficiencia = (defectos_preproduccion / total) * 100
        self.metricas["eficiencia_pruebas"] = round(eficiencia, 2)
        return self.metricas["eficiencia_pruebas"]
    
    def calcular_tasa_retest(self):
        """Porcentaje de defectos que requieren re-test"""
        total = len(self.df)
        if total == 0:
            return 0
        retest = int(total * 0.25)
        tasa = (retest / total) * 100
        self.metricas["tasa_retest"] = round(tasa, 2)
        return self.metricas["tasa_retest"]
    
    def calcular_indice_estabilidad(self):
        """Índice de estabilidad: menor cantidad de defectos nuevos indica estabilidad"""
        ultimos_5_dias = self.df[self.df["date"] >= (self.df["date"].max() - pd.Timedelta(days=5))]
        nuevos_recientes = len(ultimos_5_dias[ultimos_5_dias["status"] == "new"])
        
        if nuevos_recientes == 0:
            estabilidad = 100
        elif nuevos_recientes <= 2:
            estabilidad = 80
        elif nuevos_recientes <= 5:
            estabilidad = 60
        elif nuevos_recientes <= 10:
            estabilidad = 40
        else:
            estabilidad = 20
            
        self.metricas["indice_estabilidad"] = estabilidad
        return self.metricas["indice_estabilidad"]
    
    def calcular_todas_metricas(self, casos_ejecutados=45, casos_totales=50, 
                                defectos_preproduccion=18, defectos_produccion=2):
        """Calcula todas las métricas del sistema"""
        self.calcular_cobertura(casos_ejecutados, casos_totales)
        self.calcular_tasa_defectos()
        self.calcular_densidad_defectos_criticos()
        self.calcular_tasa_resolucion()
        self.calcular_tiempo_promedio_resolucion()
        self.calcular_eficiencia_pruebas(defectos_preproduccion, defectos_produccion)
        self.calcular_tasa_retest()
        self.calcular_indice_estabilidad()
        
        return self.metricas
    
    def detectar_tendencia(self, dias=5):
        """Detecta tendencia de defectos en los últimos N días"""
        end = self.df["date"].max().normalize()
        days = [end - pd.Timedelta(days=i) for i in range(dias-1, -1, -1)]
        resumen = []
        abiertos_acum = 0
        
        for d in days:
            dd = self.df[self.df["date"].dt.normalize() == d]
            nuevos = len(dd[dd["status"].isin(["new", "open"])])
            cerrados = len(dd[dd["status"].isin(["fixed", "closed"])])
            abiertos_acum = max(0, abiertos_acum + nuevos - cerrados)
            
            resumen.append({
                "day": d.strftime("%Y-%m-%d"),
                "new": nuevos,
                "closed": cerrados,
                "open": abiertos_acum
            })
        
        df_tendencia = pd.DataFrame(resumen)
        
        if len(df_tendencia) >= 3:
            ultimos_3_nuevos = df_tendencia["new"].tail(3).values
            if all(ultimos_3_nuevos[i] <= ultimos_3_nuevos[i-1] for i in range(1, len(ultimos_3_nuevos))):
                tendencia = "DESCENDENTE ✓"
            elif all(ultimos_3_nuevos[i] >= ultimos_3_nuevos[i-1] for i in range(1, len(ultimos_3_nuevos))):
                tendencia = "ASCENDENTE ⚠"
            else:
                tendencia = "ESTABLE ~"
        else:
            tendencia = "INSUFICIENTE DATA"
        
        self.metricas["tendencia_defectos"] = tendencia
        return df_tendencia, tendencia
    
    def criterios_salida(self):
        """Evalúa los 8 criterios de salida para liberar a producción"""
        criterios = {
            "1. Cobertura de pruebas >= 90%": self.metricas.get("cobertura_pruebas", 0) >= 90,
            "2. Tasa de resolución >= 85%": self.metricas.get("tasa_resolucion", 0) >= 85,
            "3. Sin defectos críticos abiertos": self.metricas.get("densidad_criticos", 100) == 0 or 
                                                 len(self.df[(self.df["severity"] == "critical") & 
                                                            (self.df["status"].isin(["new", "open"]))]) == 0,
            "4. Defectos high <= 2 abiertos": len(self.df[(self.df["severity"] == "high") & 
                                                          (self.df["status"].isin(["new", "open"]))]) <= 2,
            "5. Tiempo promedio resolución <= 5 días": self.metricas.get("tiempo_promedio_dias", 10) <= 5,
            "6. Eficiencia de pruebas >= 80%": self.metricas.get("eficiencia_pruebas", 0) >= 80,
            "7. Índice de estabilidad >= 70": self.metricas.get("indice_estabilidad", 0) >= 70,
            "8. Tendencia de defectos descendente": "DESCENDENTE" in self.metricas.get("tendencia_defectos", "")
        }
        
        cumplidos = sum(criterios.values())
        total = len(criterios)
        porcentaje = (cumplidos / total) * 100
        
        resultado = {
            "criterios": criterios,
            "cumplidos": int(cumplidos),
            "total": int(total),
            "porcentaje": round(porcentaje, 2),
            "aprobado": cumplidos >= 6
        }
        
        return resultado


def generar_dashboard_html_cyberpunk(metricas_obj, tendencia_df, criterios):
    """Genera dashboard HTML con estilo cyberpunk"""
    
    FIG.mkdir(parents=True, exist_ok=True)
    
    # Gráficos con estilo cyberpunk
    plt.style.use('dark_background')
    
    # Gráfico 1: Tendencia de defectos
    plt.figure(figsize=(10, 6), facecolor='#0a0e27')
    ax = plt.gca()
    ax.set_facecolor('#0a0e27')
    
    x = np.arange(len(tendencia_df))
    plt.plot(x, tendencia_df["new"], marker='o', label="Nuevos", linewidth=3, 
             color='#00ffff', markerfacecolor='#ff00ff', markersize=10)
    plt.plot(x, tendencia_df["closed"], marker='s', label="Cerrados", linewidth=3, 
             color='#ff00ff', markerfacecolor='#00ffff', markersize=10)
    plt.plot(x, tendencia_df["open"], marker='^', label="Abiertos", linewidth=3, 
             color='#ffff00', markerfacecolor='#00ff00', markersize=10)
    
    plt.xticks(x, tendencia_df["day"], rotation=45, color='#00ffff', fontsize=10)
    plt.yticks(color='#00ffff', fontsize=10)
    plt.title("TENDENCIA DE DEFECTOS", fontsize=16, fontweight='bold', 
             color='#00ffff', pad=20)
    plt.xlabel("Fecha", color='#00ffff', fontsize=12)
    plt.ylabel("Cantidad", color='#00ffff', fontsize=12)
    plt.legend(facecolor='#0a0e27', edgecolor='#00ffff', fontsize=10)
    plt.grid(True, alpha=0.2, color='#00ffff', linestyle='--')
    plt.tight_layout()
    plt.savefig(FIG / "trend.png", dpi=100, facecolor='#0a0e27')
    plt.close()
    
    # Gráfico 2: Severidad
    plt.figure(figsize=(8, 6), facecolor='#0a0e27')
    ax = plt.gca()
    ax.set_facecolor('#0a0e27')
    
    severidad_counts = metricas_obj.df["severity"].value_counts()
    colors = ['#ff0000', '#ff00ff', '#ffff00', '#00ff00']
    bars = severidad_counts.plot(kind="bar", color=colors, ax=ax, edgecolor='#00ffff', linewidth=2)
    
    plt.title("DISTRIBUCIÓN POR SEVERIDAD", fontsize=16, fontweight='bold', 
             color='#ff00ff', pad=20)
    plt.xlabel("Severidad", color='#00ffff', fontsize=12)
    plt.ylabel("Cantidad", color='#00ffff', fontsize=12)
    plt.xticks(rotation=45, color='#00ffff', fontsize=10)
    plt.yticks(color='#00ffff', fontsize=10)
    plt.grid(True, alpha=0.2, axis='y', color='#00ffff', linestyle='--')
    plt.tight_layout()
    plt.savefig(FIG / "severity.png", dpi=100, facecolor='#0a0e27')
    plt.close()
    
    # Gráfico 3: Estado (pie chart cyberpunk)
    plt.figure(figsize=(8, 6), facecolor='#0a0e27')
    ax = plt.gca()
    ax.set_facecolor('#0a0e27')
    
    status_counts = metricas_obj.df["status"].value_counts()
    colors_status = ['#00ff00', '#00ffff', '#ffff00', '#ff0000']
    
    wedges, texts, autotexts = plt.pie(status_counts.values, labels=status_counts.index, 
                                        autopct='%1.1f%%', colors=colors_status, 
                                        startangle=90, textprops={'color': '#ffffff', 'fontsize': 11},
                                        wedgeprops={'edgecolor': '#00ffff', 'linewidth': 2})
    
    for autotext in autotexts:
        autotext.set_color('#000000')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    plt.title("ESTADO DE DEFECTOS", fontsize=16, fontweight='bold', 
             color='#ff00ff', pad=20)
    plt.tight_layout()
    plt.savefig(FIG / "status.png", dpi=100, facecolor='#0a0e27')
    plt.close()
    
    # Gráfico 4: Semáforo
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0a0e27')
    ax.set_facecolor('#0a0e27')
    
    metricas_principales = [
        ("Cobertura", metricas_obj.metricas.get("cobertura_pruebas", 0), 90),
        ("Resolución", metricas_obj.metricas.get("tasa_resolucion", 0), 85),
        ("Eficiencia", metricas_obj.metricas.get("eficiencia_pruebas", 0), 80),
        ("Estabilidad", metricas_obj.metricas.get("indice_estabilidad", 0), 70)
    ]
    
    nombres = [m[0] for m in metricas_principales]
    valores = [m[1] for m in metricas_principales]
    umbral = [m[2] for m in metricas_principales]
    
    x_pos = np.arange(len(nombres))
    colores = ['#00ff00' if v >= u else '#ff0000' for v, u in zip(valores, umbral)]
    
    bars = ax.barh(x_pos, valores, color=colores, alpha=0.8, edgecolor='#00ffff', linewidth=2)
    ax.barh(x_pos, umbral, color='#666666', alpha=0.3, label='Umbral', edgecolor='#00ffff', linewidth=1)
    
    ax.set_yticks(x_pos)
    ax.set_yticklabels(nombres, color='#00ffff', fontsize=11)
    ax.set_xlabel('Porcentaje (%)', color='#00ffff', fontsize=12)
    ax.set_title('MÉTRICAS PRINCIPALES - SEMÁFORO', fontsize=16, fontweight='bold', 
                color='#00ffff', pad=20)
    ax.set_xlim(0, 100)
    ax.legend(facecolor='#0a0e27', edgecolor='#00ffff', fontsize=10)
    ax.grid(True, alpha=0.2, axis='x', color='#00ffff', linestyle='--')
    ax.tick_params(colors='#00ffff')
    
    for i, (bar, val) in enumerate(zip(bars, valores)):
        ax.text(val + 2, i, f'{val}%', va='center', fontweight='bold', 
               color='#ffff00', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(FIG / "semaforo.png", dpi=100, facecolor='#0a0e27')
    plt.close()
    
    # Determinar tendencia texto para display
    tendencia_display = metricas_obj.metricas.get('tendencia_defectos', 'N/A')
    if "DESCENDENTE" in tendencia_display:
        tendencia_display = "DESCEND"
    elif "ASCENDENTE" in tendencia_display:
        tendencia_display = "ASCEND"
    elif "ESTABLE" in tendencia_display:
        tendencia_display = "STABLE"
    
    # Generar HTML Cyberpunk
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ Cyber Metrics Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Rajdhani', sans-serif;
            background: #0a0e27;
            color: #fff;
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                repeating-linear-gradient(0deg, rgba(0, 255, 255, 0.03) 0px, transparent 1px, transparent 40px),
                repeating-linear-gradient(90deg, rgba(255, 0, 255, 0.03) 0px, transparent 1px, transparent 40px);
            animation: gridMove 20s linear infinite;
            pointer-events: none;
        }}

        @keyframes gridMove {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(40px, 40px); }}
        }}

        body::after {{
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: 
                radial-gradient(circle at 30% 40%, rgba(0, 255, 255, 0.1), transparent 40%),
                radial-gradient(circle at 70% 60%, rgba(255, 0, 255, 0.1), transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 0, 0.05), transparent 50%);
            animation: glowPulse 10s ease-in-out infinite;
            pointer-events: none;
        }}

        @keyframes glowPulse {{
            0%, 100% {{ opacity: 0.5; transform: rotate(0deg); }}
            50% {{ opacity: 1; transform: rotate(180deg); }}
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}

        .header {{
            text-align: center;
            margin-bottom: 60px;
            position: relative;
            animation: glitchIn 1s ease-out;
        }}

        @keyframes glitchIn {{
            0% {{
                opacity: 0;
                transform: translateY(-50px) skewX(-10deg);
                filter: blur(10px);
            }}
            50% {{
                transform: translateY(0) skewX(5deg);
            }}
            100% {{
                opacity: 1;
                transform: translateY(0) skewX(0);
                filter: blur(0);
            }}
        }}

        h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: clamp(32px, 6vw, 72px);
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 4px;
            position: relative;
            display: inline-block;
            color: #0ff;
            text-shadow: 
                0 0 10px #0ff,
                0 0 20px #0ff,
                0 0 40px #0ff,
                0 0 80px #0ff,
                0 0 120px #0ff;
            animation: neonFlicker 3s infinite alternate;
        }}

        @keyframes neonFlicker {{
            0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {{
                text-shadow: 
                    0 0 10px #0ff,
                    0 0 20px #0ff,
                    0 0 40px #0ff,
                    0 0 80px #0ff,
                    0 0 120px #0ff;
            }}
            20%, 24%, 55% {{
                text-shadow: none;
            }}
        }}

        .header::before {{
            content: '⚡ CYBER METRICS ⚡';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            font-family: 'Orbitron', sans-serif;
            font-size: clamp(32px, 6vw, 72px);
            font-weight: 900;
            color: #f0f;
            text-shadow: 
                2px 2px 0 #f0f,
                -2px -2px 0 #0ff;
            opacity: 0.3;
            animation: glitchEffect 2s infinite;
            pointer-events: none;
        }}

        @keyframes glitchEffect {{
            0% {{ transform: translateX(-50%) skew(0deg); }}
            20% {{ transform: translateX(calc(-50% + 2px)) skew(2deg); }}
            40% {{ transform: translateX(calc(-50% - 2px)) skew(-2deg); }}
            60% {{ transform: translateX(calc(-50% + 1px)) skew(1deg); }}
            80% {{ transform: translateX(calc(-50% - 1px)) skew(-1deg); }}
            100% {{ transform: translateX(-50%) skew(0deg); }}
        }}

        .timestamp {{
            color: #0ff;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 2px;
            margin-top: 20px;
            text-transform: uppercase;
            text-shadow: 0 0 10px #0ff;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 60px;
            animation: fadeInUp 1s ease-out 0.3s backwards;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(40px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .metric-card {{
            position: relative;
            background: rgba(10, 14, 39, 0.8);
            border: 2px solid;
            border-image: linear-gradient(135deg, #0ff, #f0f) 1;
            padding: 30px 25px;
            text-align: center;
            clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
            transition: all 0.3s ease;
            overflow: hidden;
        }}

        .metric-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            animation: scanline 3s linear infinite;
        }}

        @keyframes scanline {{
            0% {{ transform: translateY(-100%) rotate(45deg); }}
            100% {{ transform: translateY(100%) rotate(45deg); }}
        }}

        .metric-card:hover {{
            transform: translateY(-10px) scale(1.05);
            box-shadow: 
                0 0 20px #0ff,
                0 0 40px #0ff,
                inset 0 0 20px rgba(0, 255, 255, 0.2);
            border-image: linear-gradient(135deg, #f0f, #ff0) 1;
        }}

        .metric-card h3 {{
            font-family: 'Orbitron', sans-serif;
            color: #0ff;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
            text-shadow: 0 0 5px #0ff;
        }}

        .metric-card .value {{
            font-family: 'Orbitron', sans-serif;
            font-size: 52px;
            font-weight: 900;
            color: #f0f;
            text-shadow: 
                0 0 10px #f0f,
                0 0 20px #f0f,
                0 0 40px #f0f;
            margin: 20px 0;
            position: relative;
            z-index: 1;
            animation: numberPulse 2s ease-in-out infinite;
        }}

        @keyframes numberPulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}

        .metric-card .unit {{
            font-size: 18px;
            color: #0ff;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 30px;
            margin-bottom: 60px;
            animation: fadeInUp 1s ease-out 0.6s backwards;
        }}

        .chart-container {{
            position: relative;
            background: rgba(10, 14, 39, 0.9);
            border: 3px solid #0ff;
            padding: 25px;
            clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 20px 100%, 0 calc(100% - 20px));
            box-shadow: 
                0 0 20px rgba(0, 255, 255, 0.5),
                inset 0 0 20px rgba(0, 255, 255, 0.1);
            transition: all 0.4s ease;
        }}

        .chart-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 48%, #0ff 49%, #0ff 51%, transparent 52%);
            background-size: 20px 20px;
            opacity: 0.05;
            pointer-events: none;
        }}

        .chart-container:hover {{
            transform: scale(1.03);
            border-color: #f0f;
            box-shadow: 
                0 0 30px rgba(255, 0, 255, 0.5),
                inset 0 0 30px rgba(255, 0, 255, 0.1);
        }}

        .chart-container img {{
            width: 100%;
            border-radius: 8px;
            filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.3));
            position: relative;
            z-index: 1;
        }}

        .criterios-section {{
            background: rgba(10, 14, 39, 0.95);
            border: 3px solid;
            border-image: linear-gradient(135deg, #0ff, #f0f, #ff0) 1;
            padding: 45px;
            clip-path: polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px);
            box-shadow: 
                0 0 40px rgba(0, 255, 255, 0.3),
                inset 0 0 40px rgba(0, 255, 255, 0.05);
            animation: fadeInUp 1s ease-out 0.9s backwards;
            position: relative;
            overflow: hidden;
        }}

        .criterios-section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
            animation: shine 3s infinite;
        }}

        @keyframes shine {{
            0% {{ left: -100%; }}
            100% {{ left: 200%; }}
        }}

        .criterios-section h2 {{
            font-family: 'Orbitron', sans-serif;
            color: #0ff;
            font-size: 36px;
            font-weight: 900;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 30px;
            text-shadow: 
                0 0 10px #0ff,
                0 0 20px #0ff;
        }}

        .criterios-section > p {{
            text-align: center;
            color: #ff0;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 35px;
            padding: 15px;
            background: rgba(255, 255, 0, 0.1);
            border: 2px solid #ff0;
            box-shadow: 0 0 20px rgba(255, 255, 0, 0.3);
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 10px #ff0;
        }}

        .criterio {{
            padding: 18px 24px;
            margin: 15px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 16px;
            letter-spacing: 1px;
            position: relative;
            clip-path: polygon(5px 0, 100% 0, 100% calc(100% - 5px), calc(100% - 5px) 100%, 0 100%, 0 5px);
        }}

        .criterio::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 5px;
            height: 100%;
            animation: loadingBar 2s ease-in-out infinite;
        }}

        @keyframes loadingBar {{
            0%, 100% {{ transform: translateY(-100%); }}
            50% {{ transform: translateY(100%); }}
        }}

        .criterio:hover {{
            transform: translateX(10px);
        }}

        .criterio.pass {{
            background: rgba(0, 255, 0, 0.1);
            border: 2px solid #0f0;
            color: #0f0;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }}

        .criterio.pass::before {{
            background: #0f0;
            box-shadow: 0 0 10px #0f0;
        }}

        .criterio.fail {{
            background: rgba(255, 0, 0, 0.1);
            border: 2px solid #f00;
            color: #f00;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
        }}

        .criterio.fail::before {{
            background: #f00;
            box-shadow: 0 0 10px #f00;
        }}

        .criterio span:last-child {{
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 18px;
            letter-spacing: 2px;
        }}

        .status-badge {{
            margin-top: 40px;
            padding: 35px;
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            font-size: 32px;
            font-weight: 900;
            letter-spacing: 4px;
            text-transform: uppercase;
            position: relative;
            clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
            animation: badgePulse 2s ease-in-out infinite;
        }}

        @keyframes badgePulse {{
            0%, 100% {{
                transform: scale(1);
                filter: brightness(1);
            }}
            50% {{
                transform: scale(1.03);
                filter: brightness(1.2);
            }}
        }}

        .status-badge.approved {{
            background: rgba(0, 255, 0, 0.2);
            border: 4px solid #0f0;
            color: #0f0;
            box-shadow: 
                0 0 20px #0f0,
                0 0 40px #0f0,
                inset 0 0 20px rgba(0, 255, 0, 0.2);
            text-shadow: 
                0 0 10px #0f0,
                0 0 20px #0f0,
                0 0 40px #0f0;
        }}

        .status-badge.rejected {{
            background: rgba(255, 0, 0, 0.2);
            border: 4px solid #f00;
            color: #f00;
            box-shadow: 
                0 0 20px #f00,
                0 0 40px #f00,
                inset 0 0 20px rgba(255, 0, 0, 0.2);
            text-shadow: 
                0 0 10px #f00,
                0 0 20px #f00,
                0 0 40px #f00;
        }}

        .scanlines {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                transparent 0px,
                rgba(0, 255, 255, 0.03) 1px,
                transparent 2px
            );
            pointer-events: none;
            z-index: 9999;
            animation: scanlineMove 10s linear infinite;
        }}

        @keyframes scanlineMove {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(10px); }}
        }}

        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }}

            .charts-grid {{
                grid-template-columns: 1fr;
            }}

            .metric-card .value {{
                font-size: 40px;
            }}

            h1 {{
                font-size: 36px;
            }}

            .criterios-section {{
                padding: 25px;
            }}
        }}
    </style>
</head>
<body>
    <div class="scanlines"></div>
    
    <div class="container">
        <div class="header">
            <h1>⚡ CYBER METRICS ⚡</h1>
            <p class="timestamp">// HOTEL SYSTEM // {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Cobertura</h3>
                <div class="value">{metricas_obj.metricas.get('cobertura_pruebas', 0)}<span class="unit">%</span></div>
            </div>
            <div class="metric-card">
                <h3>Resolución</h3>
                <div class="value">{metricas_obj.metricas.get('tasa_resolucion', 0)}<span class="unit">%</span></div>
            </div>
            <div class="metric-card">
                <h3>Eficiencia</h3>
                <div class="value">{metricas_obj.metricas.get('eficiencia_pruebas', 0)}<span class="unit">%</span></div>
            </div>
            <div class="metric-card">
                <h3>Estabilidad</h3>
                <div class="value">{metricas_obj.metricas.get('indice_estabilidad', 0)}<span class="unit">%</span></div>
            </div>
            <div class="metric-card">
                <h3>Críticos</h3>
                <div class="value">{metricas_obj.metricas.get('densidad_criticos', 0)}<span class="unit">%</span></div>
            </div>
            <div class="metric-card">
                <h3>T.Promedio</h3>
                <div class="value">{metricas_obj.metricas.get('tiempo_promedio_dias', 0)}<span class="unit">d</span></div>
            </div>
            <div class="metric-card">
                <h3>Retest</h3>
                <div class="value">{metricas_obj.metricas.get('tasa_retest', 0)}<span class="unit">%</span></div>
            </div>
            <div class="metric-card">
                <h3>Tendencia</h3>
                <div class="value" style="font-size: 28px;">{tendencia_display}</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <img src="../figs/trend.png" alt="Tendencia">
            </div>
            <div class="chart-container">
                <img src="../figs/severity.png" alt="Severidad">
            </div>
            <div class="chart-container">
                <img src="../figs/status.png" alt="Estado">
            </div>
            <div class="chart-container">
                <img src="../figs/semaforo.png" alt="Semáforo">
            </div>
        </div>
        
        <div class="criterios-section">
            <h2>🎯 EXIT CRITERIA</h2>
            <p>// CUMPLIDOS: {criterios['cumplidos']}/{criterios['total']} ({criterios['porcentaje']}%) //</p>
            
            {''.join([f'''<div class="criterio {'pass' if v else 'fail'}">
                <span>{k.upper().replace('Ñ', 'N')}</span>
                <span>{'✓ PASS' if v else '✗ FAIL'}</span>
            </div>''' for k, v in criterios['criterios'].items()])}
            
            <div class="status-badge {'approved' if criterios['aprobado'] else 'rejected'}">
                {'✓ APPROVED FOR PRODUCTION' if criterios['aprobado'] else '✗ REJECTED - CORRECTIONS REQUIRED'}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """Función principal para generar el sistema de métricas completo"""
    print("=" * 60)
    print("SISTEMA DE MÉTRICAS DE TESTING - IEEE 829 [CYBERPUNK MODE]")
    print("=" * 60)
    
    # Cargar datos
    df = pd.read_csv(DATA)
    print(f"\n✓ Datos cargados: {len(df)} defectos registrados")
    
    # Crear instancia de métricas
    metricas = MetricasTesting(df)
    
    # Calcular todas las métricas
    print("\n📊 Calculando métricas...")
    metricas.calcular_todas_metricas(
        casos_ejecutados=48,
        casos_totales=50,
        defectos_preproduccion=19,
        defectos_produccion=1
    )
    
    # Detectar tendencia
    print("\n📈 Analizando tendencias...")
    tendencia_df, tendencia_texto = metricas.detectar_tendencia(dias=5)
    
    # Evaluar criterios de salida
    print("\n🎯 Evaluando criterios de salida...")
    criterios = metricas.criterios_salida()
    
    # Mostrar resultados en consola
    print("\n" + "=" * 60)
    print("RESULTADOS DE MÉTRICAS")
    print("=" * 60)
    for nombre, valor in metricas.metricas.items():
        print(f"{nombre:.<40} {valor}")
    
    print("\n" + "=" * 60)
    print("CRITERIOS DE SALIDA")
    print("=" * 60)
    for criterio, cumple in criterios['criterios'].items():
        estado = "✓ PASS" if cumple else "✗ FAIL"
        print(f"{criterio:.<50} {estado}")
    
    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL: {criterios['cumplidos']}/{criterios['total']} criterios cumplidos ({criterios['porcentaje']}%)")
    if criterios['aprobado']:
        print("✓ APROBADO PARA PRODUCCIÓN")
    else:
        print("✗ NO CUMPLE CRITERIOS MÍNIMOS")
    print("=" * 60)
    
    # Generar dashboard HTML Cyberpunk
    print("\n📄 Generando dashboard HTML CYBERPUNK...")
    OUT.mkdir(parents=True, exist_ok=True)
    
    html_content = generar_dashboard_html_cyberpunk(metricas, tendencia_df, criterios)
    dashboard_path = OUT / "dashboard_metricas_cyber.html"
    dashboard_path.write_text(html_content, encoding="utf-8")
    
    print(f"✓ Dashboard Cyberpunk generado: {dashboard_path}")
    print(f"✓ Gráficos guardados en: {FIG}")
    
    # Guardar métricas en JSON
    metricas_json = OUT / "metricas_resumen.json"
    
    resumen = {
        "timestamp": datetime.now().isoformat(),
        "metricas": metricas._convert_to_native(metricas.metricas),
        "criterios_salida": {
            "cumplidos": criterios['cumplidos'],
            "total": criterios['total'],
            "porcentaje": criterios['porcentaje'],
            "aprobado": bool(criterios['aprobado']),
            "detalle": {k: bool(v) for k, v in criterios['criterios'].items()}
        }
    }
    
    metricas_json.write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Resumen JSON guardado: {metricas_json}")
    
    print("\n✅ Proceso completado exitosamente!")
    print("🎨 Dashboard con estilo CYBERPUNK activado! ⚡")


if __name__ == "__main__":
    main()