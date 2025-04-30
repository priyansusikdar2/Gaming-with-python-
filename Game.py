import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

# Colors
WHITE = (255, 255, 255)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load assets with transparency
background = pygame.image.load("images/space.webp").convert()
player_img = pygame.image.load("images/playership.jpeg").convert_alpha()
alien_img = pygame.image.load("images/ufo.jpg").convert_alpha()
bullet_img = pygame.image.load("images/bullet.webp").convert_alpha()

# Scale images
player_img = pygame.transform.scale(player_img, (60, 40))
alien_img = pygame.transform.scale(alien_img, (50, 35))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -8

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Sprite groups
player = Player()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Alien spawn timer
ALIEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ALIEN_EVENT, 800)

# Score and game loop
score = 0
running = True

while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ALIEN_EVENT:
            alien = Alien()
            aliens.add(alien)
            all_sprites.add(alien)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet)

    # Update
    player.update(keys)
    aliens.update()
    bullets.update()

    # Collisions
    hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
    score += len(hits)

    if pygame.sprite.spritecollideany(player, aliens):
        running = False

    # Draw background
    screen.blit(background, (0, 0))
    
    # Draw direction line (highlight bullet path)
    for bullet in bullets:
        pygame.draw.line(screen, (255, 165, 0), (bullet.rect.centerx, bullet.rect.bottom), (bullet.rect.centerx, bullet.rect.bottom + 10), 2)

    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
