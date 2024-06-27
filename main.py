import pygame
import sys
import random
from abc import ABC, abstractmethod

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Indie Fighter Game")

# Загрузка изображений
BACKGROUND_IMG = pygame.image.load("img/background.png")
SWORD_IMG = pygame.image.load("img/sword.png")
BOW_IMG = pygame.image.load("img/bow.png")
FIGHTER_IMG = pygame.image.load("img/fighter.png")
MONSTER_IMG = pygame.image.load("img/monster.png")
BOSS_IMG = pygame.image.load("img/boss.png")
HEALTH_POTION_IMG = pygame.image.load("img/health_potion.png")

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

    # Метод для получения урона монстром
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return "Монстр побежден!"
        return f"У монстра осталось {self.health} здоровья."

    # Метод атаки монстра
    def attack(self, fighter):
        damage = random.randint(5, 15)
        fighter.health -= damage
        if fighter.health < 0:
            fighter.health = 0
        return f"Монстр атакует и наносит {damage} урона!"

# Класс Fighter, представляющий бойца
class Fighter:
    def __init__(self, name):
        self.name = name
        self.weapon = None
        self.health = 150
        self.lives = 1
        self.rect = FIGHTER_IMG.get_rect(center=(200, 300))

    # Метод для смены оружия бойца
    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon

    # Метод атаки бойца
    def attack(self, monster: Monster):
        if self.weapon is None:
            return "Боец без оружия не может атаковать!"
        attack_description = self.weapon.attack()
        print(f"{self.name} наносит {attack_description}.")
        return monster.take_damage(10)

    # Метод для лечения бойца
    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    # Метод для потери жизни бойцом
    def lose_life(self):
        self.lives -= 1
        self.health = 100  # Восстановление здоровья при потере жизни
        if self.lives <= 0:
            show_game_over_screen()

# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = (0, 128, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 24)

    # Метод для отрисовки кнопки
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    # Метод для обработки событий кнопки
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Функция для создания монстра в зависимости от уровня
def create_monster(level):
    health = 10 + level * 10
    x = 600
    y = 300
    if level == 5:  # Босс на 5 уровне
        return Monster(health * 2, BOSS_IMG, x, y)
    return Monster(health, MONSTER_IMG, x, y)

# Функция для отображения экрана проигрыша
def show_game_over_screen():
    game_over_font = pygame.font.SysFont(None, 72)
    game_over_text = game_over_font.render("Вы проиграли!", True, (255, 0, 0))
    retry_button = Button(WIDTH // 2 - 75, HEIGHT // 2, 150, 50, "Начать заново", main)
    exit_button = Button(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50, "Выход", sys.exit)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            retry_button.handle_event(event)
            exit_button.handle_event(event)

        WINDOW.fill((0, 0, 0))
        WINDOW.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
        retry_button.draw(WINDOW)
        exit_button.draw(WINDOW)
        pygame.display.flip()
        clock.tick(30)

# Функция для отображения экрана победы
def show_victory_screen():
    victory_font = pygame.font.SysFont(None, 72)
    victory_text = victory_font.render("Вы победили!", True, (0, 255, 0))
    retry_button = Button(WIDTH // 2 - 75, HEIGHT // 2, 150, 50, "Начать заново", main)
    exit_button = Button(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50, "Выход", sys.exit)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            retry_button.handle_event(event)
            exit_button.handle_event(event)

        WINDOW.fill((0, 0, 0))
        WINDOW.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2 - 50))
        retry_button.draw(WINDOW)
        exit_button.draw(WINDOW)
        pygame.display.flip()
        clock.tick(30)

# Основной игровой цикл
def main():
    global clock
    clock = pygame.time.Clock()
    fighter = Fighter("Боец")

    sword = Sword()
    bow = Bow()

    current_weapon = None
    game_state = {
        'level': 1,
        'monster': create_monster(1),
        'damage_text': "",
        'weapon_text': "Оружие не выбрано",
        'potion_dropped': False
    }

    font = pygame.font.SysFont(None, 28)

    # Функция выбора меча
    def select_sword():
        nonlocal current_weapon
        current_weapon = sword
        fighter.change_weapon(sword)
        game_state['weapon_text'] = "Выбран меч"
        print(f"{fighter.name} выбирает меч.")

    # Функция выбора лука
    def select_bow():
        nonlocal current_weapon
        current_weapon = bow
        fighter.change_weapon(bow)
        game_state['weapon_text'] = "Выбран лук"
        print(f"{fighter.name} выбирает лук.")

    # Функция атаки бойца
    def attack():
        if current_weapon:
            result = fighter.attack(game_state['monster'])
            game_state['damage_text'] = result
            print(result)
            if game_state['monster'].health == 0:
                game_state['potion_dropped'] = random.choice([True, False])
                if game_state['level'] < 5:
                    game_state['level'] += 1
                    game_state['monster'] = create_monster(game_state['level'])
                    game_state['damage_text'] = f"Уровень {game_state['level']}. Новый монстр!"
                    print(f"Уровень {game_state['level']}. Новый монстр!")
                else:
                    show_victory_screen()
            else:
                monster_attack_result = game_state['monster'].attack(fighter)
                game_state['damage_text'] += f" {monster_attack_result}"
                print(monster_attack_result)
                if fighter.health == 0:
                    fighter.lose_life()

    # Функция использования зелья лечения
    def use_potion():
        if game_state['potion_dropped']:
            fighter.heal(20)
            game_state['potion_dropped'] = False
            print(f"{fighter.name} использует зелье лечения.")

    # Создание кнопок
    sword_button = Button(50, 500, 100, 50, "Меч", select_sword)
    bow_button = Button(200, 500, 100, 50, "Лук", select_bow)
    attack_button = Button(350, 500, 100, 50, "Атака", attack)
    potion_button = Button(500, 500, 150, 50, "Использовать зелье", use_potion)

    # Главный цикл игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            sword_button.handle_event(event)
            bow_button.handle_event(event)
            attack_button.handle_event(event)
            potion_button.handle_event(event)

        WINDOW.blit(BACKGROUND_IMG, (0, 0))

        WINDOW.blit(FIGHTER_IMG, fighter.rect)
        WINDOW.blit(game_state['monster'].image, game_state['monster'].rect)

        if current_weapon == sword:
            WINDOW.blit(SWORD_IMG, (fighter.rect.centerx, fighter.rect.top))
        elif current_weapon == bow:
            WINDOW.blit(BOW_IMG, (fighter.rect.centerx, fighter.rect.top))

        if game_state['potion_dropped']:
            WINDOW.blit(HEALTH_POTION_IMG, (300, 300))

        sword_button.draw(WINDOW)
        bow_button.draw(WINDOW)
        attack_button.draw(WINDOW)
        potion_button.draw(WINDOW)

        # Отображение уровня
        level_text = font.render(f"Уровень: {game_state['level']}", True, (0, 0, 0))
        WINDOW.blit(level_text, (10, 10))

        # Отображение урона
        damage_text = font.render(game_state['damage_text'], True, (255, 0, 0))
        WINDOW.blit(damage_text, (10, 50))

        # Отображение выбранного оружия
        weapon_text = font.render(game_state['weapon_text'], True, (0, 0, 255))
        WINDOW.blit(weapon_text, (10, 90))

        # Отображение здоровья бойца
        health_text = font.render(f"Здоровье: {fighter.health}", True, (0, 255, 0))
        WINDOW.blit(health_text, (10, 130))

        # Отображение количества жизней бойца
        lives_text = font.render(f"Жизни: {fighter.lives}", True, (255, 255, 0))
        WINDOW.blit(lives_text, (10, 170))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
