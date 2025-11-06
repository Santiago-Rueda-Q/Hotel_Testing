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
### Sistema
** imagen 1 ingreso de habitacion **

<img width="942" height="536" alt="image" src="https://github.com/user-attachments/assets/4fb4c839-0168-4ae8-9725-eb8787783158" />

** imagen 2 Registro de habitacion **

<img width="885" height="474" alt="image" src="https://github.com/user-attachments/assets/a9c8256a-749d-42da-9ac3-c292a92d15a1" />

** imagen 3 pago **

<img width="913" height="248" alt="image" src="https://github.com/user-attachments/assets/e476aa64-cbad-4d29-ac29-376359d6202a" />

** imagen 4 Pago **

<img width="882" height="239" alt="image" src="https://github.com/user-attachments/assets/364b38d1-f147-4e63-94b0-9ff2f0cbe608" />

** imagen 5 Registro **

<img width="859" height="394" alt="image" src="https://github.com/user-attachments/assets/9d514faf-eeab-46a1-9645-8e638afadffc" />

** imagen 6 Inicio de sesion **

<img width="866" height="397" alt="image" src="https://github.com/user-attachments/assets/693d3324-4f79-4b7c-93ac-c2a7659fa010" />


### Salida del Sistema del dashboard

<img width="1212" height="903" alt="image" src="https://github.com/user-attachments/assets/325b1b60-f0ea-4ca7-9643-b0a1802c4c69" />
<img width="1158" height="521" alt="image" src="https://github.com/user-attachments/assets/21ae526b-e0a2-465e-be80-1b87e45bb8c6" />
