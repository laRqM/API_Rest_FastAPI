from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from config.db import engine, meta_data

profesor_materia = Table(
    "profesor_materia",
    meta_data,
    Column("id_profesor_materia", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("id_profesor", Integer, ForeignKey("persona.id_persona"), nullable=False),
    Column("id_materia", Integer, ForeignKey("materia.id_materia"), nullable=False)
)

# Verificar si la tabla "profesor_materia" existe antes de crearla
inspector = inspect(engine)
if not inspector.has_table("profesor_materia"):
    meta_data.create_all(engine)