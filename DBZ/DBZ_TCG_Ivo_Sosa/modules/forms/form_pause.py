import pygame as py
import sys
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import (
    Label, ButtonSound
)
import modules.variables as var
import modules.sonido as sonido
import modules.forms.form_stage as form_stage

def create_form_pause(dict_form_data: dict) -> dict:
    form = form_base.create_form_base(dict_form_data)

    form["last_volume"] = None

    form["lbl_titulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text= var.TITULO_JUEGO, screen= form.get("screen"), 
        font_path = var.FONT_SAIYAN_SANS, font_size = 45, color = py.Color("blue")
    )

    form["lbl_subtitulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=160,
        text= "PAUSE", screen= form.get("screen"), 
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, color = py.Color("blue")
    )
    
    form["btn_resume"] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 400,
        text = "RESUME", screen = form.get("screen"),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = cambiar_pantalla,
        on_click_param = {"form": form, "form_name": "form_stage"}, color = py.Color("cyan")
    )

    form["btn_restart"] = ButtonSound(
        x=var.DIMENSION_PANTALLA[0] // 2, y=270,
        text="RESTART STAGE", screen=form.get("screen"),
        font_path=var.FONT_SAIYAN_SANS, font_size= 30, sound_path= var.CLICK_SOUND,
        on_click=restart_stage, 
        on_click_param={"form": form, "form_name": "form_stage"}, color = py.Color("cyan")
    )

    form["btn_back"] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 330,
        text = "BACK TO MENU", screen = form.get("screen"),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = form_base.cambiar_pantalla, on_click_param = "form_menu", color = py.Color("cyan")
    )

    form["widgets_list"] = [
        form.get("lbl_titulo"),
        form.get("lbl_subtitulo"),
        form.get("btn_resume"),
        form.get("btn_restart"),
        form.get("btn_back")
    ]

    var.dict_forms_status[form.get("name")] = form 

    return form

def cambiar_pantalla(params: dict):
    last_vol = params.get("form").get("last_volume")
    form_base.cambiar_pantalla(params.get("form_name"))
    set_last_vol(last_vol)

def set_last_vol(vol: int):
    if vol is not None:
        sonido.set_volume(vol)

def save_last_vol(form_dict_data: dict):
    form_dict_data["last_volume"] = sonido.get_actual_volume()
    set_last_vol(10)

def restart_stage(params: dict):
    """Reinicia el stage completamente"""
    stage_form = var.dict_forms_status.get(params.get("form_name"))
    
    # Cambiar a la pantalla del stage
    cambiar_pantalla(params)
    
    # Reiniciar la partida completamente
    form_stage.iniciar_nueva_partida(stage_form)
    
    print("Stage reiniciado desde el menú de pausa")

def draw(form_dict_data: dict):
    form_base.draw(form_dict_data)
    form_base.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    form_base.update(form_dict_data)