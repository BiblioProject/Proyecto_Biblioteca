# 📚 Proyecto Biblioteca

**Proyecto Biblioteca** es una aplicación web robusta y eficiente desarrollada con **Django** para la gestión integral de bibliotecas. Permite administrar **libros**, **lectores**, **préstamos**, **géneros**, **editoriales** e **idiomas** mediante una interfaz moderna, intuitiva y funcional.

🎯 Diseñado para bibliotecas escolares, universitarias o comunitarias, optimiza procesos y digitaliza la gestión bibliotecaria con foco en **usabilidad** y **escalabilidad**.

---

## 📑 Tabla de Contenidos

* [📘 Descripción](#-descripción)
* [⚙️ Utilidad](#️-utilidad)
* [🚀 Funcionalidades Principales](#-funcionalidades-principales)
* [🧰 Requisitos Previos](#-requisitos-previos)
* [💻 Instalación](#-instalación)
* [🧪 Uso](#-uso)
* [📂 Estructura del Proyecto](#-estructura-del-proyecto)
* [🧪 Ejecutar Pruebas](#-ejecutar-pruebas)
* [🤝 Contribuir](#-contribuir)

---

## 📘 Descripción

**Proyecto Biblioteca** es una solución integral construida con **Django**, que proporciona una experiencia *responsive* para administrar bibliotecas. Su arquitectura modular y extensible facilita la adaptación a las necesidades de cada institución.

---

## ⚙️ Utilidad

✅ Automatización de tareas como registros de préstamos y sanciones.
✅ Organización centralizada de libros, lectores, géneros, etc.
✅ Interfaz amigable y accesible desde cualquier navegador moderno.
✅ Escalabilidad para bibliotecas pequeñas o grandes instituciones.

---

## 🚀 Funcionalidades Principales

### 📚 Gestión de Libros

* CRUD completo (Crear, Leer, Actualizar, Eliminar).
* Búsquedas avanzadas por múltiples filtros.
* Registro detallado: título, autor, año, ISBN, idioma, editorial, género, stock, disponibilidad.

### 🧍 Gestión de Lectores

* Registro de datos personales.
* Control de sanciones.

### 🔄 Gestión de Préstamos

* Control de préstamos y devoluciones.
* Fechas automáticas y cálculo de sanciones.
* Historial por lector.

### 🗃️ Gestión de Categorías

* Géneros, Editoriales e Idiomas personalizables.

### 🛠️ Panel de Administración

* Interfaz segura para administración completa.
* Estadísticas visuales del estado general.

### 🔐 Autenticación de Usuarios

* Sistema de login/logout.
* Roles y permisos configurables.

### 📊 Dashboard Visual

* Métricas clave: libros disponibles, préstamos activos, usuarios registrados.

### 🔍 Filtros y Búsquedas Avanzadas

---

## 🧰 Requisitos Previos

### 💾 Software

* Python `>=3.10` (ideal: `3.11+`)
* Django `5.1.5`
* `pip`, `git`
* Navegador moderno
* XAMPP *(opcional para MySQL)*

### 📦 Dependencias Python

```txt
django==5.1.5
# Opcionales:
mysqlclient
pymysql
python-decouple
```

---

## 💻 Instalación

### 🔧 Paso a paso:

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

3. **Instala dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configura la base de datos:**
   *(Por defecto usa SQLite)*
   Para usar MySQL, edita `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_base',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **Ejecuta migraciones:**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crea superusuario:**

```bash
python manage.py createsuperuser
```

---

## 🧪 Uso

1. **Ejecuta el servidor:**

```bash
python manage.py runserver
```

2. **Accede en el navegador:**

* Aplicación: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

3. **Inicia sesión** con el superusuario y comienza a explorar el sistema.

---

## 📂 Estructura del Proyecto

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

## 🧪 Ejecutar Pruebas

Ejecuta todas las pruebas:

```bash
python manage.py test
```

Pruebas específicas de la app:

```bash
python manage.py test app_biblioteca
```

---

## 🤝 Contribuir

¡Tus aportes son bienvenidos! 🚀

1. Haz un **Fork**
2. Crea una rama:

   ```bash
   git checkout -b nombre-de-tu-rama
   ```
3. Realiza tus cambios y haz commit:

   ```bash
   git commit -m "Describe tus cambios"
   ```
4. Sube los cambios:

   ```bash
   git push origin nombre-de-tu-rama
   ```
5. Abre un **Pull Request** con descripción detallada.

### ✅ Buenas prácticas

* Sigue la guía PEP 8.
* Agrega pruebas para nuevas funciones.
* Documenta tus cambios claramente.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.

