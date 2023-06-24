from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from config.db import engine, meta_data

tipo_persona_tabla = Table(
    "tipo_persona",
    meta_data,
    Column("id_tipo_persona", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("designacion", String(50), nullable=False)
)

# Verificar si la tabla "tipo_persona" existe antes de crearla
inspector = inspect(engine)
if not inspector.has_table("tipo_persona"):
    meta_data.create_all(engine)