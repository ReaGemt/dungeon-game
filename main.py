import pygame
import sys
from abc import ABC, abstractmethod

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Indie Fighter Game")

# Загрузка изображений
SWORD_IMG = pygame.image.load("sword.png")
BOW_IMG = pygame.image.load("bow.png")
FIGHTER_IMG = pygame.image.load("fighter.png")
MONSTER_IMG = pygame.image.load("monster.png")
BOSS_IMG = pygame.image.load("boss.png")

# Абстрактный класс для оружия
class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

# Конкретные классы оружия
class Sword(Weapon):
    def attack(self):
        return "удар мечом"

class Bow(Weapon):
    def attack(self):
        return "выстрел из лука"

# Класс Monster, представляющий монстра
class Monster:
    def __init__(self, health, image, x, y):
        self.health = health
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return "Монстр побежден!"
        return f"У монстра осталось {self.health} здоровья."

# Класс Fighter
class Fighter:
    def __init__(self, name):
        self.name = name
        self.weapon = None
        self.rect = FIGHTER_IMG.get_rect(center=(200, 300))

    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def attack(self, monster: Monster):
        if self.weapon is None:
            return "Боец без оружия не может атаковать!"
        attack_description = self.weapon.attack()
        print(f"{self.name} наносит {attack_description}.")
        return monster.take_damage(10)

# Функция для создания уровней
def create_monster(level):
    health = 10 + level * 10
    x = 600
    y = 300
    if level == 5:  # Босс на 5 уровне
        return Monster(health * 2, BOSS_IMG, x, y)
    return Monster(health, MONSTER_IMG, x, y)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    fighter = Fighter("Боец")

    sword = Sword()
    bow = Bow()

    current_weapon = None
    level = 1
    monster = create_monster(level)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_weapon = sword
                    fighter.change_weapon(sword)
                    print(f"{fighter.name} выбирает меч.")
                elif event.key == pygame.K_2:
                    current_weapon = bow
                    fighter.change_weapon(bow)
                    print(f"{fighter.name} выбирает лук.")
                elif event.key == pygame.K_SPACE:
                    if current_weapon:
                        result = fighter.attack(monster)
                        print(result)
                        if monster.health == 0:
                            if level < 5:
                                level += 1
                                monster = create_monster(level)
                                print(f"Уровень {level}. Новый монстр!")
                            else:
                                print("Вы победили босса! Игра окончена.")
                                pygame.quit()
                                sys.exit()

        WINDOW.fill((255, 255, 255))

        WINDOW.blit(FIGHTER_IMG, fighter.rect)
        WINDOW.blit(monster.image, monster.rect)

        if current_weapon == sword:
            WINDOW.blit(SWORD_IMG, (fighter.rect.centerx, fighter.rect.top))
        elif current_weapon == bow:
            WINDOW.blit(BOW_IMG, (fighter.rect.centerx, fighter.rect.top))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
