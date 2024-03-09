import pygame                                                           #para poder agregarlo, tenemos que ir a settings,
                                                                        # python interpreter, +
import random
import math
from pygame import mixer                                                #para cargar archivos .mp3

# Inicializa pygame
pygame.init()

# Crea la pantalla
pantalla = pygame.display.set_mode((800, 600))

#Titulo e Icono ----> buscamos los iconos de FLATICON
pygame.display.set_caption("Invasión Espacial")                         #cambiamos el titulo de la pantalla
icono = pygame.image.load("espada-de-luz.png")                          #descargamos el icono y lo guardamos en la misma carpeta donde esta el codigo
pygame.display.set_icon(icono)                                          #cargamos el icono al display
fondo = pygame.image.load("cielo-estrellado (1).jpg")

#Musica de fondo
mixer.music.load("musica_fondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)                                                    #ponemos -1 para que suene todo el tiempo en loop

#Variable del Jugador
img_jugador = pygame.image.load("nave-espacial.png")
#ubicacion 0,0 seria la esquina superior izquierda
jugador_x = 368                                                         #para que quede exacto en la mitad 400 - (64/2) = 368
jugador_y = 520                                                         #para que quede exacto abajo del todo 600 - 64 = 536
jugador_x_cambio = 0

#Variable del Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("astronave.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

#Variable del Bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 520
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

#puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (280, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x, y))



#Funcion del jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))                   #rellenamos la pantalla con el jugador y la posicion

#Funcion del enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y)) #aqui ponemos ene por enemigo y sirve para que cada vez que cargue los enemigos, los ponga con todos los parametros.

#Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

#Funcion detectar colsiones
def hay_colision(x_1, y_1, x_2, y_2):
    #tenemos que hacer una operacion "raiz cuadrada  (x2-x1)^2 + (y2-y1)^2" esto detecta la distancia entre elementos
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:

    #RGB, ponerlo antes de la funcion asi no tapa
    pantalla.blit(fondo, (0,0))                                      # cambiamos el color de fondo de la pantalla
    #MOVER JUGADOR
    #jugador_x += 0.1                                                   #movemos el jugador cambiando +,-
    #jugador_y -= 0.1

    #iterar eventos
    for evento in pygame.event.get():
        #Evento cerrar
        if evento.type == pygame.QUIT:                                  #indicamos que cuando se presione la x se cierre el juego y termine el loop
            se_ejecuta = False

        #Evento presionar tecla
        elif evento.type == pygame.KEYDOWN:                             #tecla presionada
            if evento.key == pygame.K_LEFT:
                #print("Flecha izquierda presionada")
                jugador_x_cambio = -0.3                                 #mientras mas grande el numero, mas rapido nos moveremos
            elif evento.key == pygame.K_RIGHT:
                jugador_x_cambio = +0.3
                #print("Flecha derecha presionada")
            elif evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo_laser.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        #Evento soltar tecla
        elif evento.type == pygame.KEYUP:                               #tecla soltada
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
                #print("La flecha fue soltada")

    #Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    #mantener jugador dentro de bordes del jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        #Fin del juego
        if enemigo_y [e] > 500:
            for k in range (cantidad_enemigos):
                enemigo_y[k] = 1000 #ponemos un numero mayor a la pantalla para que los enemigos desaparescan de ella y se vayan mas abajo
            texto_final()
            break


        enemigo_x[e] += enemigo_x_cambio[e]
    #enemigo_y += enemigo_y_cambio

    # mantener jugador dentro de bordes del enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("Explosion.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    #Movimiento bala
    if bala_y <= -64:                                   #con esto indico que la vala en el eje y no siga infinitamente
        bala_y = 520
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio



    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)


    #Actualizar
    pygame.display.update()                                             #actualizamos para que cargue el color