from Game import Game
from Menu import Menu


class GameEngine:
    def run(self):
        while True:
            menu = Menu()
            menu.run()
            sizes = menu.get_size()
            g = Game(*sizes)
            g.run()