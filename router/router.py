from fastapi import APIRouter, Response, status
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from config.db import engine
from model.tipo_persona import tipo_persona_tabla
from model.materia import materia
from model.persona import persona
from model.profesor_materia import profesor_materia
from model.alumno_materia import alumno_materia
from schema.tipo_persona_schema import TipoPersona
from schema.materia_schema import Materia
from schema.persona_schema import Persona
from schema.profesor_materia_schema import ProfesorMateria
from schema.alumno_materia_schema import AlumnoMateria
from typing import List, Optional, Dict, Union

user = APIRouter()

@user.get(
    "/",
)
def root():
    return {"message": "¡Conexión exitosa!"}

####################################################
##########     MANEJO DE LAS PERSONAS     ##########
####################################################

@user.get(
    "/api/persona/{user_id}",
    tags=["personas"],
    description="<h2>Obtener a un usuario específico por medio de su ID</h2>",
    response_model=Persona
)
def get_persona(id_persona: int):
    with engine.connect() as conn: # Nos conectamos a la base de datos
        result = conn.execute(persona.select().where(persona.c.id_persona == id_persona)).first() # Se ejecuta la consulta a la base de datos. Se hace un SELECT a la tabla persona WHERE persona.id_persona sea igual a id_persona. Este último se lo pasamos por Swagger

        if result: # Si result es true...
            user_dict = { # Creamos un diccionario que contiene los valores de la consulta
                "id_persona": result[0],
                "nombre_uno": result[1],
                "nombre_dos": result[2],
                "apellido_uno": result[3],
                "apellido_dos": result[4],
                "id_tipo_persona": result[5]
            }
            return user_dict # Si se encontró un resultado, devolvemos el diccionario...

        return None # Si no se encontró nada, no se hace nada.

@user.get(
    "/api/persona/profesores/",
    tags=["personas"],
    description="<h2>Obtener una lista de todos los profesores.</h2><br><h4>Esta función asume que el ID del profesor en la tabla tipo_persona es 1</h4>",
    response_model=List[Persona]
)
def get_profesor():
    with engine.connect() as conn: # Nos conectamos a la base de datos
        result = conn.execute(persona.select().where(persona.c.id_tipo_persona == 1)).fetchall() # Se ejecuta la consulta a la base de datos. Se hace un SELECT a la tabla persona WHERE persona.id_tipo_persona sea igual a 1. Aquí se asume que el ID 1 pertenece al tipo de persona Profesor.

        personas = [] # Creamos una lista vacía que almacenará los diccionarios
        for row in result: # Iteramos sobre los resultados de la consulta
            persona_dict = { # Creamos un diccionario que contiene los resultados de la consulta
                "id_persona": row.id_persona,
                "nombre_uno": row.nombre_uno,
                "nombre_dos": row.nombre_dos,
                "apellido_uno": row.apellido_uno,
                "apellido_dos": row.apellido_dos,
                "id_tipo_persona": row.id_tipo_persona
            }
            personas.append(persona_dict) # Agregamos el diccionario a la lista vacía

        return personas # Ya que se recorrieron todos los resultados de la consulta, devolvemos la lista vacía(que en este punto ya no está vacía :P)

@user.get(
    "/api/persona/alumnos/",
    tags=["personas"],
    description="<h2>Obtener una lista de todos los alumnos.</h2><br><h4>Esta función asume que el ID del alumno en la tabla tipo_persona es 2</h4>",
    response_model=List[Persona]
)
def get_alumno():
    with engine.connect() as conn: # Nos conectamos a la base de datos
        result = conn.execute(persona.select().where(persona.c.id_tipo_persona == 2)).fetchall() # Se ejecuta la consulta a la base de datos. Se hace un SELECT a la tabla persona WHERE persona.id_tipo_persona sea igual a 2. Aquí se asume que el ID 2 pertecene al tipo de persona Alumno.

        personas = [] # Creamos una lista vacía que almacenará los diccionarios
        for row in result: # Iteramos sobre los resultados de la consulta
            persona_dict = { # Creamos un diccionario que contiene los resultados de la consulta
                "id_persona": row.id_persona,
                "nombre_uno": row.nombre_uno,
                "nombre_dos": row.nombre_dos,
                "apellido_uno": row.apellido_uno,
                "apellido_dos": row.apellido_dos,
                "id_tipo_persona": row.id_tipo_persona
            }
            personas.append(persona_dict) # Agreagamos el diccionario a la lista vacía

        return personas # Ya que se recorrieron todos los resultados de la consulta, devolvemos la lista vacía(que en este punto ya no está vacía :P)

@user.post(
    "/api/persona",
    tags=["personas"],
    description="<h2>Crear a una persona en el sistema</h2><br><h4>Se utiliza el ID en la tabla tipo_persona para designar a la nueva persona como Profesor o Alumnos</h4>",
    status_code=HTTP_201_CREATED,
    response_model=Persona
)
def create_persona(datos_persona: Persona):
    with engine.connect() as conn: # Nos conectamos a la base de datos
        new_persona = datos_persona.dict() # Creamos un diccionario con los datos obtenidos en el formulario. Se lo asigna a la variable new_persona

        result = conn.execute(persona.insert().values(new_persona)) # Ejecutamos la consulta. Es decir, mandamos el SQL query de creación de persona usando los datos en new_persona.
        persona_id = result.inserted_primary_key[0] # Obtenemos el ID de la persona que acabamos de crear

        conn.commit() # Confirmamos el procedimiento a la base de datos

        created_persona = conn.execute(persona.select().where(persona.c.id_persona == persona_id)).first() # Ejecutamos una consulta a la base de datos para obtener los datos de la persona que acabamos de crear. Para ello, usamos el ID de la persona que recién se creó.

        if created_persona: # Si created_persona es true...
            user_dict = { # Creamos un diccionario con los datos de la persona recién creada
                "id_persona": created_persona[0],
                "nombre_uno": created_persona[1],
                "nombre_dos": created_persona[2],
                "apellido_uno": created_persona[3],
                "apellido_dos": created_persona[4],
                "id_tipo_persona": created_persona[5]
            }
            return user_dict # Devolvemos el diccionario

        return None # En caso contrario, o sea, que no se creó, no se hace nada.

@user.put(
    "/api/persona/{user_id}",
    tags=["personas"],
    description="<h2>Actualizar los datos de una persona</h2>",
    response_model=Persona
)
def update_persona(data_update: Persona, persona_id: int):
    with engine.connect() as conn: # Nos conectamos a la base de datos
        tipo_persona_exists = conn.execute( # tipo_persona_exists será igual a una consulta a la base de datos.
            tipo_persona_tabla.select().where(tipo_persona_tabla.c.id_tipo_persona == data_update.id_tipo_persona) # Se hace un SELECT a la tabla tipo_persona(nombrada tipo_persona_tabla en tipo_persona.py) WHERE tipo_persona_tabla.id_tipo_persona sea igual al id_tipo_persona que se proporcionó en el formulario.
        ).first()

        if not tipo_persona_exists: # Si no hay resultado, es decir, que el ID está mal o no existe...
            return Response(status_code=HTTP_400_BAD_REQUEST, content="id_tipo_persona inválido o inexistente") # Devolvemos un error HTTP 400

        conn.execute( # Ejecutamos a conn
            persona.update() # Aquí actualizaremos los datos en la tabla con los valores que se nos han pasado
            .values(
                nombre_uno=data_update.nombre_uno,
                nombre_dos=data_update.nombre_dos,
                apellido_uno=data_update.apellido_uno,
                apellido_dos=data_update.apellido_dos,
                id_tipo_persona=data_update.id_tipo_persona
            )
            .where(persona.c.id_persona == persona_id) # Donde persona.id_persona sea igual a persona_id. Siendo este último el dato se nos está enviando desde el formulario
        )

        conn.commit() # Confirmamos el procedimiento a la base de datos

        result = conn.execute(persona.select().where(persona.c.id_persona == persona_id)).first() # Ejecutamos una consulta a la base de datos. Hacemos un SELECT a la tabla persona WHERE persona.id_persona sea igual a persona_id. Este último es proporcionado por el formulario.

        if result: # Si result es true...
            updated_persona = Persona( # Obtenemos los datos actualizados de la persona
                id_persona=result.id_persona,
                nombre_uno=result.nombre_uno,
                nombre_dos=result.nombre_dos,
                apellido_uno=result.apellido_uno,
                apellido_dos=result.apellido_dos,
                id_tipo_persona=result.id_tipo_persona
            )
            return updated_persona # Retornamos el resultado

        return None # Si no hay resultados, no hace nada

@user.delete(
    "/api/persona/{user_id}",
    tags=["personas"],
    description="<h2>Borrar a una persona</h2>",
    status_code=HTTP_204_NO_CONTENT)
def delete_persona(id_persona: int):
    with engine.connect() as conn: # Nos conectamos a la base de datos
        conn.execute(persona.delete().where(persona.c.id_persona == id_persona)) # Generamos una consulta para eliminar a una persona en la base de datos. Se hace un DELETE en la tabla persona WHERE persona.id_persona sea igual a id_persona, siendo este último el dato que se nos envía desde el formulario
        conn.commit() # Confirmamos el procedimiento a la base de datos
        return Response(status_code=HTTP_204_NO_CONTENT) # Retornamos una respuesta de tipo HTTP 204

######################################################
###########     MANEJO DE LAS MATERIAS     ###########
######################################################
@user.get(
    "/api/materia",
    tags=["materias"],
    description="<h2>Obtener una lista de todos las materias</h2>",
    response_model=List[Materia]
)
def get_materias():
    with engine.connect() as conn: # Nos conectamos a la base de datos
        result = conn.execute(materia.select().order_by(materia.c.id_materia)) # Generamos una consulta SQL en la tabla materia ordenando por id_materia

        lista_materias = [] # Creamos una lista vacía
        for row in result: # Iteramos sobre los resultados de la consulta
            tipo_persona_obj = Materia( #tipo_persona_obj será igual a un objeto Materia. Este último contiene los datos de id_materia y nombre que se encuentran en la tabla materia en la base de datos.
                id_materia=row.id_materia,
                nombre=row.nombre
            )
            lista_materias.append(tipo_persona_obj) # Agregamos el objeto a la lista vacía

        return lista_materias # Ya que se recorrieron todos los resultados de la consulta, devolvemos la lista vacía(que en este punto ya no está vacía :P)

@user.post(
    "/api/materia",
    tags=["materias"],
    description="<h2>Crear una materia</h2>",
    status_code=HTTP_201_CREATED)
def create_materia(data_user: Materia):
    with engine.connect() as conn:  # Nos conectamos a la base de datos
        new_materia = data_user.dict() # Creamos un diccionario

        conn.execute(materia.insert().values(new_materia)) # Creamos una consulta SQL a la tabla materia donde haremos un INSERT con el valor new_materia que se está recibiendo desde el formulario
        conn.commit() # Confirmamos el procedimiento a la base de datos

        return Response(status_code=HTTP_201_CREATED) # Retornamos una respuesta HTTP 201

@user.delete(
    "/api/materia/{identificador}",
    tags=["materias"],
    description="<h2>Eliminar una materia por ID o nombre</h2>",
    status_code=HTTP_204_NO_CONTENT
)
def delete_materia(identificador: str):
    with engine.connect() as conn:  # Nos conectamos a la base de datos
        condition = None # Declaramos la variable y la inicializamos sin nada

        if identificador.isdigit(): # Si identificador(el parámetro que recibimos desde el formulario) es un digito, entramos al condicional
            condition = materia.c.id_materia == int(identificador) # condition será igual al id_materia de la tabla materia. El doble igual compara a materia.id_materia e int(identificador) para saber si son iguales.
            # Entonces, materia.c.id_materia == int(identificador) compara el campo id_materia de la tabla materia con identificador convertido a un entero. Si estos valores son iguales, esto se evalúa como True. De lo contrario, se evalúa como False.
        else:
            condition = materia.c.nombre == identificador # Compara el campo nombre de la tabla materia con identificador. Si estos valores son iguales, condition se evalúa como True, de lo contrario, se evalúa como False.
            # El resultado de la comparación se asigna a la variable condition, lo que significa que condition será True si el campo nombre coincide con el identificador y False si no coinciden.

        conn.execute(materia.delete().where(condition)) # Se ejecuta la consulta de eliminación en la base de datos. Eliminando las filas que coinciden con la comparación anterior
        conn.commit() # Confirmamos el procedimiento a la base de datos

        return Response(status_code=HTTP_204_NO_CONTENT) # Retornamos una respuesta HTTP 204

@user.put(
    "/api/materia/{id_materia}",
    tags=["materias"],
    description="<h2>Editar una materia por ID</h2>",
    response_model=Materia
)
def update_materia(id_materia: int, materia_data: Materia):
    with engine.connect() as conn:
        conn.execute(
            materia.update()
            .values(nombre=materia_data.nombre)
            .where(materia.c.id_materia == id_materia)
        )

        conn.commit()

        result = conn.execute(materia.select().where(materia.c.id_materia == id_materia)).first()

        if result:
            updated_materia = Materia(
                id_materia=result.id_materia,
                nombre=result.nombre
            )
            return updated_materia

        return None


########################################################
##########     MANEJO DE TIPO DE PERSONAS     ##########
########################################################
@user.post(
    "/api/tipo_personas",
    tags=["tipo_personas"],
    description="<h2>Crear un tipo de persona</h2>(sea alumno o profesor, etc.)",
    status_code=HTTP_201_CREATED)
def create_tipo_persona(data_user: TipoPersona):
    with engine.connect() as conn:
        new_tipo_persona = data_user.dict()

        conn.execute(tipo_persona_tabla.insert().values(new_tipo_persona))
        conn.commit()

        return Response(status_code=HTTP_201_CREATED)

@user.get(
    "/api/tipo_personas",
    tags=["tipo_personas"],
    description="<h2>Obtener una lista de todos los tipos de personas</h2>",
    response_model=List[TipoPersona]
)
def get_tipo_personas():
    with engine.connect() as conn:
        result = conn.execute(tipo_persona_tabla.select().order_by(tipo_persona_tabla.c.id_tipo_persona))

        tipo_personas = []
        for row in result:
            tipo_persona_obj = TipoPersona(
                id_tipo_persona=row.id_tipo_persona,
                designacion=row.designacion
            )
            tipo_personas.append(tipo_persona_obj)

        return tipo_personas


#####################################################
###########     ENDPOINTS ESPECÍFICOS     ###########
#####################################################
@user.get(
    "/api/alumno/{id_alumno}/materias",
    tags=["endpoint_especifico"],
    description="<h2>Obtener información de un alumno y las materias a las que está inscrito</h2>",
    response_model=Dict[str, Union[Persona, List[Materia]]]
)
def get_alumno_materias(id_alumno: int):
    with engine.connect() as conn:
        alumno_result = conn.execute(persona.select().where(persona.c.id_persona == id_alumno)).first()

        if not alumno_result or alumno_result.id_tipo_persona != 2:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Alumno no encontrado")

        alumno_info = Persona(
            id_persona=alumno_result.id_persona,
            nombre_uno=alumno_result.nombre_uno,
            nombre_dos=alumno_result.nombre_dos,
            apellido_uno=alumno_result.apellido_uno,
            apellido_dos=alumno_result.apellido_dos,
            id_tipo_persona=alumno_result.id_tipo_persona
        )

        assigned_materias = conn.execute(
            materia.select()
            .join(alumno_materia, alumno_materia.c.id_materia == materia.c.id_materia)
            .where(alumno_materia.c.id_alumno == id_alumno)
        ).fetchall()

        materias = []
        for row in assigned_materias:
            materia_obj = Materia(
                id_materia=row.id_materia,
                nombre=row.nombre
            )
            materias.append(materia_obj)

        alumno_materias = {
            "alumno": alumno_info,
            "materias": materias
        }

        return alumno_materias

@user.post(
    "/api/alumno/{id_alumno}/materia/{id_materia}",
    tags=["endpoint_especifico"],
    description="<h2>Inscribir a un alumno a una materia</h2>",
    status_code=status.HTTP_204_NO_CONTENT
)
def assign_alumno_materia(id_alumno: int, id_materia: int):
    with engine.connect() as conn:
        alumno_result = conn.execute(persona.select().where(persona.c.id_persona == id_alumno)).first()

        if not alumno_result or alumno_result.id_tipo_persona != 2:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Alumno no encontrado")

        materia_result = conn.execute(materia.select().where(materia.c.id_materia == id_materia)).first()

        if not materia_result:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Materia no encontrada")

        existing_assignment = conn.execute(
            alumno_materia.select()
            .where(alumno_materia.c.id_alumno == id_alumno)
            .where(alumno_materia.c.id_materia == id_materia)
        ).first()

        if existing_assignment:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content="El alumno ya está asignado a esta materia")

        conn.execute(alumno_materia.insert().values(id_alumno=id_alumno, id_materia=id_materia))
        conn.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

@user.post(
    "/api/profesor/{profesor_id}/materia/{materia_id}",
    tags=["endpoint_especifico"],
    description="<h2>Asignar una materia a un profesor</h2>",
    status_code=status.HTTP_204_NO_CONTENT
)
def assign_materia_profesor(profesor_id: int, materia_id: int):
    with engine.connect() as conn:
        profesor_result = conn.execute(persona.select().where(persona.c.id_persona == profesor_id)).first()

        if not profesor_result or profesor_result.id_tipo_persona != 1:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Profesor no encontrado")

        materia_result = conn.execute(materia.select().where(materia.c.id_materia == materia_id)).first()

        if not materia_result:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Materia no encontrada")

        existing_assignment = conn.execute(
            profesor_materia.select()
            .where(profesor_materia.c.id_profesor == profesor_id)
            .where(profesor_materia.c.id_materia == materia_id)
        ).first()

        if existing_assignment:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content="La materia ya está asignada a este profesor")

        conn.execute(profesor_materia.insert().values(id_profesor=profesor_id, id_materia=materia_id))
        conn.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

@user.get(
    "/api/profesor/{profesor_id}",
    tags=["endpoint_especifico"],
    description="<h2>Obtener la información de un profesor específico por su ID</h2>",
    response_model=Dict[str, Union[Persona, List[Materia]]]
)
def get_profesor_materias(profesor_id: int):
    with engine.connect() as conn:
        profesor_result = conn.execute(persona.select().where(persona.c.id_persona == profesor_id)).first()

        if not profesor_result or profesor_result.id_tipo_persona != 1:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Profesor no encontrado")

        profesor_dict = {
            "id_persona": profesor_result[0],
            "nombre_uno": profesor_result[1],
            "nombre_dos": profesor_result[2],
            "apellido_uno": profesor_result[3],
            "apellido_dos": profesor_result[4],
            "id_tipo_persona": profesor_result[5]
        }

        materias_result = conn.execute(
            materia.join(profesor_materia).join(persona)
            .select()
            .where(persona.c.id_persona == profesor_id)
        ).fetchall()

        materias = []
        for row in materias_result:
            materia_dict = {
                "id_materia": row[materia.c.id_materia.name],
                "nombre": row[materia.c.nombre.name]
            }
            materias.append(materia_dict)

        result_dict = {
            "profesor": profesor_dict,
            "materias": materias
        }

        return result_dict
