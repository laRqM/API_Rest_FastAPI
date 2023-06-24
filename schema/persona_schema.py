from pydantic import BaseModel
from typing import Optional

class Persona(BaseModel):
    id_persona: Optional[int]
    nombre_uno: str
    nombre_dos: str
    apellido_uno: str
    apellido_dos: str
    id_tipo_persona: int