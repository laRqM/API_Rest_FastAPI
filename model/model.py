from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from config.db import engine, meta_data

alumno_materia = Table(
    "alumno_materia",
    meta_data,
    Column("id_alumno_materia", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("id_alumno", Integer, ForeignKey("persona.id_persona"), nullable=False),
    Column("id_materia", Integer, ForeignKey("materia.id_materia"), nullable=False)
)

# Verificar si la tabla "materia" existe antes de crearla
inspector = inspect(engine)
if not inspector.has_table("alumno_materia"):
    meta_data.create_all(engine)
