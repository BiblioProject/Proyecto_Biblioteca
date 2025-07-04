
# Proyecto Biblioteca

**Proyecto Biblioteca** es una aplicación web robusta y eficiente desarrollada con Django para la gestión integral de bibliotecas. Este sistema permite administrar libros, lectores, préstamos, géneros, editoriales e idiomas a través de una interfaz moderna, intuitiva y altamente funcional. Diseñado para bibliotecas escolares, universitarias o comunitarias, optimiza procesos y digitaliza la gestión de recursos bibliotecarios con un enfoque en la usabilidad y la escalabilidad.

---

## Tabla de Contenidos

- [Descripción](#descripción)  
- [Utilidad](#utilidad)  
- [Funcionalidades Principales](#funcionalidades-principales)  
- [Requisitos Previos](#requisitos-previos)  
- [Instalación](#instalación)  
- [Uso](#uso)  
- [Estructura del Proyecto](#estructura-del-proyecto)  
- [Ejecutar Pruebas](#ejecutar-pruebas)  
- [Contribuir](#contribuir)  
- [Licencia](#licencia)  

---

## Descripción

**Proyecto Biblioteca** es una solución integral para la gestión de bibliotecas, construida con Django, un framework de Python reconocido por su robustez y seguridad. La aplicación ofrece una interfaz web *responsive* que permite a los administradores gestionar de manera eficiente los recursos de la biblioteca, desde el inventario de libros hasta los registros de préstamos y usuarios. Su diseño modular y extensible facilita la integración de nuevas funcionalidades según las necesidades específicas de cada institución.

---

## Utilidad

Este sistema está diseñado para:

- **Optimizar procesos:** Automatiza tareas como el registro de préstamos, devoluciones y sanciones.  
- **Mejorar la organización:** Centraliza la información de libros, lectores, géneros, editoriales e idiomas.  
- **Facilitar el acceso:** Proporciona una interfaz amigable con búsquedas avanzadas y paneles de control.  
- **Escalabilidad:** Ideal para bibliotecas de cualquier tamaño.

---

## Funcionalidades Principales

### Gestión de Libros
- Registro, edición, eliminación y consulta de libros.  
- Información detallada: título, autor, año de publicación, ISBN, idioma, editorial, género, stock y disponibilidad.  
- Búsqueda avanzada por múltiples criterios.  

### Gestión de Lectores
- Registro y administración de datos personales.  
- Seguimiento de sanciones por retrasos o daños.  

### Gestión de Préstamos
- Registro de préstamos y devoluciones.  
- Cálculo automático de fechas de vencimiento y sanciones.  
- Historial de préstamos por lector.  

### Gestión de Géneros, Editoriales e Idiomas
- Creación, edición y eliminación de categorías para organizar el catálogo.  

### Panel de Administración
- Interfaz segura para administradores con acceso completo.  
- Estadísticas visuales del estado de la biblioteca.  

### Autenticación de Usuarios
- Sistema de login/logout con roles (administrador, usuario estándar).  
- Gestión de permisos.  

### Dashboard
- Resumen visual con métricas clave: libros disponibles, préstamos activos, lectores registrados, etc.  

### Búsquedas y Filtros
- Listados dinámicos con filtros avanzados.  

---

## Requisitos Previos

### Software

- Python: `3.10` o superior (recomendado `3.11+`)  
- Django: `5.1.5`  
- pip  
- Git  
- Navegador web moderno  
- XAMPP *(opcional para usar MySQL)*  

### Dependencias Python

Instalar las dependencias listadas en `requirements.txt`:

```bash
django==5.1.5
# Opcionales:
# mysqlclient o pymysql
# python-decouple
````

---

## Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/tu_usuario/proyecto_biblioteca.git
cd proyecto_biblioteca/Proyecto_Biblioteca-1/Proyecto_Biblioteca/Proyecto_Biblioteca/Proyecto_Biblioteca-2
```

2. **Crea y activa un entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
# o bien:
pip install django==5.1.5
```

4. **Configura la base de datos:**

Por defecto usa SQLite. Para usar MySQL, edita `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_de_tu_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **Realiza las migraciones:**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crea un superusuario:**

```bash
python manage.py createsuperuser
```

---

## Uso

1. **Inicia el servidor de desarrollo:**

```bash
python manage.py runserver
```

2. **Accede a la aplicación:**

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Panel de administración: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

3. **Inicia sesión** con las credenciales del superusuario.

4. **Explora funcionalidades:**

   * Registro de libros, lectores y préstamos.
   * Uso del dashboard.
   * Búsquedas avanzadas.

---

## Estructura del Proyecto

```plaintext
proyecto_biblioteca/
├── app_biblioteca/
│   ├── migrations/          
│   ├── templates/          
│   ├── static/             
│   ├── models.py           
│   ├── views.py            
│   ├── forms.py            
│   ├── urls.py             
│   └── ...
├── biblioteca/
│   ├── settings.py         
│   ├── urls.py             
│   └── wsgi.py             
├── manage.py               
├── requirements.txt        
└── README.md               
```

---

## Ejecutar Pruebas

Ejecuta todas las pruebas del proyecto:

```bash
python manage.py test
```

Para pruebas específicas de la app:

```bash
python manage.py test app_biblioteca
```

---

## Contribuir

¡Agradecemos cualquier contribución! Pasos para colaborar:

1. **Fork** del repositorio
2. Crea una nueva rama:

```bash
git checkout -b nombre-de-tu-rama
```

3. Realiza tus cambios y haz commit:

```bash
git commit -m "Descripción clara de los cambios"
```

4. **Push** a tu fork:

```bash
git push origin nombre-de-tu-rama
```

5. Abre un **Pull Request** con una descripción detallada.

### Buenas prácticas

* Sigue las guías de estilo (PEP 8).
* Incluye pruebas para nuevas funcionalidades.
* Documenta tus cambios.

---
## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más información.
