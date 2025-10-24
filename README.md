# 🎰 Proyecto Ruleta Casino

Este documento contiene todas las instrucciones necesarias para instalar, configurar y ejecutar el proyecto de la ruleta.

## 📂 Estructura del Proyecto

El proyecto está organizado en dos directorios principales:

```
proyecto_ruleta/
├── ruleta_server/     # Contiene el servidor web de la ruleta
│   ├── database.py
│   ├── ruleta.py
│   └── requirements.txt
├── management/        # Contiene los scripts para la gestión de usuarios
│   ├── manage.py
│   └── menu.sh
└── venv/              # Entorno virtual de Python
```

## ⚙️ Instalación

Sigue estos pasos para poner en marcha el proyecto.

### 1. Clonar o Descargar el Proyecto

Asegúrate de tener todos los archivos del proyecto en tu sistema local.

### 2. Crear y Activar el Entorno Virtual

Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.

```bash
# Navega a la raíz del proyecto
cd proyecto_ruleta

# Crea el entorno virtual (si no existe)
python3 -m venv venv

# Activa el entorno virtual
source venv/bin/activate
```
**Nota:** Cada vez que abras una nueva terminal para trabajar en el proyecto, deberás activar el entorno virtual con `source venv/bin/activate`.

### 3. Instalar Dependencias

Con el entorno virtual activado, instala las librerías de Python necesarias.

```bash
# Instala las dependencias desde ruleta_server
pip install -r ruleta_server/requirements.txt
```

### 4. Dar Permisos de Ejecución

Asegúrate de que los scripts de gestión sean ejecutables.

```bash
# Navega al directorio de gestión
cd management

# Da permisos de ejecución
chmod +x manage.py menu.sh

# Vuelve a la raíz del proyecto
cd ..
```

## ▶️ Cómo Ejecutar la Aplicación

La aplicación consta de dos partes: el servidor de la ruleta y el sistema de gestión. Debes ejecutarlos en **dos terminales separadas**.

### Terminal 1: Iniciar el Servidor de la Ruleta

Esta terminal mantendrá el servidor web funcionando.

```bash
# 1. Activa el entorno virtual (si no lo has hecho)
source venv/bin/activate

# 2. Navega al directorio del servidor
cd ruleta_server

# 3. Inicia el servidor
python ruleta.py
```

Verás un mensaje indicando que el servidor está en marcha. Puedes acceder a la ruleta abriendo tu navegador web y visitando:
**http://localhost:5678**

### Terminal 2: Usar el Sistema de Gestión

Esta terminal te permitirá administrar los usuarios y sus saldos.

```bash
# 1. Activa el entorno virtual (si no lo has hecho)
source venv/bin/activate

# 2. Navega al directorio de gestión
cd management

# 3. Ejecuta el menú interactivo
./menu.sh
```

Aparecerá un menú interactivo para crear, listar y modificar usuarios.

## 🛠️ Comandos de Gestión (Uso Avanzado)

También puedes usar `manage.py` directamente desde la línea de comandos sin el menú interactivo.

Asegúrate de estar en el directorio `management` y de que el entorno virtual esté activado.

*   **Crear un usuario:**
    ```bash
    python manage.py crear <nombre> <saldo>
    # Ejemplo: python manage.py crear User1 500
    ```

*   **Consultar saldo:**
    ```bash
    python manage.py saldo <nombre>
    # Ejemplo: python manage.py saldo User1
    ```

*   **Acreditar saldo:**
    ```bash
    python manage.py acreditar <nombre> <monto>
    # Ejemplo: python manage.py acreditar User1 150
    ```

*   **Listar todos los usuarios:**
    ```bash
    python manage.py listar
    ```
