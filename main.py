import asyncio
import platform
import pygame
import random
import math

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Infinite Otterndorf-Wanna Quest")
clock = pygame.time.Clock()
FPS = 60

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Agenten-Klasse
class Agent:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.speed = 2
        self.energy = 100
        self.target = None
        self.in_combat = False
        self.special_action = False

    def set_target(self, map_width, map_height, other_agent=None, enemies=[]):
        if self.energy < 30 and other_agent:
            self.target = (other_agent.x, other_agent.y)  # Rufsystem
        elif self.in_combat and enemies:
            closest_enemy = min(enemies, key=lambda e: math.hypot(e.x - self.x, e.y - self.y))
            self.target = (closest_enemy.x, closest_enemy.y)
        elif self.name == "Simple D" and other_agent and random.random() < 0.7:
            self.target = (other_agent.x, other_agent.y)
        else:
            if random.random() < 0.7:
                self.target = (random.randint(1000, 2000), random.randint(1000, 2000))  # Ruinen
                self.special_action = True
            else:
                self.target = (random.randint(0, map_width), random.randint(0, map_height))
                self.special_action = False

    def move(self, map_width, map_height, other_agent=None, enemies=[]):
        if not self.target:
            self.set_target(map_width, map_height, other_agent, enemies)
        tx, ty = self.target
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist < self.speed:
            self.set_target(map_width, map_height, other_agent, enemies)
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, screen, camera_x, camera_y, zoom):
        screen_x = (self.x - camera_x) * zoom
        screen_y = (self.y - camera_y) * zoom
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), int(10 * zoom))
        pygame.draw.line(screen, self.color, (int(screen_x), int(screen_y + 10 * zoom)),
                        (int(screen_x), int(screen_y + 30 * zoom)), int(2 * zoom))
        font = pygame.font.SysFont('arial', int(15 * zoom))
        text = font.render(f"{self.name}: {self.energy}", True, WHITE)
        screen.blit(text, (int(screen_x - 20 * zoom), int(screen_y - 30 * zoom)))

# Gegner-Klasse
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = YELLOW
        self.speed = 1

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, screen, camera_x, camera_y, zoom):
        screen_x = (self.x - camera_x) * zoom
        screen_y = (self.y - camera_y) * zoom
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), int(8 * zoom))

# Map-Einstellungen
map_width = 2000
map_height = 2000

# Regionen
regions = [
    {"type": "forest", "rect": pygame.Rect(0, 0, 1000, 1000), "color": GREEN},
    {"type": "ruins", "rect": pygame.Rect(1000, 1000, 1000, 1000), "color": GRAY}
]

# Agenten und Gegner erstellen
simple_d = Agent(400, 300, BLUE, "Simple D")
irsan_ai = Agent(450, 300, RED, "Irsan AI")
enemies = [Enemy(random.randint(0, map_width), random.randint(0, map_height)) for _ in range(5)]

def get_zoom_style(dist, enemies_near, special_action):
    if enemies_near > 0:
        return "combat"
    elif special_action:
        return "focus"
    elif dist > 500:
        return "split" if dist < 1000 else "overview"
    elif dist > 200:
        return "exploration"
    else:
        return "standard"

def update_loop():
    # Gegner bewegen sich auf Simple D zu
    for enemy in enemies:
        enemy.move_towards(simple_d.x, simple_d.y)

    # Agenten bewegen und Energie aktualisieren
    enemies_near_simple_d = sum(1 for e in enemies if math.hypot(e.x - simple_d.x, e.y - simple_d.y) < 200)
    enemies_near_irsan_ai = sum(1 for e in enemies if math.hypot(e.x - irsan_ai.x, e.y - irsan_ai.y) < 200)
    simple_d.in_combat = enemies_near_simple_d > 0
    irsan_ai.in_combat = enemies_near_irsan_ai > 0
    if simple_d.in_combat or irsan_ai.in_combat:
        simple_d.energy -= 0.1
        irsan_ai.energy -= 0.1

    simple_d.move(map_width, map_height, irsan_ai, enemies)
    irsan_ai.move(map_width, map_height, simple_d, enemies)

    # Berechne Abstand und wähle Zoom-Stil
    dist = math.hypot(simple_d.x - irsan_ai.x, simple_d.y - irsan_ai.y)
    enemies_near = max(enemies_near_simple_d, enemies_near_irsan_ai)
    special_action = simple_d.special_action or irsan_ai.special_action
    zoom_style = get_zoom_style(dist, enemies_near, special_action)

    if zoom_style == "combat":
        zoom = 1.5
        camera_x = simple_d.x - 400 / zoom if simple_d.in_combat else irsan_ai.x - 400 / zoom
        camera_y = simple_d.y - 300 / zoom if simple_d.in_combat else irsan_ai.y - 300 / zoom
    elif zoom_style == "focus":
        zoom = 2.0
        camera_x = simple_d.x - 400 / zoom if simple_d.special_action else irsan_ai.x - 400 / zoom
        camera_y = simple_d.y - 300 / zoom if simple_d.special_action else irsan_ai.y - 300 / zoom
    elif zoom_style == "split":
        screen.fill(BLACK)
        left_view = pygame.Surface((400, 600))
        right_view = pygame.Surface((400, 600))
        camera_x_left = simple_d.x - 200
        camera_y_left = simple_d.y - 300
        camera_x_right = irsan_ai.x - 200
        camera_y_right = irsan_ai.y - 300
        for region in regions:
            rect_left = pygame.Rect(region["rect"].x - camera_x_left, region["rect"].y - camera_y_left, region["rect"].width, region["rect"].height)
            rect_right = pygame.Rect(region["rect"].x - camera_x_right, region["rect"].y - camera_y_right, region["rect"].width, region["rect"].height)
            pygame.draw.rect(left_view, region["color"], rect_left)
            pygame.draw.rect(right_view, region["color"], rect_right)
        simple_d.draw(left_view, camera_x_left, camera_y_left, 1)
        irsan_ai.draw(right_view, camera_x_right, camera_y_right, 1)
        for enemy in enemies:
            enemy.draw(left_view, camera_x_left, camera_y_left, 1)
            enemy.draw(right_view, camera_x_right, camera_y_right, 1)
        screen.blit(left_view, (0, 0))
        screen.blit(right_view, (400, 0))
    elif zoom_style == "overview":
        zoom = 0.3
        mid_x = (simple_d.x + irsan_ai.x) / 2
        mid_y = (simple_d.y + irsan_ai.y) / 2
        camera_x = mid_x - (400 / zoom)
        camera_y = mid_y - (300 / zoom)
    elif zoom_style == "exploration":
        zoom = 0.5
        mid_x = (simple_d.x + irsan_ai.x) / 2
        mid_y = (simple_d.y + irsan_ai.y) / 2
        camera_x = mid_x - (400 / zoom)
        camera_y = mid_y - (300 / zoom)
    else:  # Standard
        zoom = max(0.5, min(2.0, 800 / (dist + 1)))
        mid_x = (simple_d.x + irsan_ai.x) / 2
        mid_y = (simple_d.y + irsan_ai.y) / 2
        camera_x = mid_x - (400 / zoom)
        camera_y = mid_y - (300 / zoom)

    if zoom_style != "split":
        screen.fill(BLACK)
        for region in regions:
            screen_rect = pygame.Rect(
                (region["rect"].x - camera_x) * zoom,
                (region["rect"].y - camera_y) * zoom,
                region["rect"].width * zoom,
                region["rect"].height * zoom
            )
            pygame.draw.rect(screen, region["color"], screen_rect)
        simple_d.draw(screen, camera_x, camera_y, zoom)
        irsan_ai.draw(screen, camera_x, camera_y, zoom)
        for enemy in enemies:
            enemy.draw(screen, camera_x, camera_y, zoom)

    # Mini-Map
    mini_map = pygame.Surface((102, 102))
    mini_map.fill(WHITE)
    inner_map = pygame.Surface((100, 100))
    inner_map.fill((50, 50, 50))
    for region in regions:
        scaled_rect = pygame.Rect(region["rect"].x / 20, region["rect"].y / 20,
                                region["rect"].width / 20, region["rect"].height / 20)
        pygame.draw.rect(inner_map, region["color"], scaled_rect)
    pygame.draw.circle(inner_map, BLUE, (simple_d.x / 20, simple_d.y / 20), 2)
    pygame.draw.circle(inner_map, RED, (irsan_ai.x / 20, irsan_ai.y / 20), 2)
    for enemy in enemies:
        pygame.draw.circle(inner_map, YELLOW, (enemy.x / 20, enemy.y / 20), 1)
    mini_map.blit(inner_map, (1, 1))
    screen.blit(mini_map, (698, 498))

    pygame.display.flip()

def setup():
    pass

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())