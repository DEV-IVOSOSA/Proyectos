import pygame as py
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import (
    Label, ButtonSound, TextBox
)
import modules.variables as var
import modules.participante_juego as participante
import modules.auxiliar as aux

def create_form_name(dict_form_data: dict) -> dict:

    form = form_base.create_form_base(dict_form_data)
     
    form["jugador"] = dict_form_data.get("jugador")
    form["info_submitida"] = False
    form["win_status"] = True  # por defecto victoria

    form["lbl_titulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=100,
        text="¡VICTORIA!", screen=form.get("screen"), 
        font_path=var.FONT_SAIYAN_SANS, font_size=35, color=py.Color('cyan')
    )

    form["lbl_subtitulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=150,
        text="Escriba su nombre", screen=form.get("screen"), 
        font_path=var.FONT_SAIYAN_SANS, font_size=35, color=py.Color('cyan')
    )

    form["lbl_score"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=210,
        text=f"SCORE: {participante.get_score_participante(form.get('jugador'))}",
        screen=form.get("screen"), 
        font_path=var.FONT_ALAGARD, font_size=35, color=py.Color('cyan')
    )

    form["lbl_nombre_texto"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=300,
        text="", screen=form.get("screen"), 
        font_path=var.FONT_ALAGARD, font_size=35, color=py.Color('white')
    )

    form['btn_submit'] = ButtonSound(
        x=var.DIMENSION_PANTALLA[0] // 2, y=400,
        text="CONFIRMAR NOMBRE", screen=form.get('screen'),
        font_path=var.FONT_SAIYAN_SANS, font_size=30, sound_path=var.CLICK_SOUND,
        on_click=submit_name, on_click_param=form
    )

    form["text_box"] = TextBox(
        x=var.DIMENSION_PANTALLA[0] // 2, y=310, text="_________________",
        screen=form.get("screen"), 
        font_path=var.FONT_ALAGARD, font_size=25, color=py.Color('orange')
    )

    form["widgets_list"] = [
        form.get("lbl_titulo"),        
        form.get("lbl_subtitulo"),     
        form.get("lbl_score"),         
        form.get("lbl_nombre_texto"),  
        form.get("btn_submit")         
    ]

    var.dict_forms_status[form.get("name")] = form

    return form


def configurar_resultado(form_dict_data: dict, win_status: bool):
    """Configura fondo, música y título según victoria o derrota."""
    form_dict_data["win_status"] = win_status

    if win_status:
        titulo = "¡VICTORIA!"
        nuevo_fondo = var.FONDO_NAME_VICTORY
        nueva_musica = var.MUSICA_NAME_VICTORY
    else:
        titulo = "DERROTA"
        nuevo_fondo = var.FONDO_NAME_DEFEAT
        nueva_musica = var.MUSICA_NAME_DEFEAT

    # Actualizar título
    form_dict_data.get("widgets_list")[0].update_text(titulo, py.Color("cyan"))


    try:
        nueva_superficie = py.image.load(nuevo_fondo).convert_alpha()
        nueva_superficie = py.transform.scale(nueva_superficie, var.DIMENSION_PANTALLA)
        form_dict_data["surface"] = nueva_superficie
    except Exception as e:
        print(f"No se pudo cargar el fondo. '{nuevo_fondo}': {e}")


    form_dict_data["music_path"] = nueva_musica


def submit_name(form_data: dict):
    jugador = form_data.get("jugador")
    nombre_jugador = form_data.get("text_box").writing
    participante.set_nombre_participante(jugador, nombre_jugador)
    nombre_jugador_seteado = participante.get_nombre_participante(jugador)
    puntaje_jugador = participante.get_score_participante(jugador)

    print(f"NOMBRE JUGADOR: {nombre_jugador_seteado} - {puntaje_jugador}")
    aux.guardar_puntaje(var.RANKING_CSV, nombre_jugador_seteado, puntaje_jugador)
    form_data["info_submitida"] = True

    form_base.set_active("form_ranking")


def update(form_dict_data: dict, event_list: list[py.event.Event]):
    score = participante.get_score_participante(form_dict_data.get("jugador"))

    form_dict_data.get("widgets_list")[2].update_text(
        text=f"SCORE: {score}", color=py.Color("white")
    )
    form_dict_data.get("widgets_list")[3].update_text(
        text=f"{form_dict_data.get('text_box').writing.upper()}", color=py.Color("white")
    )
    
    form_dict_data.get("text_box").update(event_list)
    form_base.update(form_dict_data)


def draw(form_dict_data: dict):
    form_base.draw(form_dict_data)
    form_dict_data.get("text_box").draw()
    form_base.draw_widgets(form_dict_data)