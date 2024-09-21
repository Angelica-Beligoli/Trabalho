import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evite os Inimigos")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Carrega os ativos
player_img = pygame.image.load('assets/player.png')
enemy_img = pygame.image.load('assets/enemy.png')

# Classe do Jogador
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 10

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe do Inimigo
class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Função para exibir o menu
def menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Evite os Inimigos", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    
    play_font = pygame.font.Font(None, 48)
    play_text = play_font.render("Pressione ENTER para jogar", True, BLACK)
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    while True:
        screen.fill(WHITE)
        screen.blit(text, text_rect)
        screen.blit(play_text, play_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # Sai do menu e inicia o jogo

# Loop do jogo
def game_loop():
    clock = pygame.time.Clock()
    player = Player()
    enemies = []
    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        screen.fill(WHITE)

        # Tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")

        # Gerar inimigos
        if random.randint(1, 30) == 1:  # Ajustar taxa de spawn
            enemies.append(Enemy())

        # Atualizar inimigos
        for enemy in enemies[:]:
            enemy.fall()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                score += 1  # Incrementa a pontuação por evitar

            # Verifica colisão
            if player.rect.colliderect(enemy.rect):
                print(f"Você foi atingido! Pontuação final: {score}")
                running = False  # Encerra o jogo em caso de colisão

        # Desenhar tudo
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Desenhar pontuação
        score_text = font.render(f"Pontuação: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    menu()  # Mostra o menu antes de iniciar o jogo
    game_loop()  # Inicia o loop do jogo
