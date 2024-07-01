import random

class Hero:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 20

    def attack(self, other):
        damage = random.randint(0, self.attack_power)
        other.health -= damage
        print(f"{self.name} атакует {other.name} и наносит {damage} урона.")

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name}: здоровье = {self.health}"

class Game:
    def __init__(self, player_name):
        self.player = Hero(player_name)
        self.computer = Hero("Компьютер")

    def start(self):
        print("Игра началась!")
        print(self.player)
        print(self.computer)

        while self.player.is_alive() and self.computer.is_alive():
            self.player_turn()
            if self.computer.is_alive():
                self.computer_turn()
            print(self.player)
            print(self.computer)

        self.show_winner()

    def player_turn(self):
        input("Нажмите Enter, чтобы атаковать...")
        self.player.attack(self.computer)

    def computer_turn(self):
        print("Компьютер атакует...")
        self.computer.attack(self.player)

    def show_winner(self):
        if self.player.is_alive():
            print("Вы победили!")
        else:
            print("Вы проиграли!")

if __name__ == "__main__":
    player_name = input("Введите имя вашего героя: ")
    game = Game(player_name)
    game.start()
