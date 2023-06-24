from pydantic import BaseModel
from typing import Optional

class AlumnoMateria(BaseModel):
    id_alumno_materia: Optional[int]
    id_alumno: int
    id_materia: int
