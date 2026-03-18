import pygame as py
import modules.variables as var
import modules.forms.form_base as form_base
from utn_fra.pygame_widgets import Label, Button

# Rutas de las imágenes
RUTAS = [
    "assets/img/forms/FORM_TUTORIAL/stage.png",
    "assets/img/forms/FORM_TUTORIAL/wish.png",
    "assets/img/forms/FORM_TUTORIAL/shield_activo.png",
    "assets/img/forms/FORM_TUTORIAL/victoria.png",
    "assets/img/forms/FORM_TUTORIAL/ranking.png",
]

textos = [
    {
        "imagen": py.image.load(RUTAS[0]),
        "texto": "CADA JUGADOR JUEGA UNA MANO AL PRESIONAR EL BOTON JUGAR MANO, DETERMINANDO EL GANADOR DE LA MANO"
    },
    {
        "imagen": py.image.load(RUTAS[1]),
        "texto": "EL JUGADOR CONTARA CON DOS COMODINES: SHIELD(EFECTO ESPEJO REBOTIN) Y HEAL (RESTAURA EL HP PERDIDO)"
    },
    {
        "imagen": py.image.load(RUTAS[2]),
        "texto": "MIENTRAS QUE EL COMODIN SHIELD ESTE ACTIVO SE MOSTRARA UN ICONO EN PANTALLA"
    },
    {
        "imagen": py.image.load(RUTAS[3]),
        "texto": "UNA VEZ FINALIZADO EL JUEGO, PODREMOS INGRESAR NUESTRO NOMBRE"
    },
    {
        "imagen": py.image.load(RUTAS[4]),
        "texto": "EL NOMBRE INGRESADO SE GUARDARA EN EL RANKING JUNTO CON EL SCORE, MOSTRANDO LOS 10 MEJORES"
    },
]
# Tamaño de la imagen en pantalla
IMAGEN_W = 500
IMAGEN_H = 280

indice = 0


def crear_form_tutorial(dict_form_data: dict) -> dict:
    global indice
    indice = 0  # Reiniciamos al abrir el form

    form = form_base.create_form_base(dict_form_data)

    #Título
    form["lbl_titulo"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2,
        y=var.DIMENSION_PANTALLA[1] // 8,
        text="TUTORIAL",
        screen=form.get("screen"),
        font_path=var.FONT_SAIYAN_SANS,
        font_size=45,
        color=py.Color("red")
    )

    #Texto descriptivo
    form["lbl_texto"] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2,
        y=posicion_imagen() + IMAGEN_H - 310,
        text=textos[indice]["texto"],
        screen=form.get("screen"),
        font_path=var.FONT_ALAGARD,
        font_size=15,
        color=py.Color("black")
    )

    #Botón PREV
    form["btn_prev"] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 - 290,
        y=posicion_imagen() + IMAGEN_H // 2,
        text="PREV",
        screen=form.get("screen"),
        font_path=var.FONT_SAIYAN_SANS,
        font_size=28,
        on_click=imagen_anterior,
        on_click_param=form
    )

    # Botón NEX
    form["btn_next"] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 + 300,
        y=posicion_imagen() + IMAGEN_H // 2,
        text="NEXT",
        screen=form.get("screen"),
        font_path=var.FONT_SAIYAN_SANS,
        font_size=28,
        on_click=imagen_siguiente,
        on_click_param=form
    )

    #Botón VOLVER
    form["btn_volver"] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2,
        y=var.DIMENSION_PANTALLA[1] - 70,
        text="VOLVER",
        screen=form.get("screen"),
        font_path=var.FONT_SAIYAN_SANS,
        font_size=38,
        on_click=form_base.set_active,
        on_click_param="form_menu"
    )

    form["widgets_list"] = [
        form.get("lbl_titulo"),
        form.get("lbl_texto"),
        form.get("btn_prev"),
        form.get("btn_next"),
        form.get("btn_volver"),
    ]

    var.dict_forms_status[form.get("name")] = form
    return form



def posicion_imagen() -> int:
    return var.DIMENSION_PANTALLA[1] // 4

def actualizar_labels(form: dict):
    """Actualiza el texto del label descriptivo"""
    form["lbl_texto"].update_text(textos[indice]["texto"], color=py.Color("black"))

def imagen_siguiente(form: dict):
    global indice
    indice = (indice + 1) % len(textos)
    actualizar_labels(form)

def imagen_anterior(form: dict):
    global indice
    indice = (indice - 1) % len(textos)
    actualizar_labels(form)


def draw_image(screen: py.Surface):
    cx   = var.DIMENSION_PANTALLA[0] // 2
    y    = posicion_imagen()
    rect = py.Rect(cx - IMAGEN_W // 2, y, IMAGEN_W, IMAGEN_H)

    img_escalada = py.transform.scale(textos[indice]["imagen"], (IMAGEN_W, IMAGEN_H))
    screen.blit(img_escalada, rect.topleft)

def draw(form_dict_data: dict):
    form_base.draw(form_dict_data)
    draw_image(form_dict_data.get("screen"))
    for widget in form_dict_data.get("widgets_list", []):
        widget.draw()

def update(form_dict_data: dict):
    form_base.update(form_dict_data)

    for widget in form_dict_data.get("widgets_list", []):
        widget.update()