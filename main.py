import pygame
import sys
import random
from abc import ABC, abstractmethod
from console_game.battle_heroes import Game as ConsoleGame

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 360
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

# Анимация атаки
ATTACK_ANIMATION_FRAMES = [pygame.image.load(f"img/attack_{i}.png") for i in range(1, 4)]
ANIMATION_SPEED = 10  # Скорость анимации

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
        self.speed = 2  # Скорость перемещения монстра

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return "Монстр побежден!"
        return f"У монстра осталось {self.health} здоровья."

    def attack(self, fighter):
        damage = random.randint(5, 15)
        fighter.health -= damage
        if fighter.health < 0:
            fighter.health = 0
        return f"Монстр атакует и наносит {damage} урона!"

    def move(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        direction = random.choice(directions)
        self.rect.x += direction[0] * self.speed
        self.rect.y += direction[1] * self.speed

        # Ограничение движения монстра границами окна
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Класс Fighter
class Fighter:
    def __init__(self, name):
        self.name = name
        self.weapon = None
        self.health = 100
        self.lives = 3
        self.rect = FIGHTER_IMG.get_rect(center=(200, 300))
        self.speed = 5  # Скорость перемещения
        self.is_attacking = False
        self.attack_frame = 0

    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def attack(self, monster: Monster):
        if self.weapon is None:
            return "Боец без оружия не может атаковать!"
        attack_description = self.weapon.attack()
        print(f"{self.name} наносит {attack_description}.")
        self.is_attacking = True
        self.attack_frame = 0
        return monster.take_damage(10)

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def lose_life(self):
        self.lives -= 1
        self.health = 100  # Восстановление здоровья при потере жизни
        if self.lives <= 0:
            show_game_over_screen()

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Ограничение движения бойца границами окна
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update_attack_animation(self):
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame >= len(ATTACK_ANIMATION_FRAMES) * ANIMATION_SPEED:
                self.is_attacking = False
                self.attack_frame = 0

    def draw(self, surface):
        if self.is_attacking:
            frame = self.attack_frame // ANIMATION_SPEED
            surface.blit(ATTACK_ANIMATION_FRAMES[frame], self.rect.topleft)
        else:
            surface.blit(FIGHTER_IMG, self.rect.topleft)

# Класс для круглых кнопок
class RoundButton:
    def __init__(self, x, y, radius, text, callback):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.text = text
        self.callback = callback
        self.color = (0, 128, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 24)
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.rect.centerx, self.rect.centery), self.radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2,
                                    self.rect.centery - text_surface.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Функция для создания уровней
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
    retry_button = RoundButton(WIDTH // 2 - 75, HEIGHT // 2, 75, "Заново", main)
    exit_button = RoundButton(WIDTH // 2 + 75, HEIGHT // 2, 75, "Выход", sys.exit)

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
    retry_button = RoundButton(WIDTH // 2 - 75, HEIGHT // 2, 75, "Заново", main)
    exit_button = RoundButton(WIDTH // 2 + 75, HEIGHT // 2, 75, "Выход", sys.exit)

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

    def start_console_game():
        player_name = input("Введите имя вашего героя: ")
        game = ConsoleGame(player_name)
        game.start()

    def start_pygame_game():
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

        font = pygame.font.SysFont(None, 36)

        def select_sword():
            nonlocal current_weapon
            current_weapon = sword
            fighter.change_weapon(sword)
            game_state['weapon_text'] = "Выбран меч"
            print(f"{fighter.name} выбирает меч.")

        def select_bow():
            nonlocal current_weapon
            current_weapon = bow
            fighter.change_weapon(bow)
            game_state['weapon_text'] = "Выбран лук"
            print(f"{fighter.name} выбирает лук.")

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

        def use_potion():
            if game_state['potion_dropped']:
                fighter.heal(20)
                game_state['potion_dropped'] = False
                print(f"{fighter.name} использует зелье лечения.")

        # Круглые кнопки в левом нижнем углу с отступом
        button_radius = 30
        button_spacing = 10
        button_y = HEIGHT - button_radius - button_spacing

        sword_button = RoundButton(button_radius + button_spacing, button_y, button_radius, "Меч", select_sword)
        bow_button = RoundButton(2 * (button_radius + button_spacing) + button_spacing, button_y, button_radius, "Лук", select_bow)
        attack_button = RoundButton(3 * (button_radius + button_spacing) + 2 * button_spacing, button_y, button_radius, "Атака", attack)
        potion_button = RoundButton(4 * (button_radius + button_spacing) + 3 * button_spacing, button_y, button_radius, "Зелье", use_potion)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                sword_button.handle_event(event)
                bow_button.handle_event(event)
                attack_button.handle_event(event)
                potion_button.handle_event(event)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                fighter.move(-1, 0)
            if keys[pygame.K_RIGHT]:
                fighter.move(1, 0)
            if keys[pygame.K_UP]:
                fighter.move(0, -1)
            if keys[pygame.K_DOWN]:
                fighter.move(0, 1)

            game_state['monster'].move()
            fighter.update_attack_animation()

            WINDOW.blit(BACKGROUND_IMG, (0, 0))

            fighter.draw(WINDOW)
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

    print("Выберите игру:")
    print("1. Консольная игра 'Битва героев'")
    print("2. Графическая игра на Pygame")
    choice = input("Введите 1 или 2: ")

    if choice == "1":
        start_console_game()
    elif choice == "2":
        start_pygame_game()
    else:
        print("Неверный выбор")

if __name__ == "__main__":
    main()
