import pygame as py
import modules.variables as var
import modules.forms.form_menu as form_menu
import modules.forms.form_ranking as form_ranking
import modules.forms.form_options as form_options
import modules.forms.form_pause as form_pause
import modules.forms.form_stage as form_stage
import modules.forms.form_tutorial as form_tutorial
import modules.forms.form_name as form_name
import modules.forms.form_wish as form_wish

def create_form_controller(screen: py.Surface, datos_juego: dict):
    controller = {}
    
    controller["main_screen"] = screen 
    controller["current_stage"] = 1
    controller["game_started"] = False
    controller["player"] = datos_juego.get("player") 
    controller["music_config"] = datos_juego.get("music_config")
    controller["forms_list"] =  [
        form_menu.create_form_menu(
            {
                "name": "form_menu",
                "screen": controller.get("main_screen"),
                "active": True,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_MENU,
                "music_path": var.MUSICA_MENU,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config")
            }
        ),
        form_ranking.create_form_ranking(
            {
                "name": "form_ranking",
                "screen": controller.get("main_screen"),
                "active": False,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_RANKING,
                "music_path": var.MUSICA_RANKING,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config")
            }
        ),
        form_options.create_form_options(
            {
                "name": "form_options",
                "screen": controller.get("main_screen"),
                "active": False,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_RANKING,
                "music_path": var.MUSICA_OPTIONS,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config")
            }        
        ),
        form_pause.create_form_pause(
            {
                "name": "form_pause",
                "screen": controller.get("main_screen"),
                "active": False,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_PAUSE,
                "music_path": var.MUSICA_PAUSA,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config")
            }
        ),
        form_stage.crear_form_stage(
            {
                "name": "form_stage",
                "screen": controller.get("main_screen"),
                "active": False,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_STAGE,
                "music_path": var.MUSICA_STAGE,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config"),
                "jugador": controller.get("player")
            }

        ),
        form_tutorial.crear_form_tutorial(
            {
                "name": "form_tutorial",
                "screen": controller.get("main_screen"),
                "active": False,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_TUTORIAL,
                "music_path": var.MUSICA_TUTORIAL,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config"),
                "jugador": controller.get("player")
            }

        ),
        form_name.create_form_name(
            {
                "name": "form_name",
                "screen": controller.get("main_screen"),
                "active": False,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_GANADOR,
                "music_path": var.MUSICA_NAME_VICTORY,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config"),
                "jugador": controller.get("player")
            }

        ),
        form_wish.create_form_wish(
            {
                "name": "form_wish",
                "screen": controller.get("main_screen"),
                "active": False,  
                "coord": (0, 0),
                "screen_dimension": (800, 600),
                "background": var.FONDO_WISH,
                "music_path": var.MUSICA_WISH,
                "screen_dimentions": var.DIMENSION_PANTALLA,
                "music_config": controller.get("music_config"),
                "jugador": controller.get("player")
            }

        )
    ] 
    
    return controller 

def forms_update(form_controller: dict, eventos: list[py.event.Event]):
    lista_formularios = form_controller.get("forms_list")

    for form in lista_formularios:
        if form.get("active"):
            match form.get("name"):
                case "form_menu":
                    menu_form = lista_formularios[0]
                    form_menu.update(menu_form)
                    form_menu.draw(menu_form)
                case "form_ranking":
                    ranking_form = lista_formularios[1]
                    form_ranking.update(ranking_form)
                    form_ranking.draw(ranking_form)
                case "form_options":
                    options_form = lista_formularios[2]
                    form_options.draw(options_form)
                    form_options.update(options_form)
                case "form_pause":
                    pause_form = lista_formularios[3]
                    form_pause.draw(pause_form)
                    form_pause.update(pause_form)
                case "form_stage":
                    stage_form = lista_formularios[4]
                    form_stage.update(stage_form,eventos)
                    form_stage.draw(stage_form)
                case "form_tutorial":
                    tuto_form = lista_formularios[5]
                    form_tutorial.update(tuto_form)
                    form_tutorial.draw(tuto_form)
                case "form_name":
                    name_form = lista_formularios[6]
                    form_name.update(name_form, eventos)
                    form_name.draw(name_form)
                case "form_wish":
                    wish_form = lista_formularios[7]
                    form_wish.update(wish_form)
                    form_wish.draw(wish_form)

def handle_events(eventos: list[py.event.Event], form_controller: dict):

    for evento in eventos:
        pass
    
def update(form_controller: dict, eventos: list[py.event.Event]):
    forms_update(form_controller, eventos)
    handle_events(eventos, form_controller)

