import modules.auxiliar as aux
import pygame as py

def inicializar_carta(carta_dict: dict, coords: list[int]) -> dict:
    """Inicializa una carta creando una copia independiente"""
    card = {
        "id": carta_dict.get("id", ""),
        "hp": carta_dict.get("hp", 0),
        "atk": carta_dict.get("atk", 0),
        "def": carta_dict.get("def", 0),
        "bonus": carta_dict.get("bonus"),
        "ruta_frente": carta_dict.get("ruta_frente", ""),
        "ruta_reverso": carta_dict.get("ruta_reverso", ""),
        "visible": False,
        "coordenadas": coords,
        "imagen": None,
        "rect": None
    }
    
    return card

def esta_visible(cartas_dict: dict) -> bool:
    return cartas_dict.get("visible", False)

def cambiar_visibilidad(cartas_dict: dict):
    cartas_dict["visible"] = not cartas_dict.get("visible", False)

def get_hp_carta(cartas_dict: dict) -> int:
    return cartas_dict.get("hp", 0)

def get_def_carta(cartas_dict: dict) -> int:
    return cartas_dict.get("def", 0)

def get_atk_carta(cartas_dict: dict) -> int:
    return cartas_dict.get("atk", 0)

def get_bonus_carta(cartas_dict: dict) -> int:
    """
    Retorna el bonus de la carta.
    Cada estrella representa 1% de bonus.
    Rango: 1-7 estrellas
    """
    return cartas_dict.get("bonus", 1)

def asignar_coordenadas_carta(cartas_dict: dict, coordenadas: tuple[int]):
    cartas_dict["coordenadas"] = coordenadas

def calcular_ataque_con_bonus(carta_jugador: dict) -> int:
    """
    Calcula el ataque de una carta aplicando su bonus.
    Ataque final = Ataque base + (Ataque base * bonus%)
    """
    atk = carta_jugador.get("atk", 0)
    bonus = carta_jugador.get("bonus", 0)
    
    # Cada estrella suma 1% de bonus
    porcentaje_bonus = bonus
    ataque_con_bonus = atk * (1 + porcentaje_bonus / 100)
    
    return int(ataque_con_bonus)

def draw_carta(cartas_dict: dict, screen: py.Surface):
    """Dibuja la carta en la pantalla"""
    if cartas_dict.get("visible"):
        cartas_dict["imagen"] = aux.redimensionar_imagen(cartas_dict.get("ruta_frente"), 40)
    else:
        cartas_dict["imagen"] = aux.redimensionar_imagen(cartas_dict.get("ruta_reverso"), 40)
        
    cartas_dict["rect"] = cartas_dict.get("imagen").get_rect()
    cartas_dict["rect"].topleft = cartas_dict.get("coordenadas")

    screen.blit(cartas_dict.get("imagen"), cartas_dict.get("rect"))
