import modules.variables as var
import modules.stage as stage
import json
import os
import pygame as py

def mapear_valores(matriz: list[list], columna_a_mapear: int, callback):
    for indice_fila in range(len(matriz)):
        valor = matriz[indice_fila][columna_a_mapear]
        matriz[indice_fila][columna_a_mapear] = callback(valor)

def parsear_entero(valor: str):
    if valor.isdigit():
        return int(valor)
    return valor
    
def cargar_ranking(file_path: str, top: int = 10):
    ranking = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            texto = file.read()
            for linea in texto.split("\n"):
                if linea:
                    lista_datos_linea = linea.split(",")
                    ranking.append(lista_datos_linea)
   
        mapear_valores(ranking, columna_a_mapear=1, callback=parsear_entero)
        ranking = ranking[1:]  # Saltear el header
        ranking.sort(key=lambda fila: fila[1], reverse=True)
        return ranking[:top]
    
    
    except FileNotFoundError:
        # Si no existe el archivo, crearlo con header
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Nombre,Puntaje\n")
        return []

def guardar_puntaje(file_path: str, nombre: str, puntaje: int):
    """Guarda un nuevo puntaje en el archivo CSV"""
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{nombre},{puntaje}\n")

def cargar_configs(file_path: str) -> dict:
    data = {}
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def cargar_configs_stage(stage_data: dict):
    if not stage_data.get("juego_finalizado") and not stage_data.get("data_cargada"):
        configs_globales = cargar_configs(var.JSON_CONFIGS)
        stage_data["configs"] = configs_globales.get("nivel_1")
        stage_data["ruta_mazo"] = stage_data.get("configs").get("ruta_mazo")
        stage_data["coords_inicial_mazo_enemigo"] = stage_data.get("configs").get("coord_mazo_enemigo")
        stage_data["coords_inicial_mazo_player"] = stage_data.get("configs").get("coord_mazo_player")
        stage_data["cantidad_cartas_jugadores"] = stage_data.get("configs").get("cant_cartas_jugadores")

def guardar_info_csv (informacion: str):
    with open("", "a", encoding= "utf-8") as file:
        file.write(informacion)
        print(f"INFORMACIÓN GUARDADA -> {informacion}")

def generar_bd_cartas(path_mazo: str) -> dict:
    cartas_dict = {
        "cartas": {}
    }

    for root, dir, files in os.walk(path_mazo):
        reverse_path = ""
        deck_cards = []
        deck_name = ""
        for carta in files:
            card_path = os.path.join(root, carta)
            deck_name = root.replace("\\", "/").split("/")[-1]
            print(f"DECK NAME: {deck_name}")

            if "reverse" in card_path:
                reverse_path = card_path.replace("\\", "/")
            else:
                card_path = card_path.replace("\\", "/")
                filename = carta
                
                filename = filename.replace(".png", "")
                datos_crudo = filename.split("_")

                datos_card = {
                    "id": datos_crudo[0],
                    "atk": int(datos_crudo[4]),
                    "def": int(datos_crudo[6]),
                    "hp": int(datos_crudo[2]),
                    "ruta_frente": card_path,
                    "ruta_reverso": "",
                    "bonus": 1
                }
                deck_cards.append(datos_card)
        
            for index_carta in range(len(deck_cards)):
                deck_cards[index_carta]["ruta_reverso"] = reverse_path

            if deck_name:
                cartas_dict["cartas"][deck_name] = deck_cards

    guardar_info_cartas(var.JSON_INFO_CARDS, cartas_dict)
    return cartas_dict

def guardar_info_cartas(ruta_archivo: str, dict_cartas: dict):
    with open(ruta_archivo, "w", encoding="utf-8") as file:
        json.dump(dict_cartas, file, indent=4)

def cargar_bd_cartas(stage_data: dict):
    if not stage_data.get("juego_finalizado"):
        if os.path.exists(var.JSON_INFO_CARDS) and os.path.isfile(var.JSON_INFO_CARDS):
            print("============== CARGANDO BD CARTAS DESDE FILE ==============")
            stage_data["cartas_mazo_inicial"] = cargar_configs(var.JSON_INFO_CARDS).get("cartas", [])
        else:
            print("============== CARGANDO BD CARTAS DESDE DIR ==============")
            cartas_generadas = generar_bd_cartas(stage_data.get("ruta_mazo"))
            stage_data["cartas_mazo_inicial"] = cartas_generadas.get("cartas", [])

def redimensionar_imagen(ruta_img: str, porcentaje_a_ajustar: int):
    imagen_raw = py.image.load(ruta_img)
    ancho = imagen_raw.get_width()
    alto = imagen_raw.get_height()

    nuevo_alto = int(alto * float(f"0.{porcentaje_a_ajustar}"))
    nuevo_ancho = int(ancho * float(f"0.{porcentaje_a_ajustar}"))

    imagen_final = py.transform.scale(imagen_raw, (nuevo_ancho, nuevo_alto))
    return imagen_final

def reducir(callback, iterable: list):
    suma = 0
    for elemento in iterable:
        suma += callback(elemento)
    return suma