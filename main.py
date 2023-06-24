from fastapi import FastAPI
from router.router import user

description = """
<h3>API Rest de prueba usando FastAPI. Esto es una prueba técnica para un proyecto escolar.

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
"""

app = FastAPI(
    title="Prueba técnica",
    description=description,
    version="0.0.1",
    openapi_tags=[{
        "name": "default",
        "description": "<h5>Endpoint predeterminado. No molesta, no tiene caso quitarlo.</h5>"
    }, {
        "name": "personas",
        "description": "<h5>Sea Alumno o Profesor. Aquí se manejan sus endpoints.</h5>"
    }, {
        "name": "tipo_personas",
        "description": "<h5>Catálogo de tipo de persona. Esto es, si es Alumno, Profesor, etc. Aquí se manejan sus endpoints</h5>"
    }, {
        "name": "materias",
        "description": "<h5>Las materias del instituto. Aquí se manejan sus endpoints</h5>"
    }, {
        "name": "endpoint_especifico",
        "description": "<h5>Endpoints explícitamente solicitados en la prueba técnica.</h5>"
    }]
)

app.include_router(user)
