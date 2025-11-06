# 🏨 Sistema de Reservas de Hotel - Testing Pack

Santiago

## Estrucutura

```
├── 📁 app
│   ├── 📁 static
│   │   └── 🎨 style.css
│   ├── 📁 templates
│   │   ├── 🌐 base.html
│   │   ├── 🌐 booking.html
│   │   ├── 🌐 index.html
│   │   ├── 🌐 login.html
│   │   ├── 🌐 register.html
│   │   └── 🌐 search_results.html
│   ├── 🐍 app.py
│   ├── 🐍 db.py
│   └── 🐍 init_db.py
├── 📁 docs
│   ├── 📝 IEEE829_Plan_Template.md
│   ├── 📄 Matriz_Riesgo_RPN.xlsx
│   ├── 📄 Matriz_Trazabilidad.xlsx
│   └── 📝 Plan_Pruebas_Hotel.md
├── 📁 metrics
│   ├── 📁 dashboards
│   │   ├── 🌐 dashboard_metricas.html
│   │   └── ⚙️ metricas_resumen.json
│   ├── 📁 figs
│   │   ├── 🖼️ semaforo.png
│   │   ├── 🖼️ severity.png
│   │   ├── 🖼️ status.png
│   │   └── 🖼️ trend.png
│   ├── 📄 dataset_defectos.csv
│   ├── 📄 dataset_defectos_backup.csv
│   ├── 🐍 mejorar_dataset.py
│   └── 🐍 sistema_metricas.py
├── 📁 tests
│   ├── ⚙️ pytest.ini
│   └── 🐍 test_app.py
├── 📝 README.md
├── 📄 hotel_reservas.db
├── 📄 requirements.txt
└── 📄 run_app.bat
```
---

## 🚀 Instalación

### 1. Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

### 2. Clonar o Descargar el Proyecto

```bash
cd c:\laragon\www\hotel_testing_pack
```

### 3. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**
```
Flask==2.3.0
Werkzeug==2.3.0
pytest==7.4.0
pytest-cov==4.1.0
pandas==2.0.0
numpy==1.24.0
matplotlib==3.7.0
```

### 5. Inicializar Base de Datos

```bash
python app/init_db.py
```

Debe ver el mensaje:
```
DB inicializada en: C:\laragon\www\hotel_testing_pack\hotel_reservas.db
Base de datos inicializada correctamente.
```

---

## 💻 Uso

### Ejecutar la Aplicación

```bash
# Método 1: Directamente con Python
python app/app.py

# Método 2: Con Flask CLI
set FLASK_APP=app/app.py
set FLASK_ENV=development
flask run

# Método 3: Usar el batch file (Windows)
run_app.bat
```

La aplicación estará disponible en: **http://localhost:5000**

### Flujo de Usuario

1. **Registrarse:** http://localhost:5000/register
2. **Iniciar Sesión:** http://localhost:5000/login
3. **Buscar Habitaciones:** En la página principal
4. **Hacer Reserva:** Seleccionar habitación disponible
5. **Pagar:** Confirmar pago simulado
6. **Cerrar Sesión:** Click en "Cerrar sesión"

---

## 📊 Sistema de Métricas

### Ejecutar el Sistema de Métricas

```bash
cd metrics
python sistema_metricas.py
```
## Sistema
### imagen 1 ingreso de habitacion 

<img width="1234" height="913" alt="image" src="https://github.com/user-attachments/assets/8aa2066f-8b35-4ab0-a21f-4da8ce213b3f" />

### imagen 2 Registro de habitacion 

<img width="1290" height="889" alt="image" src="https://github.com/user-attachments/assets/68d4d38e-6070-42c3-816e-0a914aad6081" />

### imagen 3 pago 

<img width="1241" height="602" alt="image" src="https://github.com/user-attachments/assets/1c470583-6fd0-4ebb-9a7e-1cdabf306543" />

### imagen 4 Pago 

<img width="1361" height="329" alt="image" src="https://github.com/user-attachments/assets/66c488c5-3f56-4c55-9702-6a5ed908ac5d" />

### imagen 5 Registro 

<img width="1269" height="815" alt="image" src="https://github.com/user-attachments/assets/d466059b-d9fe-4a50-a84d-805ab9d07867" />

### imagen 6 Inicio de sesion 

<img width="1246" height="814" alt="image" src="https://github.com/user-attachments/assets/c6e3339b-e48c-453e-b214-c910f3b01eb4" />


### Salida del Sistema del dashboard

<img width="851" height="733" alt="image" src="https://github.com/user-attachments/assets/d6ef8826-f3fb-438f-8568-31108bd7c399" />
<img width="808" height="531" alt="image" src="https://github.com/user-attachments/assets/d3fe7315-aae0-4718-9162-eba08b24ea3a" />
