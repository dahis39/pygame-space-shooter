import pygame
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Shooting Game")

# Load background image
background_image = pygame.image.load("space.jpg").convert()
# Fonts
game_over_font = pygame.font.Font(None, 72)
kill_count_font = pygame.font.SysFont(None, 24)

# Game objects
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shoot_delay = 1000  # Time delay between enemy shots
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += 3

        # Check if it's time for the enemy to shoot
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5
        if self.rect.top > window_height:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Create player
player = Player(window_width // 2, window_height - 100)
all_sprites.add(player)

# Game loop
running = True
game_over = False
kill_count = 0
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN and game_over:
                # Restart the game
                all_sprites.empty()
                enemies.empty()
                bullets.empty()
                enemy_bullets.empty()
                player = Player(window_width // 2, window_height - 100)
                all_sprites.add(player)
                game_over = False
                kill_count = 0

    if not game_over:
        # Update game objects
        all_sprites.update()

        # Spawn enemies
        if random.randint(0, 100) < 2:
            enemy = Enemy(random.randint(0, window_width), 0)
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check for collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            enemy = Enemy(random.randint(0, window_width), 0)
            all_sprites.add(enemy)
            enemies.add(enemy)
            kill_count += 1

        # Check for collision between player and enemy bullets
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            game_over = True
        # Check for collision between player and enemy
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_over = True

    window.blit(background_image, (0, 0))
    
    all_sprites.draw(window)
    
    kill_count_text = kill_count_font.render("Kills: {}".format(kill_count), True, WHITE)
    window.blit(kill_count_text, (10, 10))
    
    if game_over:
        game_over_text = game_over_font.render("GAME OVER", True, pygame.Color("white"))
        window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2,
                                      window_height // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
