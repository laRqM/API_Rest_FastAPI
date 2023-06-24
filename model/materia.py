from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from config.db import engine, meta_data

materia = Table(
    "materia",
    meta_data,
    Column("id_materia", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("nombre", String(50), nullable=False, unique=True)
)

# Verificar si la tabla "materia" existe antes de crearla
inspector = inspect(engine)
if not inspector.has_table("materia"):
    meta_data.create_all(engine)
