from modules.auxiliar import generar_bd_cartas, guardar_info_cartas

cartas = generar_bd_cartas("./assets/img/decks")
guardar_info_cartas("./info_cartas.json", cartas)
print(cartas.get("cartas"))
