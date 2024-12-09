# To-Do List App with Flask

**To-Do List App** es una aplicación web desarrollada en Flask que permite a los usuarios gestionar sus tareas diarias de manera sencilla. Ofrece funcionalidades como registro de usuarios, asignación de prioridades y adjuntar imágenes a las tareas.

## 🚀 Características

- **Autenticación de usuarios**: registro e inicio de sesión tanto por la app como por OAuth.
- **Gestión de tareas**:
  - Crear, editar y eliminar tareas.
  - Asignar prioridades: `low`, `medium`, `high`, `urgent`.
  - Adjuntar imágenes a las tareas.
- **Implementacion de CheapShark**: muestra descuentos de juegos con calificaciones excelentes en el tablero.
  
---

## 🛠️ Instalación y Configuración

### Prerrequisitos

- **Python** 3.8 o superior.
- **Git** instalado en tu sistema.
- Un entorno virtual para gestionar dependencias.

### Pasos de instalación

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/GariboGE/to_do_list_gariboge.git
   cd to_do_list_gariboge

2. **Crea y activa un entorno virtual**:

   - En **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - En **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```


4. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt

5. **Incia la aplicacion**:
   ```bash
   flask run

La aplicación estará disponible en http://127.0.0.1:5000.


## 🧪 Pruebas
- Asegúrate de que las dependencias estén instaladas y que el entorno virtual esté activo.
- Ejecuta las pruebas con:
   ```bash
   pytest
- Esto te generara un reporte HTML y en consola con la cobertura del proyecto
