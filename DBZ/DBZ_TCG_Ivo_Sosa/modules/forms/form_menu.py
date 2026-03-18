import pygame as py
import sys
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import (
    Label, ButtonSound
)
import modules.variables as var
import modules.forms.form_stage as form_stage
import modules.forms.form_controller as form_controller

def create_form_menu(dict_form_data: dict) -> dict:

    form = form_base.create_form_base(dict_form_data)
     
    form["lbl_subtitulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=150,
        text= "Menu principal", screen= form.get("screen"), 
        font_path = var.FONT_SAIYAN_SANS, font_size = 35, color = py.Color('cyan')

    )

    form["lbl_titulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text= "Dragon Ball Trading Card", screen= form.get("screen"), 
        font_path = var.FONT_SAIYAN_SANS, font_size = 40, color = py.Color('cyan')

    )

    form['btn_play'] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 300,
        text = 'JUGAR', screen = form.get('screen'),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = iniciar_stage, on_click_param = "form_stage"
    )

    form['btn_tutorial'] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 350,
        text = 'TUTORIAL', screen = form.get('screen'),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = form_base.cambiar_pantalla, on_click_param = "form_tutorial"
    )

    form['btn_ranking'] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 450,
        text = 'RANKING', screen = form.get('screen'),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = form_base.cambiar_pantalla, on_click_param = "form_ranking"
    )
    
    form['btn_options'] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 400,
        text = 'OPCIONES', screen = form.get('screen'),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = form_base.cambiar_pantalla, on_click_param = "form_options"
    )

    form ["btn_exit"] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 500,
        text = "Salir", screen=form.get("screen"),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = salir_juego, on_click_param = None
    )

    form["widgets_list"] = [
    form.get("lbl_titulo"),
    form.get("lbl_subtitulo"),
    form.get("btn_play"),
    form.get("btn_ranking"),
    form.get("btn_options"),
    form.get("btn_exit"),
    form.get("btn_tutorial")
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def iniciar_stage(form_name: str):
    form_base.cambiar_pantalla(form_name)
    stage_form = var.dict_forms_status.get(form_name)
    form_stage.iniciar_nueva_partida(stage_form)

def salir_juego(_):
    print("Saliendo del juego desde el boton.")
    py.quit()
    sys.exit()


def draw(dict_form_data: dict):
    form_base.draw(dict_form_data)
    form_base.draw_widgets(dict_form_data)

def events_handler():
    events = py.event.get()
    for event in events:
        if event.type == py.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(f"Coordenada mouse: X={x} | Y = {y}")
        if event.type == py.QUIT:
            salir_juego()

def update(dict_form_data: dict):
    events_handler()
    form_base.update(dict_form_data)
    if not dict_form_data.get("music_config").get("music_init"):
        form_base.music_on(dict_form_data)
        dict_form_data["music_config"]["music_init"] = True
