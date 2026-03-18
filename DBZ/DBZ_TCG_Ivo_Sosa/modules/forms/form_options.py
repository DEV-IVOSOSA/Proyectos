
import pygame as py
import sys
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import (
    Label, ButtonSound
)
import modules.variables as var
import modules.sonido as sonido

def create_form_options(dict_form_data: dict) -> dict:
    form = form_base.create_form_base(dict_form_data)

    form["lbl_titulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text= "OPTIONS", screen= form.get("screen"),
        font_path = var.FONT_SAIYAN_SANS, font_size = 45, color = py.Color("blue")

    )

    form["btn_music_on"] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 150,
        text = "MUSIC ON", screen = form.get("screen"),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = activar_musica, on_click_param = form
    )

    form["btn_music_off"] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2, y = 200,
        text = "MUSIC OFF", screen = form.get("screen"),
        font_path = var.FONT_SAIYAN_SANS, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = desactivar_musica, on_click_param = form
    )

    form["btn_volver"] = ButtonSound(
        x= var.DIMENSION_PANTALLA[0] // 2, y=500,
        text= "VOLVER", screen=form.get("screen"),
        font_path= var.FONT_SAIYAN_SANS, font_size= 40, sound_path= var.CLICK_SOUND,
        on_click= cambiar_pantalla, on_click_param= "form_menu"
    )

    form["btn_vol_down"] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2 - 150, y = 320,
        text = "<", screen = form.get("screen"),
        font_path = var.FONT_ALAGARD, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = modificar_volumen, on_click_param = (-10)
    )

    form["btn_vol_up"] = ButtonSound(
        x = var.DIMENSION_PANTALLA[0] // 2 + 150, y = 320,
        text = ">", screen = form.get("screen"),
        font_path = var.FONT_ALAGARD, font_size = 30, sound_path= var.CLICK_SOUND,
        on_click = modificar_volumen, on_click_param = 10
    )

    form["lbl_vol"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=320,
        text= f"{sonido.get_actual_volume()}", screen= form.get("screen"), 
        font_path = var.FONT_ALAGARD, font_size = 45, color = py.Color("red")

    )

    form["widgets_list"] = [
        form.get("lbl_titulo"),
        form.get("btn_music_on"),
        form.get("btn_music_off"),
        form.get("btn_volver"),
        form.get("btn_vol_down"),
        form.get("btn_vol_up"),
        form.get("lbl_vol")
    ]

    var.dict_forms_status[form.get("name")] = form

    return form

def modificar_volumen(volumen: int):
    vol_actual = sonido.get_actual_volume()
    if vol_actual > 0 and volumen < 0 or\
        vol_actual < 100 and volumen > 0:
        vol_actual += volumen
        sonido.set_volume(vol_actual)

def activar_musica(form_dict_data: dict):
    form_dict_data["music_config"]["music_on"] = True
    form_base.music_on(form_dict_data)

def desactivar_musica(form_dict_data: dict):
    form_dict_data["music_config"]["music_on"] = False
    sonido.stop_music()

def cambiar_pantalla(form_name: str):
    form_base.set_active(form_name)

def draw(form_dict_data: dict):
    form_base.draw(form_dict_data)
    form_base.draw_widgets(form_dict_data)

def update(form_dict_data: dict):
    
    lbl_vol: Label = form_dict_data.get("widgets_list")[6]
    lbl_vol.update_text(text=f"{sonido.get_actual_volume()}",color= py.Color("red"))
    form_base.update(form_dict_data)