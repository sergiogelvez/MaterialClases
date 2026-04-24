import json
from pathlib import Path

Archivo = Path("tareas.json")

def cargar_tareas() -> list[dict]:
    # carga las tareas desde el json
    if not Archivo.exists():
        return []
    with open(Archivo, "r", encoding="utf-8") as f:
        return json.load(f)
    
def guardar_tareas(tareas: list[dict]) -> None:
    # guarda las tareas desde el json
    with open(Archivo, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)

def siguiente_id(tareas: list[dict]) -> int:
    # retorna el siguiente id disponible.
    if not tareas:
        return 1
    return max(t["id"] for t in tareas) + 1
