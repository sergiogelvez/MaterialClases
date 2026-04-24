from pydantic import BaseModel
from typing import Optional

class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    completada: bool = False

class TareaCreate(TareaBase):
    # modelo para crear una tarea (no incluye id)
    pass

class Tarea(TareaBase):
    # Modelo completo con id asignado por el servidor
    id: int
