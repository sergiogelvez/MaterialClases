from fastapi import FastAPI, HTTPException
from modelos import Tarea, TareaCreate
from almacenamiento import cargar_tareas, guardar_tareas, siguiente_id

app = FastAPI(
    title="Aplicación de gestión de tareas",
    description="Taller de sistemas distribuidos - UIS",
    version="0.9.0"
)

""" @app.get("/")
def raiz():
    return {"Mensaje": "Bienvenido a la api de gestión de tareas"}
 """

@app.get("/tareas", response_model=list[Tarea])
def listar_tareas():
    # devuelve las tareas almacenadas.
    return cargar_tareas()

@app.get("/tareas/{tarea_id}", response_model=Tarea)
def obtener_tarea(tarea_id: int):
    # devuelve una tarea específica por el id
    tareas = cargar_tareas()
    for t in tareas:
        if t["id"] == tarea_id:
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.post("/tareas", response_model=Tarea, status_code=201)
def crear_tareas(tarea: TareaCreate):
    # crea la tarea y la almacena
    tareas = cargar_tareas()
    nueva = tarea.model_dump()
    nueva["id"] = siguiente_id(tareas)
    tareas.append(nueva)
    guardar_tareas(tareas)
    return nueva