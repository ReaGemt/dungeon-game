import pygame

# Инициализация Pygame
pygame.init()

# Создание изображения бойца
fighter_img = pygame.Surface((64, 64))
fighter_img.fill((0, 0, 255))  # Синий цвет
pygame.image.save(fighter_img, "fighter.png")

# Создание изображения монстра
monster_img = pygame.Surface((64, 64))
monster_img.fill((255, 0, 0))  # Красный цвет
pygame.image.save(monster_img, "monster.png")

# Создание изображения босса
boss_img = pygame.Surface((128, 128))
boss_img.fill((0, 255, 0))  # Зеленый цвет
pygame.image.save(boss_img, "boss.png")

# Создание изображения меча
sword_img = pygame.Surface((32, 32))
sword_img.fill((192, 192, 192))  # Серебряный цвет
pygame.image.save(sword_img, "sword.png")

# Создание изображения лука
bow_img = pygame.Surface((32, 32))
bow_img.fill((139, 69, 19))  # Коричневый цвет
pygame.image.save(bow_img, "bow.png")

# Создание изображения зелья лечения
potion_img = pygame.Surface((32, 32))
potion_img.fill((255, 165, 0))  # Оранжевый цвет
pygame.image.save(potion_img, "health_potion.png")

# Создание изображения фона
background_img = pygame.Surface((800, 600))
background_img.fill((173, 216, 230))  # Светло-голубой цвет
pygame.image.save(background_img, "background.png")

print("Все изображения созданы и сохранены.")
