from pydantic import BaseModel
from typing import Optional

class TipoPersona(BaseModel):
    id_tipo_persona: Optional[int]
    designacion: str