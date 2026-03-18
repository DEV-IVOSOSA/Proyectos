import random
import json
import dibujo_ahorcado

def cargar_palabras():
    file = open("data.json", "r")
    data = json.load(file)
    file.close()
    return data["ahorcado"]

def menu_opciones(mensaje:str, mensaje_error:str , menu:list) -> int:
    print("--------Menu de opciones--------")
    for i in range(len(menu)):
        print(menu[i])

    opcion_seleccionada = input(mensaje)
    print("\t")

    if opcion_seleccionada.isdigit() == True:
        opcion_seleccionada = int(opcion_seleccionada)
        if opcion_seleccionada > 0 and opcion_seleccionada <= (len(menu)):
            return opcion_seleccionada
        else:
            print(mensaje_error)
            return(menu_opciones(mensaje,mensaje_error,menu))  
    else:
        print(mensaje_error)
        return(menu_opciones(mensaje,mensaje_error,menu))


def seleccionar_idioma():
    while True:
        
        idioma_seleccionado = input("Presione E para jugar con palabras en Español (ES) / Presione N para jugar con palabras en Ingles (EN): ")
        
        if idioma_seleccionado.upper() == "E":
            return "ES"
            break
        elif idioma_seleccionado.upper() == "N":
            return "EN"
            break
        else:
            print("Opcion Incorrecta!! Intente nuevamente. ")

                
def seleccionar_palabra(palabras_cargadas, idioma):
    palabra_seleccionada = random.choice(palabras_cargadas)
    return palabra_seleccionada[idioma]

def crear_renglones(palabra_seleccionada, letras_descubiertas):
    print("Palabra: ", end=" ")
    for i in range(len(palabra_seleccionada)):
        if i in letras_descubiertas: #el diccionario
            print(letras_descubiertas[i], end=" ")
        else:
            print("_", end=" ")
    print("\t")


def ingrese_letra(mensaje = "Ingrese una letra: ", mensaje_error = "La tecla ingresada no es una letra. Intente nuevamente. "):
    while True:
        letra_presionada = input(mensaje).strip()
        if len(letra_presionada) == 1 and letra_presionada.isalpha():
            return letra_presionada
            break
        else:
            print(mensaje_error)

def validar_letra_repetida(letra_ingresada, letras_descubiertas, letras_erradas_set):
    # Recorrer las letras descubiertas
    for letra in letras_descubiertas.values():
        if letra_ingresada == letra:
            return True 

    # Recorrer las letras erradas
    for letra in letras_erradas_set:
        if letra_ingresada == letra:
            return True

    return False 


def busca_si_existe(letra, palabra_seleccionada):
    posiciones_existentes = []
    for j in range(len(palabra_seleccionada)):
        if palabra_seleccionada[j] == letra:
            posiciones_existentes.append(j)
    return posiciones_existentes


def verificar_si_gano(palabra_seleccionada, puntos):
    palabra_actual = ""
    for i in range(len(palabra_seleccionada)):
        if i in letras_descubiertas:
            palabra_actual += letras_descubiertas[i] 
        else:
            palabra_actual += "_" 

    if palabra_actual == palabra_seleccionada:
        print("¡Felicidades! Adivinaste la palabra:", palabra_seleccionada)
        print(f"Obtuviste {puntos} puntos!")
        print("\t")

        nombre_jugador = input("Ingresa tu nombre: ")
        guardar_score(nombre_jugador, puntos)
        print(f"Gracias, {nombre_jugador}. ¡Tus puntos han sido guardados!")

        while True:
            decision = input("¿Que desea hacer ahora: Volver al menu (M) / Finalizar el juego (F)? ")
            if decision.upper() == "M":
                print("Volviendo al menú principal...")
                return "M"
            elif decision.upper() == "F":
                print("Gracias por jugar. ¡Hasta la próxima!")
                return "F"
            else:
                print("Opción inválida. Por favor, selecciona M para Menú o F para Finalizar.")


def guardar_score(nombre, puntos):
    file = open("scores.json", "r")
    historial_jugadores = json.load(file)
    file.close()
   
    nuevo_jugador = {} 

    nuevo_jugador = {
    "Nombre": nombre,
    "Score": puntos,
    }

    jugadores = historial_jugadores["Jugadores"]

    if len(jugadores) == 5:
        ordenar_puntajes()

        file = open("scores.json", "r")
        historial_jugadores = json.load(file)
        file.close()

        jugadores = historial_jugadores["Jugadores"]

        if puntos > jugadores[-1]["Score"]:
            jugadores[-1] = nuevo_jugador
    else:
        jugadores.append(nuevo_jugador)
        
    file = open("scores.json", "w")
    file.write(json.dumps(historial_jugadores))        
    file.close()  
            

def ordenar_puntajes():
    file = open("scores.json", "r")
    historial_jugadores = json.load(file)
    file.close()

    # Ordenamiento burbuja
    jugadores = historial_jugadores["Jugadores"]
    n = len(jugadores)

    for i in range(n):
        for j in range(0, n - i - 1):
            if jugadores[j]["Score"] < jugadores[j + 1]["Score"]:
                # asi solo en python
                jugadores[j], jugadores[j + 1] = jugadores[j + 1], jugadores[j]

    historial_jugadores["Jugadores"] = jugadores

    file = open("scores.json", "w")
    file.write(json.dumps(historial_jugadores))       
    file.close() 


def mostrar_mejores_puntajes():
    ordenar_puntajes()

    file = open("scores.json", "r")
    historial_jugadores = json.load(file)
    file.close()
    
    print("Los mejores puntajes")
    print("--------------------")

    file = open("scores.json", "r")
    historial_jugadores = json.load(file)
    file.close()


    for i in historial_jugadores["Jugadores"]:
        print(f"{i['Nombre']}: {i['Score']} Puntos")
    
    print("\t")


opciones_menu = ["1. Jugar", "2. Puntajes" , "3. Salir"]
datos = cargar_palabras()

print("--------------------------------")
print("    ¡BIENVENIDO AL AHORCADO!    ")
print("\t")


continuar_jugando = True

while continuar_jugando:
    
    opcion_seleccionada = menu_opciones('Seleccione una opcion: ', 'Opcion invalida. Intente nuevamente.' , opciones_menu)

    match opcion_seleccionada:
        case 1:
            print("Empecemos!!")
            idioma = seleccionar_idioma()
            palabra_seleccionada = seleccionar_palabra(datos, idioma)
            print(palabra_seleccionada)
            intentos = 0
            puntos = 0
            letras_descubiertas = {}
            letras_erradas_set = set()

            fallos = 0 
            max_fallos = 6 

            while True:
                print("Letras erradas: ", end=" ")
                if len(letras_erradas_set) > 0:
                    print(", ".join(letras_erradas_set))
                    print("\t")
                    
                print(dibujo_ahorcado.dibujo[intentos])
                crear_renglones(palabra_seleccionada, letras_descubiertas)
                

                while True:
                    letra_ingresada = ingrese_letra()
                    if validar_letra_repetida(letra_ingresada, letras_descubiertas, letras_erradas_set):
                        print("Ya ingresaste esa letra. Intenta con otra.")
                    else:
                        break

                posicion_letras = busca_si_existe(letra_ingresada, palabra_seleccionada)

                if len(posicion_letras) > 0:
                    puntos += 1
                    print("Bien!! Adivinaste una letra.")
                    for posicion in posicion_letras:
                        letras_descubiertas[posicion] = letra_ingresada 
                else:
                    intentos += 1
                    print("Error! Esa letra no se encuentra en la palabra oculta")
                    letras_erradas_set.add(letra_ingresada)
                    if intentos == max_fallos:
                        print(dibujo_ahorcado.dibujo[intentos])
                        print(f"Perdiste!! la palabra era {palabra_seleccionada}")
                        print("\t")
                        break

                # Verificar si ganó
                resultado = verificar_si_gano(palabra_seleccionada, puntos)
                if resultado == "M":  
                    break 
                elif resultado == "F": 
                    continuar_jugando = False
                    break 

        case 2:
            mostrar_mejores_puntajes()
        case 3:
            print("MUCHAS GRACIAS POR JUGAR")
            print("Saliendo del juego...")
            continuar_jugando = False
