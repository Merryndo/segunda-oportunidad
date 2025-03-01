import pygame

# Inicializar pygame
pygame.init()

# Configurar pantalla
ANCHO = 800
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Juego de Plataforma Retro")

# Cargar fondo
fondo = pygame.image.load("fondo.png")
amor = pygame.image.load("amor.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Ajustar la imagen al tamaño de la pantalla
amor = pygame.transform.scale(amor, (ANCHO, ALTO))
# Cargar personaje
personaje_img = pygame.image.load("personaje.png")
personaje_img = pygame.transform.scale(personaje_img, (50, 50))  # Aumenta el tamaño del personaje
personaje_rect = personaje_img.get_rect()
personaje_rect.topleft = (50, ALTO - 135)  # Posición inicial

# Cargar sonidos
pygame.mixer.init()
pygame.mixer.music.load("musica.mp3")  # Música de fondo
pygame.mixer.music.play(-1)  # Repetir siempre

sonido_salto = pygame.mixer.Sound("salto.wav")

# Contador de vidas
vidas = 3

# Cargar imagen de corazón (puedes usar un archivo PNG de corazón)
corazon_img = pygame.image.load("corazon.png")
corazon_img = pygame.transform.scale(corazon_img, (30, 30))  # Ajusta el tamaño del corazón

# Crear obstáculos
obstaculos = []
for i in range(3):
    obstaculo = pygame.Rect(300 + i * 200, ALTO - 100, 10, 10)  # Alinear con el personaje
    obstaculos.append(obstaculo)

# Variables de movimiento
velocidad = 3
salto = False
gravedad = 0

# Reloj para FPS
clock = pygame.time.Clock()

# Función para mostrar mensaje de "¿Quieres volver a intentarlo?"
def mostrar_mensaje():
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("¿Quieres volver a intentarlo?", True, (255, 255, 255))
    pantalla.blit(texto, (200, 150))

    boton_si = pygame.Rect(200, 200, 100, 50)
    boton_no = pygame.Rect(400, 200, 100, 50)

    pygame.draw.rect(pantalla, (0, 255, 0), boton_si)
    pygame.draw.rect(pantalla, (255, 0, 0), boton_no)

    texto_si = fuente.render("Sí", True, (0, 0, 0))
    texto_no = fuente.render("No", True, (0, 0, 0))
    
    pantalla.blit(texto_si, (230, 210))
    pantalla.blit(texto_no, (430, 210))

    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if boton_si.collidepoint(x, y):
                    mensaje_final()
                    esperando = False  # Reiniciar juego
                if boton_no.collidepoint(x, y):
                    pygame.quit()

# Función para mostrar el mensaje final
def mensaje_final():
    pantalla.blit(amor, (0, 0))
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("Yo también, ¿quieres salir conmigo?", True, (255, 255, 255))
    pantalla.blit(texto, (160, 175))
    pygame.display.flip()
    pygame.time.delay(3000)

suelo = ALTO - 135  # Posición fija del suelo para que el personaje siempre caiga en el mismo lugar

# Función para reiniciar el juego
def reiniciar_juego():
    global personaje_rect, vidas, obstaculos
    personaje_rect.topleft = (50, suelo)  # Reiniciar personaje al punto inicial
    vidas -= 1  # Restar una vida
    obstaculos = []  # Limpiar obstáculos y crear nuevos
    for i in range(3):
        obstaculo = pygame.Rect(300 + i * 200, ALTO - 100, 10, 10)  # Alinear con el personaje
        obstaculos.append(obstaculo)

# Bucle principal del juego
jugando = True
while jugando:
    pantalla.blit(fondo, (0, 0))  # para que se vea el fondo

    # Dibujar los corazones (vidas) en la esquina superior izquierda
    for i in range(vidas):
        pantalla.blit(corazon_img, (10 + i * 40, 10))  # Cada corazón a la derecha del anterior

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()
    
    # Movimiento del personaje
    if teclas[pygame.K_RIGHT]:  # Moverse a la derecha
        personaje_rect.x += velocidad
    if teclas[pygame.K_UP] and not salto:  # Saltar
        sonido_salto.play()
        salto = True
        gravedad = -14
    
    # Aplicar gravedad
    if salto:
        personaje_rect.y += gravedad
        gravedad += 1
        suelo = ALTO - 135  # La posición EXACTA donde el personaje debe aterrizar
    if personaje_rect.y >= suelo:
        personaje_rect.y = suelo
        salto = False  # Restablecer salto cuando toca el suelo

    # Mover obstáculos
    for obstaculo in obstaculos:
        obstaculo.x -= velocidad
        if obstaculo.x < -40:
            obstaculo.x = ANCHO

    # Detectar colisiones
    for obstaculo in obstaculos:
        if personaje_rect.colliderect(obstaculo):
            if vidas > 1:  # Si hay vidas restantes
                reiniciar_juego()  # Reiniciar el juego con una vida menos
            else:  # Si no quedan vidas
                mostrar_mensaje()  # Mostrar el mensaje final
                jugando = False
                break

    # Dibujar personaje y obstáculos
    pantalla.blit(personaje_img, personaje_rect)
    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, (255, 0, 0), obstaculo)  # Rojo

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
