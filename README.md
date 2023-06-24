# CRUD | API Rest usando FastAPI

Esta es una una API Rest para una prueba técnica para un proyecto escolar. La API de tipo CRUD permite crear las tablas configuradas en `/model`. A menos que ya estén creadas, en cuyo caso, no se hace nada.

<details>

<summary>ENDPOINTS</summary>

## Default

Endpoint predeterminado. No afecta en nada.

## Personas

Contiene la información de los alumnos y profesores. Estos son identificados como uno u otro mediante la tabla tipo_persona.

Permite:

* **Crear personas**.
* **Buscar personas por ID**.
* **Buscar datos en personas que tengan id_tipo_persona 1(profesores)**.
* **Buscar datos en personas que tengan id_tipo_persona 2(alumnos)**.
* **Actualizar datos de una persona**.
* **Borrar a una persona**.
* **Obtener una lista de profesores**.
* **Obtener una lista de alumnos**.

## tipo_personas

Catálogo de los tipos de persona. En este ejercicio, solo son dos:
* **Profesor, con ID 1**.
* **Alumno, con ID 2**.

## Materias

Contiene la información de las materias del instituto.

Permite:

* **Crear materias**.
* **Borrar materias**.
* **Actualizar materias**.
* **Obtener una lista de todas materias**.

## endpoint_especifico

Endpoints solicitados en el documento de la prueba técnica.

Permiten:

* **Obtener la información de un alumno y las materias a las que está inscrito. Esto usando su ID**.
* **Inscribir a un alumno a una materia**.
* **Asignar una materia a un profesor**.
* **Obtener la información de un alumno usando su ID**.
</details>

<details>
  <summary>BASE DE DATOS</summary>
  
  La conexión a la base de datos debe ser configurada en el archivo `db.py` que se encuentra en la carpeta `/config`. La API está pensada para ser usada con MySQL o MariaDB.
  Si las tablas configuradas en `/model` no son detectadas en la base de datos, estas serán creadas.
</details>

<details>
  <summary>ENTORNO VIRTUAL DE PYTHON</summary>

  La API fue creada usando a virtualenviroment como entorno virtual de Python. Para usar virtualenviroment primero debemos tener instalado virtualenv:
  ```python
  python -m pip install --user virtualenv
  ```

  Después nos ubicamos en la carpeta donde trabajaremos y entramos usando `cd`. Una vez en la carpeta, usamos el comando:
  ```python
  python -m venv venv
  ```

  Donde el segundo `venv` será el nombre de la carpeta que contendrá el entorno virtual.
  Finalmente, para activar el entorno virtual usamos el comando:
  - Para CMD en Windows
  ```python
  venv\Scripts\activate.bat
  ```
  - Para PowerShell en Windows
  ```python
  venv\Scripts\Activate.ps1
  ```
  - MacOS/Linux
  ```python
  source venv/bin/activate
  ```
</details>

<details>
  <summary>DEPENDENCIAS</summary>
  
  Con el entorno virtual corriendo, usaremos el archivo `requirements.txt` que contiene las dependencias necesarias para que la API funcione.
  Para instalar desde el archivo `requirements.txt`, se debe usar el comando:
  ```python
  pip install -r requirements.txt
  ```
</details>
