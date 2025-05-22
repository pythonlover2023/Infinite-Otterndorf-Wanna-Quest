import pygame
import random

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Fenstergröße
pygame.display.set_caption("Infinite Otterndorf-Wanna Quest")
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Agenten-Klasse
class Agent:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.speed = 5
        self.energy = 100

    def draw(self, screen):
        # Einfacher Stickman: Kopf und Körper
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)  # Kopf
        pygame.draw.line(screen, self.color, (self.x, self.y + 10), (self.x, self.y + 30), 2)  # Körper
        # Energie-Anzeige
        font = pygame.font.SysFont('arial', 15)
        text = font.render(f"{self.name}: {self.energy}", True, WHITE)
        screen.blit(text, (self.x - 20, self.y - 30))

    def move(self, map_width, map_height):
        # Zufällige Bewegung (später Reinforcement Learning)
        dx = random.choice([-self.speed, 0, self.speed])
        dy = random.choice([-self.speed, 0, self.speed])
        self.x = max(0, min(self.x + dx, map_width - 10))
        self.y = max(0, min(self.y + dy, map_height - 10))

# Map-Einstellungen
map_width = 2000
map_height = 2000
camera_x = 0
camera_y = 0

# Agenten erstellen
simple_d = Agent(400, 300, BLUE, "Simple D")
irsan_ai = Agent(450, 300, RED, "Irsan AI")

# Spielschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Agenten bewegen
    simple_d.move(map_width, map_height)
    irsan_ai.move(map_width, map_height)

    # Kamera zentriert auf Simple D
    camera_x = simple_d.x - 400  # Bildschirmmitte
    camera_y = simple_d.y - 300
    camera_x = max(0, min(camera_x, map_width - 800))
    camera_y = max(0, min(camera_y, map_height - 600))

    # Zeichnen
    screen.fill(BLACK)  # Hintergrund
    # Map zeichnen (später Sektoren wie Wälder hinzufügen)
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, map_width, map_height))
    # Agenten zeichnen
    simple_d.draw(screen)
    irsan_ai.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()