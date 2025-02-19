
# Proyecto Yasuni

Este es un sistema de gestión para la Reserva Ecológica Yasuni, desarrollado con **Django**. La aplicación está diseñada para administrar la información relacionada con las nacionalidades y categorías que habitan en la reserva, permitiendo a los administradores realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) de manera eficiente. 

El proyecto sigue las mejores prácticas de desarrollo web, utilizando vistas protegidas con autenticación, una arquitectura modular y una interfaz de usuario sencilla pero funcional.

## Funcionalidades Principales

- **Gestión de Nacionalidades:** Los administradores pueden agregar, editar y eliminar registros de nacionalidades que habitan la reserva. Además, pueden visualizar estadísticas detalladas de visualización de tiempo por cada nacionalidad.
  
- **Gestión de Categorías:** Los usuarios también pueden gestionar las categorías a las que pertenecen las nacionalidades, asegurando que la información esté organizada adecuadamente.

- **Análisis de Visualización:** La aplicación incluye reportes de análisis que muestran el tiempo de visualización acumulado por cada nacionalidad y categoría, permitiendo obtener información detallada sobre la relevancia y el interés en las distintas culturas de la reserva.

- **Sistema de Autenticación:** La plataforma incluye un sistema de login y logout, utilizando las vistas genéricas de Django para la autenticación de usuarios, asegurando que solo los administradores autorizados puedan acceder a ciertas funcionalidades.

- **Interfaz Web Amigable:** Utiliza plantillas HTML con CSS personalizadas, proporcionando una experiencia de usuario clara y directa para navegar y gestionar la información.

- **Arquitectura Modular:** El proyecto está organizado de manera modular, separando la lógica de negocio, las operaciones CRUD, y las plantillas de interfaz, siguiendo las mejores prácticas de Django.

## Público Objetivo

Este sistema está dirigido a los administradores de la Reserva Ecológica Yasuni, permitiendo:

- Centralizar y gestionar la información cultural de las nacionalidades y categorías.
- Facilitar la preservación de las diferentes culturas presentes en la reserva.
- Proveer datos valiosos para investigación y documentación sobre la diversidad cultural de la región.
- Ofrecer una interfaz administrativa para la gestión de actividades turísticas relacionadas con la reserva.

## Casos de Uso

- **Administración de la Reserva:** Gestión de la información de las nacionalidades y categorías de forma centralizada.
- **Análisis de Datos:** Proporciona un análisis de visualización de las nacionalidades más vistas o consultadas.
- **Investigación y Documentación:** Datos culturales y estadísticas que pueden ser utilizados por investigadores y gestores del parque.

## Estructura del Proyecto

```plaintext
Yasuni/
├── Nacionalidades/
│   ├── migrations/
│   ├── templates/
│   │   ├── gestionarNacionalidad.html
│   │   └── detalleNacionalidad.html
│   └── models.py
│
├── Turisticas/
│   ├── migrations/
│   ├── templates/
│   │   ├── gestionarTurismo.html
│   │   └── detalleTurismo.html
│   └── models.py
│
├── static/
│   ├── images/
│   ├── js/
│   └── styles/
│       ├── actividades.css
│       └── login.css
│
├── templates/
│   ├── registration/
│   │   ├── login.html
│   │   └── logged_out.html
│   ├── base.html
│   └── paginaActividades.html
│
├── webapp/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── Yasuni/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
└── requirements.txt
```

## Instalación

Para ejecutar el proyecto localmente, sigue estos pasos:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/yasuni-proyecto.git
cd yasuni-proyecto
```

### 2. Crear y Activar un Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar las Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
- Configura la conexión a la base de datos en `settings.py`.
  
- Ejecuta las migraciones para configurar las tablas de la base de datos:
```bash
python manage.py migrate
```

### 5. Ejecutar el Servidor de Desarrollo
```bash
python manage.py runserver
```

Accede al servidor en `http://127.0.0.1:8000/` y verifica que la aplicación funcione correctamente.

## Funcionalidades

- **Autenticación de Usuarios:** Los usuarios deben iniciar sesión para acceder a las páginas protegidas como la gestión de nacionalidades o el análisis de datos.
  
- **Operaciones CRUD:** Completa gestión para agregar, editar, y eliminar nacionalidades y categorías.
  
- **Análisis de Visualización:** Proporciona informes y estadísticas sobre el tiempo de visualización de diferentes elementos culturales y turísticos.

- **Interfaz de Usuario Amigable:** Con una interfaz basada en **BOOTSTRAP**, el diseño es moderno y responsivo.

## Anexos

| **Pantalla de Inicio**                         | **Pantalla de Quienes Somos**                  |
|------------------------------------------------|------------------------------------------------|
| <img src="imagenes_proyecto/SECCION_INICIO1.png" alt="Pantalla de Inicio" style="max-width: 300px; height: auto;"> | <img src="imagenes_proyecto/SECCION_QUIENES_SOMOS1.png" alt="Pantalla de Quienes Somos" style="max-width: 300px; height: auto;"> |

| **Más Información**                            | **Ingresar**                                                                                                            |
|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| <img src="imagenes_proyecto/SECCION_MAS_INFORMACION1.png" alt="Más Información" style="max-width: 300px; height: auto;"> | <img src="imagenes_proyecto/SECCION_LOGIN1.png" alt="Pantalla de Panel de Administrador 2" style="max-width: 300px; height: auto;">       |

| **Pantalla de Panel de Administrador (1)**     | **Pantalla de Panel de Administrador (2)**     |
|------------------------------------------------|------------------------------------------------|
| <img src="imagenes_proyecto/SECCION_PANEL_ADMINISTRADOR1.png" alt="Pantalla de Panel de Administrador 1" style="max-width: 300px; height: auto;"> | <img src="imagenes_proyecto/SECCION_DATOS1.png" alt="Pantalla de Panel de Administrador 2" style="max-width: 300px; height: auto;"> |

| **Pantalla de Panel de Administrador (3)**     | **Pantalla de Panel de Administrador (4)**     |
|------------------------------------------------|------------------------------------------------|
| <img src="imagenes_proyecto/SECCION_DATOS2.png" alt="Pantalla de Panel de Administrador 3" style="max-width: 300px; height: auto;"> | <img src="imagenes_proyecto/SECCION_DATOS3.png" alt="Pantalla de Panel de Administrador 4" style="max-width: 300px; height: auto;"> |

| **Diagrama de Clases **                                                                                                          | **Diagrama de dependencias frontend**                                                                                                               |
|----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| <img src="imagenes_proyecto/DIAGRAMA_CLASES_YASUNI.png" alt="Diagrama de clases Yasuni" style="max-width: 300px; height: auto;"> | <img src="imagenes_proyecto/DIAGRAMA_DEPENDENCIAS_FRONTEND.png" alt="Diagrama de dependencias de frontend" style="max-width: 300px; height: auto;"> |


| **Diagrama de Bases de datos LDM **                                                                                                       | **Diagrama de Bases de datos PDM**                                                                                                        |
|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| <img src="imagenes_proyecto/DIAGRAMA_BASE_DE_DATOS_LDM.png" alt="Diagrama de bases de datos LDM" style="max-width: 300px; height: auto;"> | <img src="imagenes_proyecto/DIAGRAMA_BASE_DE_DATOS_PDM.png" alt="Diagrama de bases de datos PDM" style="max-width: 300px; height: auto;"> |

## 📜 **Licencia**

Este proyecto está licenciado bajo la **MIT License**. Consulta el archivo `LICENSE` para más detalles.

---

🎉 ¡**Gracias por explorar YasuniECY!** ☕📚