import pygame
import random
import time
import os

pygame.init()
pygame.mixer.init()  # Inicializa el mixer para la música

width, height = 600, 600
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Hunter Rat")

x, y = 300, 300
delta_x, delta_y = 20, 0

food_x, food_y = random.randrange(0, width) // 50 * 50, random.randrange(0, height) // 50 * 50

body_list = [(x, y)]
score_value = 0

clock = pygame.time.Clock()

game_over = False
game_paused = False
cat_mode = False  # Variable para saber si se ha activado el modo del gato
game_speed = 14  # Velocidad inicial del juego

font = pygame.font.SysFont("bahnschrift", 25)

# Cargar las imágenes
cake_image = pygame.image.load("Cake.png")
cake_image = pygame.transform.scale(cake_image, (50, 50))  # Escalar la imagen a 50x50

cat_image = pygame.image.load("Gato.gif")  # Cargar la imagen del gato
cat_image = pygame.transform.scale(cat_image, (50, 50))  # Escalar la imagen a 50x50

# Imagen de la comida (inicialmente el pastel)
food_image = cake_image

# Cargar y reproducir la música de fondo
pygame.mixer.music.load("Soft.mp3")  # Cargar la canción de fondo
pygame.mixer.music.play(-1)  # Reproducir la canción en loop

# Inicializar puntaje más alto
high_score = 0

# Función para cargar el puntaje más alto desde un archivo
def load_high_score():
    global high_score
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())

# Función para guardar el puntaje más alto en un archivo
def save_high_score():
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

# Cargar el puntaje más alto al inicio del juego
load_high_score()

def reset_game():
    global x, y, delta_x, delta_y, food_x, food_y, body_list, game_over, score_value, game_paused, cat_mode, food_image, game_speed
    x, y = 300, 300
    delta_x, delta_y = 50, 0
    food_x, food_y = random.randrange(0, width) // 50 * 50, random.randrange(0, height) // 50 * 50
    body_list = [(x, y)]
    score_value = 0
    game_over = False
    game_paused = False
    cat_mode = False
    food_image = cake_image  # Reiniciar la imagen de la comida
    game_speed = 14  # Restablecer la velocidad del juego

    # Reiniciar la música a la inicial
    pygame.mixer.music.load("Soft.mp3")
    pygame.mixer.music.play(-1)

def snake():
    global x, y, food_x, food_y, game_over, score_value, game_paused, cat_mode, food_image, high_score, game_speed
    x = (x + delta_x) % width
    y = (y + delta_y) % height

    if (x, y) in body_list:
        game_over = True
        return

    body_list.append((x, y))

    # Crear rectángulos para la serpiente y la comida
    snake_rect = pygame.Rect(x, y, 20, 20)
    food_rect = pygame.Rect(food_x, food_y, 50, 50)

    # Verificar si hay colisión entre la serpiente y la comida
    if snake_rect.colliderect(food_rect):
        # Mueve la comida a una nueva posición asegurándote de que no esté en el cuerpo de la serpiente
        while True:
            new_food_x, new_food_y = random.randrange(0, width, 50), random.randrange(0, height, 50)
            if (new_food_x, new_food_y) not in body_list:
                food_x, food_y = new_food_x, new_food_y
                break
        
        # Incrementar la puntuación
        score_value += 1
        
        # Cambiar a modo gato si la puntuación es 15
        if score_value == 15:
            game_paused = True
            cat_mode = True
            food_image = cat_image  # Cambiar la imagen de la comida al gato
            game_speed = 30  # Aumentar la velocidad del juego a 30
            
            # Cambiar la música a Hunter-mp3
            pygame.mixer.music.load("Hunter.mp3")
            pygame.mixer.music.play(-1)  # Reproducir en loop

    else:
        # Si no hay colisión, se elimina el segmento más antiguo
        del body_list[0]

    game_screen.fill((0, 0, 0))

    # Verificar si se ha superado el puntaje más alto
    if score_value > high_score:
        high_score = score_value
        save_high_score()  # Guardar el nuevo puntaje más alto

    # Mostrar puntaje actual y puntaje más alto
    score = font.render(f"Score: {score_value}", True, (255, 255, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    game_screen.blit(score, [5, 5])
    game_screen.blit(high_score_text, [5, 35])

    # Dibuja la imagen de la comida
    game_screen.blit(food_image, (food_x, food_y))

    # Dibuja la serpiente
    for (i, j) in body_list:
        pygame.draw.rect(game_screen, (255, 255, 255), [i, j, 20, 20])

    pygame.display.update()

def display_pause_message():
    game_screen.fill((0, 0, 0))
    
    # Mensaje principal
    pause_message = font.render("ME CANSÉ DE HUIR, ME FORTALECÍ,", True, (255, 255, 0))
    pause_message_rect = pause_message.get_rect(center=(width // 2, height // 2 - 20))
    game_screen.blit(pause_message, pause_message_rect)
    
    # Mensaje secundario
    pause_message_2 = font.render("Y AHORA, SOY YO QUIEN DA CAZA.", True, (255, 255, 0))
    pause_message_rect_2 = pause_message_2.get_rect(center=(width // 2, height // 2 + 20))
    game_screen.blit(pause_message_2, pause_message_rect_2)

    pygame.display.update()

while True:
    if game_over:
        game_screen.fill((0, 0, 0))
        score = font.render(f"Score: {len(body_list) - 1}", True, (255, 255, 0))
        game_screen.blit(score, [0, 0])
        
        # Mensaje GAME OVER
        msg = font.render("GAME OVER!", True, (255, 255, 2))
        msg_rect = msg.get_rect(center=(width // 2, height // 2 - 20))
        game_screen.blit(msg, msg_rect)

        # Mensaje Press R to Restart
        restart_msg = font.render("Press R to Restart", True, (255, 255, 2))
        restart_msg_rect = restart_msg.get_rect(center=(width // 2, height // 2 + 20))
        game_screen.blit(restart_msg, restart_msg_rect)

        pygame.display.update()

        # Espera a que el jugador presione 'R' para reiniciar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

    elif game_paused:
        display_pause_message()
        time.sleep(5)

        # Espera a que el jugador presione cualquier tecla para continuar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                game_paused = False  # Reanudar el juego

    else:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if delta_x != 20:
                        delta_x = -20
                    delta_y = 0
                elif event.key == pygame.K_RIGHT:
                    if delta_x != -20:
                        delta_x = 20
                    delta_y = 0
                elif event.key == pygame.K_UP:
                    delta_x = 0
                    if delta_y != 20:
                        delta_y = -20
                elif event.key == pygame.K_DOWN:
                    delta_x = 0
                    if delta_y != -20:
                        delta_y = 20
                else:
                    continue
                snake()
        if not events:
            snake()
        clock.tick(game_speed)