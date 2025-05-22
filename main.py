import asyncio
import platform
import random
import pygame
import math

# Pygame-Konstanten
FPS = 60
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Quest")
clock = pygame.time.Clock()

# Skill-Klasse
class Skill:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect  # z.B. {"damage": 10, "heal": 5}

# Skilltree-Klasse
class SkillTree:
    def __init__(self, role):
        if role == "Magier":
            self.skills = [
                Skill("Feuerball", {"damage": 20}),
                Skill("Heilung", {"heal": 10}),
                Skill("Schild", {"defense": 5}),
                Skill("Frost", {"damage": 15}),
                Skill("Mana", {"energy": 20})
            ]

# Agent-Klasse
class Agent:
    def __init__(self, x, y, color, name, role):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.role = role
        self.energy = 100
        self.skill_tree = SkillTree(role)
        self.selected_skills = []

    def choose_skill(self):
        if len(self.selected_skills) < 5 and random.random() < 0.1:  # Zufällige Auswahl
            available_skills = [s for s in self.skill_tree.skills if s not in self.selected_skills]
            if available_skills:
                self.selected_skills.append(random.choice(available_skills))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 1:
            self.x += dx / dist
            self.y += dy / dist

# Gegner-Klasse
class Enemy:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.health = 50 if type == "Dämon" else 30
        self.damage = 10 if type == "Dämon" else 5

    def attack(self, agent):
        agent.energy -= self.damage

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x - 10, self.y - 10, 20, 20))

# Item-Klasse
class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def apply(self, agent):
        if self.type == "Heiltrank":
            agent.energy = min(100, agent.energy + 20)

    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 5)

# Spielobjekte
agents = [Agent(100, 100, WHITE, "Simple D", "Magier")]
enemies = [Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT), "Dämon") for _ in range(2)]
items = [Item(random.randint(0, WIDTH), random.randint(0, HEIGHT), "Heiltrank") for _ in range(3)]

# Setup-Funktion
def setup():
    pass  # Hier könnte später mehr Initialisierung hinzukommen

# Update-Schleife
def update_loop():
    screen.fill((0, 0, 0))

    # Agenten-Logik
    for agent in agents:
        agent.choose_skill()
        if enemies:
            nearest_enemy = min(enemies, key=lambda e: math.hypot(e.x - agent.x, e.y - agent.y))
            agent.move_towards(nearest_enemy.x, nearest_enemy.y)
        elif items:
            nearest_item = min(items, key=lambda i: math.hypot(i.x - agent.x, i.y - agent.y))
            agent.move_towards(nearest_item.x, nearest_item.y)
        agent.draw()

    # Gegner-Logik
    for enemy in enemies[:]:
        if agents:
            nearest_agent = min(agents, key=lambda a: math.hypot(a.x - enemy.x, a.y - enemy.y))
            enemy.attack(nearest_agent)
            if nearest_agent.energy <= 0:
                agents.remove(nearest_agent)
        enemy.draw()

    # Item-Logik
    for item in items[:]:
        for agent in agents:
            if math.hypot(agent.x - item.x, agent.y - item.y) < 10:
                item.apply(agent)
                items.remove(item)
                break
        item.draw()

    pygame.display.flip()

# Hauptprogramm
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