import pygame
import random

pygame.init()

ancho = 800
alto = 600

screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("PONG!")

blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255,0,0)

screen.fill(negro)

velocidad_pelota = .1
puntos_izquierda = 0
puntos_derecha = 0
puntos_victoria = 10

#-------------------inicio de clases   

class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 100)
        self.velocidad = 1
        self.mover_arriba = False
        self.mover_abajo = False

    def mover(self):
        if self.mover_arriba == True and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if self.mover_abajo == True and self.rect.bottom < alto:
            self.rect.y += self.velocidad

    def dibujar(self, screen):
        pygame.draw.rect(screen, blanco, self.rect)


class Pelota:
    def __init__(self, x, y, radio):
        self.x = x
        self.y = y
        self.radio = radio
        self.vel_x = velocidad_pelota
        self.vel_y = velocidad_pelota
        self.rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)


    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Rebote arriba y abajo
        if self.y - self.radio <= 0 or self.y + self.radio >= alto:
            self.vel_y *= -1

        # Actualizar el rectángulo
        self.rect.x = self.x - self.radio
        self.rect.y = self.y - self.radio

    def reiniciar(self):
        self.x = 390
        self.y = 290
        self.vel_x = random.choice([-velocidad_pelota, velocidad_pelota])
        self.vel_y = random.choice([-velocidad_pelota, velocidad_pelota])

    def dibujar(self, screen):
        pygame.draw.circle(screen, blanco, (self.x, self.y), self.radio)

#-------------------fin de clases       

#-------------------inicio de funciones

def pantalla_inicio():
    comenzar = True
    while comenzar:
        screen.fill(negro)
        mensaje_texto = font_ganador.render("Presione ENTER para jugar", True, blanco)
        screen.blit(mensaje_texto, (80, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Detectar teclas presionadas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    comenzar = False



def dibujar_pantalla(puntos_izquierda, puntos_derecha):
    screen.fill(negro)
    jugador_izquierda.dibujar(screen)
    jugador_derecha.dibujar(screen)
    pelota.dibujar(screen)

    linea_inicio = (398, 1)  
    linea_fin = (398, 800)   
    ancho_linea = 4           
    pygame.draw.line(screen, blanco, linea_inicio, linea_fin, ancho_linea)

    score_text = font_puntaje.render(f"{puntos_izquierda}", True, blanco)
    screen.blit(score_text, (150, 40))

    score_text = font_puntaje.render(f"{puntos_derecha}", True, blanco)
    screen.blit(score_text, (550, 40))


def jugar_denuevo():
    while True:

        letra_r = font_ganador.render("Presione R para jugar denuevo", True, blanco)
        letra_q = font_ganador.render("Presione Q para salir", True, blanco)
        
        screen.blit(letra_r, (80, 400))
        screen.blit(letra_q, (80, 500))
        
        pygame.display.flip() # Redibuja la pantalla
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return None


def ganador(jugador, pts_izquierda , pts_derecha):
    dibujar_pantalla(pts_izquierda, pts_derecha)
    ganador_text = font_ganador.render(f"Gano el jugador de la {jugador}", True, rojo)
    screen.blit(ganador_text, (80, 10))  
    if jugar_denuevo() == True:
        global puntos_izquierda
        global puntos_derecha
        puntos_izquierda = 0
        puntos_derecha = 0

def dibujar_colisiones():
    pygame.draw.rect(screen, rojo, pelota.rect, 2)  # Dibuja el rectángulo de la pelota
    pygame.draw.rect(screen, rojo, jugador_izquierda.rect, 2)  # Rectángulo del jugador izquierdo
    pygame.draw.rect(screen, rojo, jugador_derecha.rect, 2)  # Rectángulo del jugador derecho
    
#-------------------fin de funciones

#-------------------inicio juego

# Puntajes
font_puntaje = pygame.font.SysFont("dejavusansmono", 100)
font_ganador = pygame.font.SysFont("dejavusansmono", 25)

# Sonidos
sonido_rebote = pygame.mixer.Sound("sonidos/rebote.mp3")
sonido_punto= pygame.mixer.Sound("sonidos/punto.mp3")
sonido_ganador = pygame.mixer.Sound("sonidos/ganador.mp3")


# Posiciones
jugador_izquierda = Jugador(10, 250)
jugador_derecha = Jugador(770, 250)
pelota = Pelota(390, 290, 10)


pantalla_inicio()

#bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar teclas presionadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                jugador_izquierda.mover_arriba = True
            if event.key == pygame.K_s:
                jugador_izquierda.mover_abajo = True
            if event.key == pygame.K_UP:
                jugador_derecha.mover_arriba = True
            if event.key == pygame.K_DOWN:
                jugador_derecha.mover_abajo = True

        # Detectar teclas soltadas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                jugador_izquierda.mover_arriba = False
            if event.key == pygame.K_s:
                jugador_izquierda.mover_abajo = False
            if event.key == pygame.K_UP:
                jugador_derecha.mover_arriba = False
            if event.key == pygame.K_DOWN:
                jugador_derecha.mover_abajo = False 


    jugador_izquierda.mover()
    jugador_derecha.mover()
    pelota.mover()

    
    # colision
    if pelota.rect.colliderect(jugador_izquierda.rect) or pelota.rect.colliderect(jugador_derecha.rect):
        pelota.vel_x *= -1 
        pygame.mixer.Sound.play(sonido_rebote)

        # Incrementar la velocidad gradualmente
        incremento_velocidad = 0.1            
        if pelota.vel_x > 0: 
            pelota.vel_x += incremento_velocidad 
        else:
            pelota.vel_x -= incremento_velocidad  

        #si comentamos esto, sale mas recto
        # if pelota.vel_y > 0: 
        #     pelota.vel_y += incremento_velocidad
        # else:
        #     pelota.vel_y -= incremento_velocidad    

    elif pelota.x < 30:
        pelota.reiniciar()
        puntos_derecha += 1
        pygame.mixer.Sound.play(sonido_punto)
        if puntos_derecha == puntos_victoria:
            pygame.mixer.Sound.play(sonido_ganador)
            respuesta_usuario = ganador("derecha", puntos_izquierda , puntos_derecha)
            velocidad_pelota = .1

    elif pelota.x > 770:
        pelota.reiniciar()
        pygame.mixer.Sound.play(sonido_punto)
        puntos_izquierda += 1
        if puntos_izquierda == puntos_victoria:
            pygame.mixer.Sound.play(sonido_ganador)
            respuesta_usuario = ganador("izquierda" , puntos_izquierda , puntos_derecha)
            velocidad_pelota = .1

    dibujar_pantalla(puntos_izquierda, puntos_derecha)
    #dibujar_colisiones()

    pygame.display.flip()

pygame.quit()
