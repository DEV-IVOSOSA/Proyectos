import pygame as py
import modules.carta as carta
import modules.variables as var
import modules.auxiliar as aux
import random as rd

def inicializar_participante(pantalla: py.Surface, nombre: str = "PC"):
    participante = {}
    participante["nombre"] = nombre
    participante["hp_inicial"] = 0
    participante["hp_actual"] = 0
    participante["attack"] = 0
    participante["defense"] = 0
    participante["score"] = 0

    participante["mazo_asignado"] = []
    participante["cartas_mazo"] = []
    participante["cartas_mazo_usadas"] = []

    participante["screen"] = pantalla
    participante["pos_deck_inicial"] = (0, 0)
    participante["pos_deck_jugado"] = (0, 0)

    return participante

def get_hp_participante(participante: dict) -> int:
    return participante.get("hp_actual", 0)

def set_hp_participante(participante: dict, hp_actual: int):
    participante["hp_actual"] = hp_actual

def get_hp_inicial_participante(participante: dict) -> int:
    return participante.get("hp_inicial", 0)

def get_attack_participante(participante: dict) -> int:
    return participante.get("attack", 0)

def get_defense_participante(participante: dict) -> int:
    return participante.get("defense", 0)

def get_nombre_participante(participante: dict) -> str:
    return participante.get("nombre", "")

def set_nombre_participante(participante: dict, nuevo_nombre: str):
    participante["nombre"] = nuevo_nombre

def get_cartas_participante(participante: dict) -> list[dict]:
    return participante.get("cartas_mazo", [])

def get_cartas_restantes_participante(participante: dict) -> list[dict]:
    return participante.get("cartas_mazo", [])

def get_cartas_jugadas_participante(participante: dict) -> list[dict]:
    return participante.get("cartas_mazo_usadas", [])

def get_score_participante(participante: dict) -> int:
    return participante.get("score", 0)

def get_coordenadas_mazo_inicial(participante: dict):
    return participante.get("pos_deck_inicial")

def get_coordenadas_mazo_jugado(participante: dict):
    return participante.get("pos_deck_jugado")

def get_carta_actual_participante(participante: dict):
    if participante.get("cartas_mazo_usadas"):
        return participante.get("cartas_mazo_usadas")[-1]
    return None

def setear_stat_participante(participante: dict, stat: str, valor: int):
    participante[stat] = valor

def set_cartas_participante(participante: dict, lista_cartas: list[dict]):
    """Asigna las cartas al participante haciendo copias independientes"""
    cartas_copiadas = []
    for carta_original in lista_cartas:
        carta_copia = carta_original.copy()
        carta_copia["coordenadas"] = list(get_coordenadas_mazo_inicial(participante))
        cartas_copiadas.append(carta_copia)

    participante["mazo_asignado"] = cartas_copiadas
    participante["cartas_mazo"] = [c.copy() for c in cartas_copiadas]
    
    print(f"{participante.get("nombre")} recibió {len(cartas_copiadas)} cartas")

def set_score_participante(participante: dict, nuevo_score: int):
    participante["score"] = nuevo_score

def add_score_participante(participante: dict, score: int):
    participante["score"] += score

def asignar_stats_iniciales_participante(participante: dict):
    participante["hp_inicial"] = aux.reducir(
        carta.get_hp_carta,
        participante.get("mazo_asignado")
    )

    participante["hp_actual"] = participante["hp_inicial"]

    participante["attack"] = aux.reducir(
        carta.get_atk_carta,
        participante.get("mazo_asignado")
    )

    participante["defense"] = aux.reducir(
        carta.get_def_carta,
        participante.get("mazo_asignado")
    )

def chequear_valor_negativo(stat: int):
    return max(0, stat)

def aplicar_bonus_a_stat(stat: int, bonus: int) -> int:
    """Aplica el bonus porcentual al stat"""
    if bonus is None:
        bonus = 0
    porcentaje_bonus = bonus
    stat_con_bonus = stat * (1 + porcentaje_bonus / 100)
    return int(stat_con_bonus)

def sumar_stats_carta(participante: dict, carta_jugada: dict):
    """Suma las stats de la carta jugada al participante"""
    participante["hp_actual"] += carta.get_hp_carta(carta_jugada)
    participante["attack"] += carta.get_atk_carta(carta_jugada)
    participante["defense"] += carta.get_def_carta(carta_jugada)

def restar_stats_participante(participante: dict, carta_perdedora: dict, is_critic: bool):
    """
    Resta stats al participante basado en la carta perdedora.
    Aplica el bonus a los stats de la carta antes de restar.
    """
    damage_mul = 1
    if is_critic:
        damage_mul = 3
        print("¡CRÍTICO! x3 de daño")

    # Obtener bonus de la carta perdedora
    bonus = carta.get_bonus_carta(carta_perdedora)
    
    # Aplicar bonus a cada stat de la carta perdedora
    hp_carta = aplicar_bonus_a_stat(carta.get_hp_carta(carta_perdedora), bonus)
    atk_carta = aplicar_bonus_a_stat(carta.get_atk_carta(carta_perdedora), bonus)
    def_carta = aplicar_bonus_a_stat(carta.get_def_carta(carta_perdedora), bonus)

    # Aplicar multiplicador crítico
    hp_carta *= damage_mul
    atk_carta *= damage_mul
    def_carta *= damage_mul

    
    # Restar stats al participante
    participante["hp_actual"] = chequear_valor_negativo(participante.get("hp_actual") - hp_carta)
    participante["attack"] = chequear_valor_negativo(participante.get("attack") - atk_carta)
    participante["defense"] = chequear_valor_negativo(participante.get("defense") - def_carta)

def jugar_carta(participante: dict):
    """
    Saca una carta del mazo y la pone en juego.
    SUMA las stats de la carta al participante.
    """
    if participante.get("cartas_mazo"):
        print(f"{participante.get("nombre")} tiene {len(participante.get("cartas_mazo"))} cartas")
        
        carta_actual = participante.get("cartas_mazo").pop()
        carta.asignar_coordenadas_carta(carta_actual, get_coordenadas_mazo_jugado(participante))
        carta.cambiar_visibilidad(carta_actual)
        participante.get("cartas_mazo_usadas").append(carta_actual)
        
        # SUMAR las stats de la carta jugada
        sumar_stats_carta(participante, carta_actual)
        
        return True
    else:
        print(f"{participante.get("nombre")} no tiene más cartas")
    return False

def tiene_cartas(participante: dict) -> bool:
    return len(participante.get("cartas_mazo", [])) > 0

def info_to_csv(participante: dict):
    return f"{get_nombre_participante(participante)},{participante.get("score")}\n"

def reiniciar_datos_participante(participante: dict):
    """Reinicia todos los datos del participante"""
    participante["score"] = 0
    participante["mazo_asignado"] = []
    participante["cartas_mazo"] = []
    participante["cartas_mazo_usadas"] = []
    participante["hp_inicial"] = 0
    participante["hp_actual"] = 0
    participante["attack"] = 0
    participante["defense"] = 0
    print(f"{participante.get("nombre")} reiniciado")

def draw_participante(participante: dict, screen: py.Surface):
    """Dibuja el mazo y la carta jugada del participante"""
    # Dibujar el mazo (carta reverso)
    if participante.get("cartas_mazo") and len(participante.get("cartas_mazo")) > 0:
        carta_reverso = participante.get("cartas_mazo")[-1].copy()
        carta_reverso["coordenadas"] = participante.get("pos_deck_inicial")
        carta_reverso["visible"] = False
        carta.draw_carta(carta_reverso, screen)
    
    # Dibujar la carta jugada
    if participante.get("cartas_mazo_usadas") and len(participante.get("cartas_mazo_usadas")) > 0:
        carta_jugada = participante.get("cartas_mazo_usadas")[-1]
        carta.draw_carta(carta_jugada, screen)