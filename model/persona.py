from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from config.db import engine, meta_data

persona = Table(
    "persona",
    meta_data,
    Column("id_persona", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("nombre_uno", String(50), nullable=False),
    Column("nombre_dos", String(50)),
    Column("apellido_uno", String(50), nullable=False),
    Column("apellido_dos", String(50)),
    Column("id_tipo_persona", Integer, nullable=False),
    ForeignKeyConstraint(
        ["id_tipo_persona"],
        ["tipo_persona.id_tipo_persona"],
    ),
)

# Verificar si la tabla "materia" existe antes de crearla
inspector = inspect(engine)
if not inspector.has_table("persona"):
    meta_data.create_all(engine)