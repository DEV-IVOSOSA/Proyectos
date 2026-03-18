import pygame as py
import sys
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var
import modules.auxiliar as aux


def create_form_ranking(dict_form_data: dict) -> dict:
    form = form_base.create_form_base(dict_form_data)

    form["lista_ranking_file"] = []

    form["lista_ranking_screen"] = []

    form["data_loaded"] = False

    form["lbl_subtitulo"] = Label(
        x= var.DIMENSION_PANTALLA[0] // 2, y=90,
        text= "TOP TEN Ranking", screen=form.get("screen"),
        font_path= var.FONT_SAIYAN_SANS, font_size= 50, color= py.Color("orange")
    )

    form["btn_volver"] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2, y=520,
        text= "VOLVER", screen=form.get("screen"),
        font_path= var.FONT_SAIYAN_SANS, font_size= 40,
        on_click= cambiar_pantalla, on_click_param= [form, "form_menu"]
    )

    form["widgets_list"] = [
        form.get("lbl_subtitulo"),
        form.get("btn_volver")
    ]

    var.dict_forms_status[form.get("name")] = form

    return form

def cambiar_pantalla(param_list: list):
    form_ranking= param_list[0]
    form_name= param_list[1]

    print("Saliendo del formulario Ranking")
    form_ranking["data_loaded"] = False
    form_ranking["lista_ranking_screen"]=[]
    form_base.cambiar_pantalla(form_name)

def init_ranking_data(form_dict_data):
    matriz = form_dict_data.get("lista_ranking_file")
    y_coord_inicial = 50

    for indice_fila in range(len(matriz)):
        fila= matriz[indice_fila]
        color_texto = py.Color("cyan")
        
        if indice_fila > 0:
            color_texto = py.Color("red")

        posicion= Label(
            x=var.DIMENSION_PANTALLA[0] // 2 - 120, y=y_coord_inicial + 100,
            text = f"{indice_fila + 1}", screen= form_dict_data.get("screen"),
            font_size=15, font_path= var.FONT_ALAGARD, color=color_texto
        )

        nombre= Label(
            x=var.DIMENSION_PANTALLA[0] // 2 - 10, y = y_coord_inicial + 100,
            text = f"{fila[0]}", screen= form_dict_data.get("screen"),
            font_size = 15, font_path= var.FONT_ALAGARD, color=color_texto
        )

        puntaje=  Label(
            x=var.DIMENSION_PANTALLA[0] // 2 + 120, y= y_coord_inicial + 100,
            text = f"{fila[1]}", screen= form_dict_data.get("screen"),
            font_size=15, font_path= var.FONT_ALAGARD, color=color_texto
        )

        y_coord_inicial += 42   
        form_dict_data["lista_ranking_screen"].append(posicion)
        form_dict_data["lista_ranking_screen"].append(nombre)
        form_dict_data["lista_ranking_screen"].append(puntaje)


def iniciar_ranking_archivo(form_dict_data: dict):
    form_dict_data["lista_ranking_file"] = aux.cargar_ranking(var.RANKING_CSV, top=10)
    init_ranking_data(form_dict_data)
    
    if not form_dict_data.get("data_loaded"):
        form_dict_data["lista_ranking_file"]= aux.cargar_ranking(file_path= "puntajes.csv", top=10)
        init_ranking_data(form_dict_data)
        form_dict_data["data_loaded"] = True
    

def draw(form_dict_data: dict):
    form_base.draw(form_dict_data)
    form_base.draw_widgets(form_dict_data)
    # widgets lbl ranking
    for widget in form_dict_data.get("lista_ranking_screen"):
        widget.draw()

def update(form_dict_data: dict):

    if not form_dict_data.get("data_loaded"):
        iniciar_ranking_archivo(form_dict_data)

    form_base.update(form_dict_data)
