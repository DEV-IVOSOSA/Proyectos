import pygame as py
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import Label, ButtonImageSound, TextBoxSound
import modules.forms.form_pause as form_pause
import modules.variables as var
import modules.stage as stage
import modules.participante_juego as participante
import modules.forms.form_wish as form_wish
import modules.auxiliar as aux

def crear_form_stage(dict_form_data: dict):
    form = form_base.create_form_base(dict_form_data)

    form["restart_stage"] = False
    form["time_finished"] = False 
    form["actual_level"] = 1
    form["stage_timer"] = var.STAGE_TIMER
    form["last_timer"] = py.time.get_ticks()

    form["bonus_shield_available"] = True
    form["bonus_heal_available"] = True
    form["jugador"] = dict_form_data.get("jugador")

    form["stage"] = stage.inicializar_stage(
        jugador=form.get("jugador"), 
        pantalla=form.get("screen"), 
        nro_stage=form.get("actual_level")
    )
    form["partida_iniciada"] = False
    form["juego_terminado"] = False

    form["btn_jugar_mano"] = ButtonImageSound(
        x=var.DIMENSION_PANTALLA[0] // 2 + 395, y=var.DIMENSION_PANTALLA[1] // 2 + 20,
        width= 80, height= 40, text="JUGAR MANO", screen=form.get("screen"),
        image_path= var.BOTON_PLAY_HAND, sound_path= var.CLICK_SOUND,
        on_click=jugar_mano, on_click_param= form
    )

    # LABELS PARTIDA    
    form["clock"] = py.time.Clock()

    form["lbl_timer"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2 - 420, y=var.DIMENSION_PANTALLA[0] // 2 - 430,
        screen=form.get("screen"), text= "",
        align="topleft", font_path=var.FONT_ALAGARD, font_size=20
    )

    form["lbl_score"] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2 - 420, y= var.DIMENSION_PANTALLA[0] // 2 - 400, 
        screen=form.get("screen"), text= "", font_size= 20,
        align="topleft", font_path=var.FONT_ALAGARD
    )
    
    form["lbl_mensaje"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2 - 350, y=var.DIMENSION_PANTALLA[1] // 2,
        text="", screen=form.get("screen"),
        font_path=var.FONT_SAIYAN_SANS, font_size= 20
    )

    form["lbl_golpe_critico"] = TextBoxSound(
        x=var.DIMENSION_PANTALLA[0] // 2 - 350, y=var.DIMENSION_PANTALLA[1] // 2,
        text="GOLPE CRITICO", sound_path= "assets/audio/sounds/critical_hit.ogg", screen=form.get("screen"),
        font_path=var.FONT_SAIYAN_SANS, font_size= 20
    )
    
    # CARTAS
    form["lbl_carta_e"] = Label(
        x=390, y=275,
        text=f"", screen=form.get("screen"),
        align="topleft", font_path=var.FONT_ALAGARD, font_size=20,
    )

    form["lbl_carta_p"] = Label(
        x=390, y=440,
        text=f"", screen=form.get("screen"),
        align="topleft", font_path=var.FONT_ALAGARD, font_size=20,
    )

    # LABELS ENEMIGO
    form["lbl_enemigo_hp"] = Label(
        x=120, y=160, text=f"HP: 0",
        screen=form.get("screen"),
        font_path=var.FONT_ALAGARD, font_size=15
    )

    form["lbl_enemigo_atk"] = Label(
        x=120, y=180, text=f"ATK: 0",
        screen=form.get("screen"),
        font_path=var.FONT_ALAGARD, font_size=15
    )

    form["lbl_enemigo_def"] = Label(
        x=120, y=200, text=f"DEF: 0",
        screen=form.get("screen"),
        font_path=var.FONT_ALAGARD, font_size=15
    )

    # LABELS JUGADOR
    form["lbl_jugador_hp"] = Label(
        x=120, y=430, text="HP: 0",
        screen=form.get("screen"),
        font_path=var.FONT_ALAGARD, font_size=15
    )

    form["lbl_jugador_atk"] = Label(
        x=120, y=450, text="ATK: 0",
        screen=form.get("screen"),
        font_path=var.FONT_ALAGARD, font_size=15
    )

    form["lbl_jugador_def"] = Label(
        x=120, y=470, text="DEF: 0",
        screen=form.get("screen"),
        font_path=var.FONT_ALAGARD, font_size=15
    )
    
    # COMODINES
    form["btn_heal"] = ButtonImageSound(
        x=var.DIMENSION_PANTALLA[0] // 2 + 360, y=var.DIMENSION_PANTALLA[0] // 2 + 20,
        width= 75, height= 30, text="HEAL", screen= form.get("screen"),
        image_path= var.BOTON_HEAL, sound_path= var.HEAL_ACTIVATED, on_click=call_wish_form, on_click_param={"form": form, "wish": "HEAL"},
        align="topleft"
    )

    form["btn_shield"] = ButtonImageSound(
        x=var.DIMENSION_PANTALLA[0] // 2 + 360, y=var.DIMENSION_PANTALLA[0] // 2 + 60,
        width= 75, height= 30, text="SHIELD", screen=form.get("screen"), image_path= var.BOTON_SHIELD,
        sound_path= var.SHIELD_ACTIVATED,
        on_click=call_wish_form, on_click_param={"form": form, "wish": "SHIELD"},
        align="topleft"
    )

    form["widgets_list"] = [
        form.get("lbl_timer"),
        form.get("lbl_score"),
        form.get("lbl_enemigo_hp"),
        form.get("lbl_enemigo_atk"),
        form.get("lbl_enemigo_def"),
        form.get("lbl_jugador_hp"),
        form.get("lbl_jugador_atk"),
        form.get("lbl_jugador_def"),
        form.get("lbl_carta_e"),
        form.get("lbl_carta_p"),
        form.get("btn_jugar_mano"),

        form.get("lbl_mensaje")
    ]

    form["widgets_list_bonus"] = [
        form.get("btn_heal"),
        form.get("btn_shield")
    ]

    var.dict_forms_status[form.get("name")] = form
    return form

def iniciar_nueva_partida(form_dict_data: dict):
    """Reinicia completamente la partida desde cero"""
    print("=== INICIANDO NUEVA PARTIDA ===")

    form_dict_data["restart_stage"] = False
    form_dict_data["time_finished"] = False 
    form_dict_data["actual_level"] = 1
    form_dict_data["stage_timer"] = var.STAGE_TIMER
    form_dict_data["last_timer"] = py.time.get_ticks()
    
    form_dict_data["bonus_shield_available"] = True
    form_dict_data["bonus_heal_available"] = True
    form_dict_data["juego_terminado"] = False
    
    #form_dict_data["btn_heal"].update_text("HEAL", var.colores.get("cian"))
    #form_dict_data["btn_shield"].update_text("SHIELD", var.colores.get("cian"))
    
    jugador = form_dict_data.get("jugador")
    
    if jugador:
        participante.reiniciar_datos_participante(jugador)
    
    form_dict_data["stage"] = stage.inicializar_stage(
        jugador=jugador, 
        pantalla=form_dict_data.get("screen"), 
        nro_stage=1
    )

    stage.iniciar_data_stage(form_dict_data["stage"])
    
    form_dict_data["partida_iniciada"] = True
    form_dict_data["lbl_mensaje"].update_text("", py.Color("cyan"))
    
    print("¡Partida iniciada! Presiona JUGAR MANO para comenzar")

def usar_heal(form_dict_data: dict):
    """Usa el comodín HEAL"""
    if form_dict_data.get("bonus_heal_available") and not form_dict_data.get("juego_terminado"):
        jugador = form_dict_data.get("stage").get("jugador")
        hp_inicial = participante.get_hp_inicial_participante(jugador)
        hp_actual = participante.get_hp_participante(jugador)
        hp_perdida = hp_inicial - hp_actual
        
        hp_bonus = int(hp_perdida * 0.75)
        nuevo_hp = hp_actual + hp_bonus
        
        participante.set_hp_participante(jugador, nuevo_hp)
        form_dict_data["bonus_heal_available"] = False
        #form_dict_data["btn_heal"].update_text("HEAL (usado)", py.Color("gray"))

def usar_shield(form_dict_data: dict):
    """Usa el comodín SHIELD"""
    if form_dict_data.get("bonus_shield_available") and not form_dict_data.get("juego_terminado"):
        form_dict_data["stage"]["shield_applied"] = True
        form_dict_data["bonus_shield_available"] = False
        #form_dict_data["btn_shield"].update_text("SHIELD (usado)", py.Color("gray"))

def mostrar_mensaje(form_dict_data: dict, texto: str, duracion_ms: int):
    """Muestra un mensaje temporal"""
    form_dict_data["lbl_mensaje"].update_text(texto, py.Color("cyan"))
    form_dict_data["tiempo_mensaje"] = py.time.get_ticks()
    form_dict_data["duracion_mensaje"] = duracion_ms

def jugar_mano(form_dict_data: dict):
    """Ejecuta UNA mano del juego"""
    if form_dict_data.get("juego_terminado"):
        return

    stage_juego = form_dict_data.get("stage")
    jugador = stage_juego.get("jugador")
    enemigo = stage_juego.get("enemigo")
    
    if not participante.tiene_cartas(jugador) or not participante.tiene_cartas(enemigo):
        # Sin cartas -> verificar condiciones igual
        ganador_result = stage.chequear_condiciones_victoria(stage_juego)
        if ganador_result:
            finalizar_juego(form_dict_data, ganador_result)
        return

    # JUGAR LA MANO
    resultado = stage.jugar_mano(stage_juego)
    
    if resultado:
        if resultado.get("empate"):
            mostrar_mensaje(form_dict_data, "EMPATE", 1500)
        elif resultado.get("ganador") == jugador:
            mostrar_mensaje(form_dict_data, "GANASTE LA MANO", 1500)
        else:
            mostrar_mensaje(form_dict_data, "PERDISTE LA MANO", 1500)

    # VERIFICAR SI TERMINÓ
    ganador_result = stage.chequear_condiciones_victoria(stage_juego)
    if ganador_result:
        finalizar_juego(form_dict_data, ganador_result)

def finalizar_juego(form_dict_data: dict, ganador: str):
    """Finaliza el juego"""
    if form_dict_data.get("juego_terminado"):
        return

    form_dict_data["juego_terminado"] = True
    
    stage_juego = form_dict_data.get("stage")
    jugador = stage_juego.get("jugador")
    
    if ganador == "jugador":
        stage.setear_ganador(stage_juego, jugador)
        win_status = True
        print("¡VICTORIA!")
    else:
        stage.setear_ganador(stage_juego, stage_juego.get("enemigo"))
        win_status = False
        print("DERROTA")

    try:
        import modules.forms.form_name as form_name_module
        name_form = var.dict_forms_status.get("form_name")
        if name_form is None:
            print("ERROR")
            return
        form_name_module.configurar_resultado(name_form, win_status)
        form_base.set_active("form_name")
    except Exception as e:
        import traceback
        print(f"ERROR en finalizar_juego: {e}")
        traceback.print_exc()

def events_handler(events: list[py.event.Event], form_dict_data: dict):
    """Maneja eventos"""
    for event in events:
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                form_base.set_active("form_pause")
                pause_form = var.dict_forms_status.get("form_pause")
                form_pause.save_last_vol(pause_form)

def update_score(form_dict_data: dict):
    """Actualiza score"""
    participante_obj = form_dict_data.get("stage").get("jugador")
    score = participante_obj.get("score", 0)
    form_dict_data.get("lbl_score").update_text(
        text=f"SCORE: {score}", 
        color=var.colores.get("verde")
    )

def update_lbls_participante(form_dict_data: dict, tipo_participante: str):
    """Actualiza stats"""
    stage_data = form_dict_data.get("stage")
    participante_obj = stage_data.get(tipo_participante)
    
    if participante_obj:
        form_dict_data[f"lbl_{tipo_participante}_hp"].update_text(
            text=f"HP: {participante_obj.get('hp_actual')}",
            color=var.colores.get("amarillo")
        )
        
        form_dict_data[f"lbl_{tipo_participante}_atk"].update_text(
            text=f"ATK: {participante_obj.get('attack')}",
            color=var.colores.get("amarillo")
        )
        
        form_dict_data[f"lbl_{tipo_participante}_def"].update_text(
            text=f"DEF: {participante_obj.get('defense')}",
            color=var.colores.get("amarillo")
        )

def timer_update(form_dict_data: dict):
    """Actualiza timer"""
    if form_dict_data.get("juego_terminado"):
        return
        
    if form_dict_data.get("stage_timer") > 0:
        tiempo_actual = py.time.get_ticks()
        if tiempo_actual - form_dict_data.get("last_timer") > 1000:
            form_dict_data["stage_timer"] -= 1
            form_dict_data["last_timer"] = tiempo_actual
            form_dict_data["stage"]["stage_timer"] = form_dict_data["stage_timer"]

def call_wish_form(params: dict):
    form_dict_data = params.get("form")
    wish_type = params.get("wish")
    stage_juego = form_dict_data.get("stage")

    clave_disponible = f"{'heal' if wish_type == 'HEAL' else 'shield'}_available"
    if not stage_juego.get(clave_disponible):
        return

    wish_form = var.dict_forms_status.get("form_wish")
    form_wish.update_wish_type(wish_form, wish_type)
    form_base.cambiar_pantalla("form_wish")

def draw_icono_activo(screen: py.Surface, ruta_img: str, x: int, y: int, ancho: int, alto: int):
    """Dibuja un icono de comodín activo"""
    try:
        img = py.image.load(ruta_img).convert_alpha()
        img = py.transform.scale(img, (ancho, alto))
        screen.blit(img, (x, y))
    except Exception as e:
        print(f"No se pudo dibujar icono activo: {e}")

def draw_bonus_widgets(form_dict_data: dict):
    widgets_bonus = form_dict_data.get("widgets_list_bonus")
    stage_data = form_dict_data.get("stage")
    screen = form_dict_data.get("screen")

    # HEAL: botón si disponible, nada si ya se usó
    if stage_data.get("heal_available"):
        widgets_bonus[0].draw()

    # SHIELD: botón si disponible, icono activo en esquina superior derecha, nada si ya se consumió
    if stage_data.get("shield_available"):
        widgets_bonus[1].draw()
    elif stage_data.get("shield_applied"):
        draw_icono_activo(
            screen, var.SHIELD_ACTIVO,
            x=var.DIMENSION_PANTALLA[0] // 2 + 355,
            y=var.DIMENSION_PANTALLA[1] // 2 - 150,
            ancho= 80, alto= 80
        )

def update_bonus_widgets(form_dict_data: dict):
    widgets_bonus = form_dict_data.get("widgets_list_bonus")
    stage_data = form_dict_data.get("stage")

    if stage_data.get("heal_available"):
        widgets_bonus[0].update()
    if stage_data.get("shield_available"):
        widgets_bonus[1].update()

def draw(form_dict_data: dict):
    """Dibuja todo"""
    form_base.draw(form_dict_data)
    
    if form_dict_data.get("partida_iniciada"):
        stage.draw_jugadores(form_dict_data.get("stage"))
    
    form_base.draw_widgets(form_dict_data)
    draw_bonus_widgets(form_dict_data)

def update(form_dict_data: dict, eventos: list[py.event.Event]):
    """Actualiza el juego"""
    
    if not form_dict_data.get("partida_iniciada"):
        iniciar_nueva_partida(form_dict_data)
        return

    if form_dict_data.get("juego_terminado"):
        return

    timer_update(form_dict_data)
    form_dict_data["lbl_timer"].update_text(
        f"TIME LEFT: {form_dict_data.get('stage_timer')}", 
        var.colores.get("blanco")
    )
    
    if form_dict_data.get("stage_timer") <= 0 and not form_dict_data.get("juego_terminado"):
        finalizar_juego(form_dict_data, "enemigo")
    
    events_handler(eventos, form_dict_data)

    if not form_dict_data.get("juego_terminado"):
        ganador_result = stage.chequear_condiciones_victoria(form_dict_data.get("stage"))
        if ganador_result:
            finalizar_juego(form_dict_data, ganador_result)
            return
    
    update_lbls_participante(form_dict_data, tipo_participante="jugador")
    update_lbls_participante(form_dict_data, tipo_participante="enemigo")
    update_score(form_dict_data)
    update_bonus_widgets(form_dict_data)
    
    if "tiempo_mensaje" in form_dict_data:
        if py.time.get_ticks() - form_dict_data["tiempo_mensaje"] > form_dict_data.get("duracion_mensaje", 2000):
            form_dict_data["lbl_mensaje"].update_text("", py.Color("cyan"))
    
    form_base.update(form_dict_data)