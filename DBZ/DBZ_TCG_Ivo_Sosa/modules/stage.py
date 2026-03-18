import pygame as py
import modules.variables as var
import modules.auxiliar as aux
import random as rd
import modules.carta as carta
from utn_fra.pygame_widgets import GameSound
import modules.participante_juego as participante

def inicializar_stage(jugador: dict, pantalla: py.Surface, nro_stage: int):
    stage_data = {}
    stage_data["nro_stage"] = nro_stage
    stage_data["configs"] = {}

    stage_data["cartas_mazo_inicial"] = []
    stage_data["cartas_mazo_preparadas"] = [] 
    stage_data["ruta_mazos"] = []
    
    stage_data["coords_inicial_mazo_enemigo"] = (260, 90)
    stage_data["coords_final_mazo_enemigo"] = (450, 90)

    stage_data["coords_inicial_mazo_player"] = (260, 360)
    stage_data["coords_final_mazo_player"] = (450, 360)

    stage_data["screen"] = pantalla
    stage_data["jugador"] = jugador
    stage_data["enemigo"] = participante.inicializar_participante(stage_data.get("screen"), nombre="Enemigo")
    
    participante.setear_stat_participante(stage_data.get("enemigo"), "pos_deck_inicial", stage_data.get("coords_inicial_mazo_enemigo"))
    participante.setear_stat_participante(stage_data.get("enemigo"), "pos_deck_jugado", stage_data.get("coords_final_mazo_enemigo"))
    
    participante.setear_stat_participante(stage_data.get("jugador"), "pos_deck_inicial", stage_data.get("coords_inicial_mazo_player"))
    participante.setear_stat_participante(stage_data.get("jugador"), "pos_deck_jugado", stage_data.get("coords_final_mazo_player"))
    
    stage_data["cantidad_cartas_jugadores"] = 0

    stage_data["juego_finalizado"] = False
    stage_data["puntaje_guardado"] = False
    stage_data["stage_timer"] = var.STAGE_TIMER
    stage_data["last_timer"] = py.time.get_ticks()
    stage_data["ganador"] = None

    stage_data["puntaje_stage"] = 0
    stage_data["data_cargada"] = False
    
    stage_data["shield_available"] = True
    stage_data["heal_available"] = True

    stage_data["manos_jugadas"] = 0 
    
    return stage_data

def asignar_cartas_stage(stage_data: dict, participante_juego: dict):
    """Asigna cartas aleatorias del mazo preparado a un participante"""
    cant_cartas = stage_data.get("cantidad_cartas_jugadores")
    
    if len(stage_data.get("cartas_mazo_preparadas")) >= cant_cartas:
        cartas_participante = []
        for _ in range(cant_cartas):
            carta_aleatoria = rd.choice(stage_data.get("cartas_mazo_preparadas"))
            carta_copia = {
                "id": carta_aleatoria.get("id"),
                "hp": carta_aleatoria.get("hp"),
                "atk": carta_aleatoria.get("atk"),
                "def": carta_aleatoria.get("def"),
                "bonus": carta_aleatoria.get("bonus", 1),
                "ruta_frente": carta_aleatoria.get("ruta_frente"),
                "ruta_reverso": carta_aleatoria.get("ruta_reverso"),
                "visible": False,
                "coordenadas": [0, 0],
                "imagen": None,
                "rect": None
            }
            cartas_participante.append(carta_copia)
        
        participante.set_cartas_participante(participante_juego, cartas_participante)

def modificar_estado_bonus(stage_data: dict, bonus: dict):
    stage_data[f"{bonus}_available"] = False

def generar_mazo(stage_data: dict):
    """Genera el mazo de cartas combinando todos los mazos"""
    cartas_dict = stage_data.get("cartas_mazo_inicial")
    
    if not isinstance(cartas_dict, (dict, list)):
        print(f"ERROR: cartas_mazo_inicial tipo incorrecto: {type(cartas_dict)}")
        return
    
    if isinstance(cartas_dict, list):
        for carta_inicial in cartas_dict:
            if isinstance(carta_inicial, dict):
                carta_power = carta.inicializar_carta(carta_inicial, [0, 0])
                stage_data.get("cartas_mazo_preparadas").append(carta_power)
    
    elif isinstance(cartas_dict, dict):
        for deck_name, deck_cards in cartas_dict.items():
            for carta_inicial in deck_cards:
                if isinstance(carta_inicial, dict):
                    carta_power = carta.inicializar_carta(carta_inicial, [0, 0])
                    stage_data.get("cartas_mazo_preparadas").append(carta_power)
    
    print(f"Mazo generado: {len(stage_data.get('cartas_mazo_preparadas'))} cartas")

def barajar_mazos_stage(stage_data: dict):
    """Reparte cartas a jugador y enemigo"""
    if not stage_data.get("juego_finalizado"):
        asignar_cartas_stage(stage_data, stage_data.get("jugador"))
        asignar_cartas_stage(stage_data, stage_data.get("enemigo"))

        participante.asignar_stats_iniciales_participante(stage_data.get("jugador"))
        participante.asignar_stats_iniciales_participante(stage_data.get("enemigo"))

        stage_data["data_cargada"] = True

def iniciar_data_stage(stage_data: dict):
    """Carga toda la configuración del stage"""
    print("\n=== CARGANDO STAGE ===")
    aux.cargar_configs_stage(stage_data)
    aux.cargar_bd_cartas(stage_data)
    generar_mazo(stage_data)
    barajar_mazos_stage(stage_data)
    print("Stage inicializado\n")

def is_critic() -> bool:
    """50% de probabilidad de crítico"""
    return rd.choice([True, False])

def calcular_ataque_con_bonus(carta_jugada: dict) -> int:
    """Calcula el ataque aplicando bonus"""
    atk_base = carta.get_atk_carta(carta_jugada)
    bonus = carta.get_bonus_carta(carta_jugada)
    
    # Validar que bonus no sea None
    if bonus is None:
        bonus = 0
    
    porcentaje_bonus = bonus
    atk_con_bonus = atk_base * (1 + porcentaje_bonus / 100)
    return int(atk_con_bonus)

def calcular_puntos_mano(carta_ganadora: dict, carta_perdedora: dict) -> int:
    """Calcula puntos: Ataque ganador - Defensa perdedor"""
    atk_ganador = calcular_ataque_con_bonus(carta_ganadora)
    def_perdedor = carta.get_def_carta(carta_perdedora)
    puntos = max(atk_ganador - def_perdedor, 100)
    return puntos

def jugar_mano(stage_data: dict):
    """Juega una mano completa"""
    jugador = stage_data["jugador"]
    enemigo = stage_data["enemigo"]
    
    print("\n=== JUGANDO MANO ===")
    
    # Ambos juegan carta
    jugador_jugo = participante.jugar_carta(jugador)
    enemigo_jugo = participante.jugar_carta(enemigo)
    
    if not jugador_jugo or not enemigo_jugo:
        print("No hay suficientes cartas")
        return None
    
    # INCREMENTAR CONTADOR DE MANOS
    stage_data["manos_jugadas"] = stage_data.get("manos_jugadas", 0) + 1
    
    # Obtener cartas jugadas
    carta_jugador = participante.get_carta_actual_participante(jugador)
    carta_enemigo = participante.get_carta_actual_participante(enemigo)
    
    # Calcular ataques CON bonus
    atk_jugador = calcular_ataque_con_bonus(carta_jugador)
    atk_enemigo = calcular_ataque_con_bonus(carta_enemigo)
    
    print(f"Ataque Jugador (con bonus): {atk_jugador}")
    print(f"Ataque Enemigo (con bonus): {atk_enemigo}")
    
    # Determinar ganador
    ganador = None
    perdedor = None
    carta_ganadora = None
    carta_perdedora = None
    es_empate = False
    es_critico = False
    
    if atk_jugador > atk_enemigo:
        ganador = jugador
        perdedor = enemigo
        carta_ganadora = carta_jugador
        carta_perdedora = carta_enemigo
        print("JUGADOR GANA LA MANO")
    elif atk_enemigo > atk_jugador:
        ganador = enemigo
        perdedor = jugador
        carta_ganadora = carta_enemigo
        carta_perdedora = carta_jugador
        print("ENEMIGO GANA LA MANO")
    else:
        print("EMPATE")
        es_empate = True
        es_critico = is_critic()
        participante.restar_stats_participante(jugador, carta_jugador, es_critico)
        participante.restar_stats_participante(enemigo, carta_enemigo, es_critico)
        return {"ganador": None, "empate": True, "critico": es_critico}
    
    # Aplicar daño (considerar SHIELD)
    if perdedor == jugador and stage_data.get("shield_applied"):
        print("¡SHIELD! Daño rebota al enemigo")
        stage_data["shield_applied"] = False
        es_critico = is_critic()
        participante.restar_stats_participante(enemigo, carta_enemigo, es_critico)
        puntos = calcular_puntos_mano(carta_ganadora, carta_perdedora)
        participante.add_score_participante(jugador, puntos)
    else:
        es_critico = is_critic()
        participante.restar_stats_participante(perdedor, carta_perdedora, es_critico)
        
        if ganador == jugador:
            puntos = calcular_puntos_mano(carta_ganadora, carta_perdedora)
            participante.add_score_participante(jugador, puntos)
    
    return {
        "ganador": ganador,
        "perdedor": perdedor,
        "carta_ganadora": carta_ganadora,
        "carta_perdedora": carta_perdedora,
        "empate": es_empate,
        "critico": es_critico
    }

def chequear_condiciones_victoria(stage_data: dict) -> str:
    """Evalúa el ganador."""

    if stage_data.get("manos_jugadas", 0) == 0:
        return None
    
    jugador = stage_data.get("jugador")
    enemigo = stage_data.get("enemigo")
    
    hp_jugador = participante.get_hp_participante(jugador)
    hp_enemigo = participante.get_hp_participante(enemigo)
    
    if hp_jugador <= 0:
        print("Jugador HP = 0 - DERROTA")
        return "enemigo"
    if hp_enemigo <= 0:
        print("Enemigo HP = 0 - VICTORIA")
        return "jugador"

    # Si ambos se quedaron sin cartas, gana quien tiene más HP
    sin_cartas_jugador = not participante.tiene_cartas(jugador)
    sin_cartas_enemigo = not participante.tiene_cartas(enemigo)
    if sin_cartas_jugador and sin_cartas_enemigo:
        if hp_jugador > hp_enemigo:
            print("Sin cartas - Jugador gana por HP")
            return "jugador"
        elif hp_enemigo > hp_jugador:
            print("Sin cartas - Enemigo gana por HP")
            return "enemigo"
        else:
            print("Sin cartas - Empate, gana enemigo")
            return "enemigo"

def esta_finalizado(stage_data: dict) -> bool:
    return stage_data.get('juego_finalizado', False)

def obtener_ganador(stage_data: dict):
    return stage_data.get('ganador')

def setear_ganador(stage_data: dict, ganador_participante: dict):
    stage_data["ganador"] = ganador_participante
    stage_data["juego_finalizado"] = True
    print(f"GANADOR: {participante.get_nombre_participante(ganador_participante)}")

def draw_jugadores(stage_data: dict):
    """Dibuja ambos participantes"""
    participante.draw_participante(stage_data.get("jugador"), stage_data.get("screen"))
    participante.draw_participante(stage_data.get("enemigo"), stage_data.get("screen"))

def update(stage_data: dict):
    pass