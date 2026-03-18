import pygame as py
import modules.variables as var
import sys 
import modules.forms.form_controller as form_controller
import modules.participante_juego as participante


def jueguito():
     
    py.init()

    py.display.set_icon(py.image.load(var.ICONO))
    py.display.set_caption(var.TITULO_JUEGO)
    pantalla_juego = py.display.set_mode(var.DIMENSION_PANTALLA)
    
    py.mouse.set_visible(False)
    cursor_img = py.image.load(var.POINTER).convert_alpha()
    cursor_img = py.transform.scale(cursor_img, (40, 60))

    corriendo = True
    reloj = py.time.Clock()

    datos_juego = {
        "puntaje": 0,
        "cantidad_vidas": var.CANTIDAD_VIDA,
        "player": participante.inicializar_participante(pantalla=pantalla_juego, nombre= "Player"),
        "music_config": {
            "music_volumen": var.VOLUMEN_INICIAL,
            "music_on": True,
            "music_init": False
        }
    }

    
    form_control = form_controller.create_form_controller(
        pantalla_juego, datos_juego
    )

    while corriendo:
        
        events = py.event.get()
        reloj.tick(var.FPS)
    
        for event in events:
            if event.type == py.QUIT:
                corriendo = False
        
        form_controller.update(form_control, events)

        mouse_pos = py.mouse.get_pos()
        pantalla_juego.blit(cursor_img, mouse_pos)

        py.display.flip()

    print("El juego se está cerrando...")
    py.quit()
    sys.exit()
