import pygame as py

# CONFIGURACIONES DEL JUEGO
ICONO = "assets/img/icono.png"
DIMENSION_PANTALLA = (900, 600)
TITULO_JUEGO = "Dragon Ball TCG"
STAGE_TIMER = 500
JSON_CONFIGS = "configs.json"
JSON_INFO_CARDS = "info_cartas.json"
FPS = 30
POINTER = "assets/img/golden_frieza_pointer.png"

#FONTS
FONT_SAIYAN_SANS = "assets/fonts/Saiyan-Sans.ttf"
FONT_ALAGARD = "assets/fonts/alagard.ttf"

# CONFIGURACIONES AUDIO
VOLUMEN_INICIAL = 50
SOUND_PATH = "assets/sounds/click_scouter.ogg"

# SONIDOS
CLICK_SOUND = "assets/audio/sounds/click_scouter.ogg"
HEAL_ACTIVATED = "assets/audio/sounds/heal_activated.ogg"
SHIELD_ACTIVATED= "assets/audio/sounds/shield_activated.ogg"
SHIELD_DEACTIVATED = "assets/audio/sounds/shield_deactivated.ogg"
CRITICAL_HIT = "assets/audio/sounds/critical_hit.ogg"
INTRO_WISH = "assets/audio/sounds/wish_sound_intro.ogg"
OUTRO_WISH = "assets/audio/sounds/wish_sound_outro.ogg"

# CONFIGURACIONES JUGADOR
CANTIDAD_VIDA = 3

# BUTTON IMAGES
BOTON_PLAY_HAND = "assets/img/buttons_image/btn_play_hand.png"
BOTON_HEAL = "assets/img/buttons_image/heal.png"
BOTON_SHIELD = "assets/img/buttons_image/shield.png"
SHIELD_ACTIVO = "assets/img/icons/icon_shield.png"
HEAL_ACTIVO = "assets/img/icons/icon_heal.png"

# FORMS BACKGROUNDS
FONDO_MENU = "assets/img/forms/form_main_menu.png"
FONDO_RANKING = "assets/img/forms/form_ranking.png"
FONDO_PAUSE = "assets/img/forms/form_pause.png"
FONDO_DERROTA = "assets/img/forms/form_enter_name_0.png"
FONDO_GANADOR = "assets/img/forms/form_enter_name_1.png"
FONDO_STAGE = "assets/img/background_cards_simple.png"
FONDO_NAME_VICTORY = "assets/img/forms/form_enter_name_1.png"
FONDO_NAME_DEFEAT = "assets/img/forms/form_enter_name_0.png"
FONDO_WISH = "assets/img/forms/form_wish_select.png"
FONDO_TUTORIAL = "assets/img/forms/FORM_TUTORIAL/fondo_tutorial.jpg"

dict_forms_status = {}

# FILE RANKING
RANKING_CSV = "puntajes.csv"

# RUTAS MUSICA
MUSICA_RANKING = "assets/audio/music/form_ranking.ogg"
MUSICA_MENU = "assets/audio/music/form_main_menu.ogg"
MUSICA_OPTIONS = "assets/audio/music/form_options.ogg"
MUSICA_WISH = "assets/audio/music/form_wish_select.ogg"
MUSICA_PAUSA = "assets/audio/music/form_pausa.ogg"
MUSICA_STAGE = "assets/audio/music/battle_music.ogg"
MUSICA_NAME_VICTORY = "assets/audio/music/win_music.ogg"
MUSICA_NAME_DEFEAT = "assets/audio/music/lose_music.ogg"
MUSICA_TUTORIAL = "assets/audio/music/sonido_prelude_dbz.ogg"

# COLORES
colores = {
    "amarillo":  py.Color("yellow"),
    "azul": py.Color("blue"),
    "blanco": py.Color("white"),
    "cian": py.Color("cyan"),
    "naranja": py.Color("orange"),
    "negro": py.Color("black"),
    "rojo": py.Color("red"),
    "rosa": py.Color("pink"),
    "verde": py.Color("green"),
    "violeta": py.Color("purple")
}