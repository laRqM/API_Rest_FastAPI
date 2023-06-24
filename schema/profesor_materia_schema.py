from pydantic import BaseModel
from typing import Optional

class ProfesorMateria(BaseModel):
    id_profesor_materia: Optional[int]
    id_profesor: int
    id_materia: int