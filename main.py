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
GREEN = (0, 100, 0)  # Für Wald
GRAY = (100, 100, 100)  # Für Ruinen

# Agenten-Klasse
class Agent:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.speed = 2  # Reduzierte Geschwindigkeit
        self.energy = 100

    def draw(self, screen, camera_x, camera_y):
        # Stickman relativ zur Kamera zeichnen
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), 10)  # Kopf
        pygame.draw.line(screen, self.color, (screen_x, screen_y + 10), (screen_x, screen_y + 30), 2)  # Körper
        # Energie-Anzeige
        font = pygame.font.SysFont('arial', 15)
        text = font.render(f"{self.name}: {self.energy}", True, WHITE)
        screen.blit(text, (screen_x - 20, screen_y - 30))

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

# Regionen (Wald und Ruinen)
regions = [
    {"type": "forest", "rect": pygame.Rect(0, 0, 1000, 1000), "color": GREEN},  # Wald im Nordwesten
    {"type": "ruins", "rect": pygame.Rect(1000, 1000, 1000, 1000), "color": GRAY}  # Ruinen im Südosten
]

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
    camera_x = simple_d.x - 400
    camera_y = simple_d.y - 300
    camera_x = max(0, min(camera_x, map_width - 800))
    camera_y = max(0, min(camera_y, map_height - 600))

    # Zeichnen
    screen.fill(BLACK)  # Hintergrund
    # Regionen zeichnen
    for region in regions:
        region_rect = region["rect"]
        screen_rect = pygame.Rect(region_rect.x - camera_x, region_rect.y - camera_y, region_rect.width, region_rect.height)
        pygame.draw.rect(screen, region["color"], screen_rect)
    # Agenten zeichnen
    simple_d.draw(screen, camera_x, camera_y)
    irsan_ai.draw(screen, camera_x, camera_y)

    # Mini-Map (rechte untere Ecke)
    mini_map = pygame.Surface((100, 100))
    mini_map.fill((50, 50, 50))  # Hintergrund
    for region in regions:
        scaled_rect = pygame.Rect(region["rect"].x / 20, region["rect"].y / 20, region["rect"].width / 20, region["rect"].height / 20)
        pygame.draw.rect(mini_map, region["color"], scaled_rect)
    # Agenten auf Mini-Map
    pygame.draw.circle(mini_map, BLUE, (simple_d.x / 20, simple_d.y / 20), 2)
    pygame.draw.circle(mini_map, RED, (irsan_ai.x / 20, irsan_ai.y / 20), 2)
    screen.blit(mini_map, (700, 500))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()