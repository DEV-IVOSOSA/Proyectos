import pygame as py
import sys
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import (
    Label, ButtonSound
)
import modules.variables as var
import modules.forms.form_stage as form_stage
import modules.forms.form_controller as form_controller
import modules.participante_juego as participante

def create_form_wish(dict_form_data: dict) -> dict:

    form = form_base.create_form_base(dict_form_data)

    form["jugador"] = dict_form_data.get("jugador")
    form["wish_type"] = ""


    form["lbl_titulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=150,
        text= "ELIGE TU DESEO", screen= form.get("screen"), 
        font_path = var.FONT_SAIYAN_SANS, font_size = 35, color = py.Color('cyan')
    )
    
    form["lbl_subtitulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=210,
        text= "Selecciona el deseo", screen= form.get("screen"), 
        font_path = var.FONT_SAIYAN_SANS, font_size = 35, color = py.Color('cyan')
    )

    form['btn_wish'] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 300,
        text = 'WISH', screen = form.get('screen'),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.OUTRO_WISH,
        on_click = init_wish, on_click_param = form
    )

    form['btn_cancel'] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 380,
        text = 'CANCEL', screen = form.get('screen'),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = click_resume, on_click_param = "form_stage"
    )

    form["widgets_list"] = [
        form.get("lbl_titulo"),
        form.get("lbl_subtitulo"),
        form.get("btn_wish"),
        form.get("btn_cancel")
    ]
    
    var.dict_forms_status[form.get("name")] = form

    return form

def update_wish_type(dict_form_data: dict, wish_type: str):
    dict_form_data["wish_type"] = wish_type
    dict_form_data.get("widgets_list")[2].update_text(text=wish_type, color=py.Color("green"))
    try:
        intro_sound = py.mixer.Sound(var.INTRO_WISH)
        intro_sound.play()
    except Exception as e:
        print(f"No se pudo reproducir INTRO_WISH: {e}")

def click_resume(form_name: str):
    form_base.cambiar_pantalla(form_name)

def init_wish(form_dict_data: dict):
    wish_type = form_dict_data.get("wish_type")
    jugador = form_dict_data.get("jugador")
    stage_form = var.dict_forms_status.get("form_stage")

    if wish_type == "HEAL":
        hp_recuperado = participante.get_hp_inicial_participante(jugador)
        hp_actual = participante.get_hp_participante(jugador)
        print(f"ANTERIOR HP: {hp_actual} | HP RECUPERADO: {hp_recuperado}")
        participante.set_hp_participante(jugador, hp_recuperado)
        if stage_form:
            stage_form["stage"]["heal_available"] = False
    elif wish_type == "SHIELD":
        if stage_form:
            stage_form["stage"]["shield_applied"] = True
            stage_form["stage"]["shield_available"] = False
            print("SHIELD activado: el próximo daño rebotará al enemigo")
    click_resume("form_stage")

def update(form_dict_data: dict):
    form_base.update(form_dict_data)

def draw(form_dict_data: dict):
    form_base.draw(form_dict_data)
    form_base.draw_widgets(form_dict_data)