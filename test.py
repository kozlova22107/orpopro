'''
# 1) выбор размера поля - OK
# 2) подрыв соседних ячеек - OK
# 3) отображение бомб рядом с текущей ячейкой - OK
'''
import pygame
import unittest
from Grid import Grid
from Game import Game
from Cell import Cell

class TestGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((600, 720))

    def tearDown(self):
        pygame.quit()

    def test_game_initialization(self):
        game = Game(10, 10)
        self.assertIsInstance(game.grid, Grid)  # Проверяем, что grid инициализирован как объект Grid
        self.assertEqual(game.grid.board_size, 10)  # Проверяем, что размер поля равен 10
        self.assertEqual(game.grid.bombs_cnt, 10)  # Проверяем, что количество бомб равно 10

    def test_game_invalid_bombs_cnt_min(self):
        game = Game(42, -42)
        self.assertIsInstance(game.grid, Grid)  # Проверяем, что grid инициализирован как объект Grid
        self.assertEqual(game.grid.board_size, 42)  # Проверяем, что размер поля равен 42
        self.assertEqual(game.grid.bombs_cnt, 220)  # Проверяем, что количество бомб равно 220 = 42 * 42 * 1/8

    def test_game_invalid_bombs_cnt_max(self):
        game = Game(10, 10000)
        self.assertIsInstance(game.grid, Grid)  # Проверяем, что grid инициализирован как объект Grid
        self.assertEqual(game.grid.board_size, 10)  # Проверяем, что размер поля равен 10
        self.assertEqual(game.grid.bombs_cnt, 12)  # Проверяем, что количество бомб равно 12

    def test_game_invalid_board_size(self):
        game = Game(-5, 10)  # Некорректный размер поля
        self.assertIsInstance(game.grid, Grid)
        self.assertEqual(game.grid.board_size, 24)  # По умолчанию создаем поле 24x24
        self.assertEqual(game.grid.bombs_cnt, 10)  # Проверяем, что количество бомб равно 10

# =============================================================================================================

class TestGrid(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.grid = Grid(0, 60, 600, 600, 5, 5)

    def tearDown(self):
        pygame.quit()

    def test_bfs_activate_no_bombs(self):
        for row in self.grid.cells:
            for cell in row:
                cell.bomb = False

        self.grid.bfs_activate(2, 2)
        for row in self.grid.cells:
            for cell in row:
                self.assertTrue(cell.is_excavated())

    def test_bfs_activate_with_bombs(self):
        self.grid.cells[1][1].bomb = True
        self.grid.cells[2][2].bomb = True
        self.grid.bfs_activate(0, 0)

        self.assertTrue(self.grid.cells[0][0].is_excavated())
        self.assertTrue(self.grid.cells[0][1].is_excavated() is False)
        self.assertTrue(self.grid.cells[1][0].is_excavated() is False)
        self.assertTrue(self.grid.cells[1][1].is_excavated() is False)
        self.assertTrue(self.grid.cells[2][2].is_excavated() is False)

    def test_bombs_cnt_around(self):
        self.grid.cells[1][1].bomb = True
        self.grid.cells[2][2].bomb = True

        cnt = self.grid.bombs_cnt_around(1, 0)
        self.assertEqual(cnt, 1)

        cnt = self.grid.bombs_cnt_around(1, 1)
        self.assertEqual(cnt, 1)

        cnt = self.grid.bombs_cnt_around(0, 0)
        self.assertEqual(cnt, 1)

        cnt = self.grid.bombs_cnt_around(1, 2)
        self.assertEqual(cnt, 2)

    def test_push_bomb(self):
        self.grid.cells[1][1].bomb = True
        result = self.grid.push(1 * 120, 1 * 120)
        self.assertFalse(result)

    def test_push_no_bomb(self):
        self.grid.bombs_is_planting = True

        self.grid.cells[1][1].bomb = False

        result = self.grid.push(1 * 120, 1 * 120)
        self.assertFalse(result)
        self.assertTrue(self.grid.cells[1][1].is_excavated())

    def test_push_already_excavated(self):
        self.grid.cells[1][1].state_visual = "grow"

        result = self.grid.push(1 * 120, 1 * 120)
        self.assertFalse(result)

# ==================================================================================================================

class TestStateVisual(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.grid = Grid(0, 60, 600, 600, 5, 5)
        self.grid.bombs_is_planting = True

    def tearDown(self):
        pygame.quit()

    def test_bombs_cnt_around(self):
        # Расставляем бомбы вокруг центральной ячейки
        self.grid.cells[1][1].bomb = True
        self.grid.cells[1][2].bomb = True
        self.grid.cells[2][1].bomb = True

        # Проверяем количество бомб вокруг центральной ячейки
        cnt = self.grid.bombs_cnt_around(2, 2)
        self.assertEqual(cnt, 3)

    def test_push_showing_bombs_count(self):
        # Расставляем бомбы вокруг центральной ячейки
        self.grid.cells[1][1].bomb = True
        self.grid.cells[1][2].bomb = True
        self.grid.cells[2][1].bomb = True

        # Нажимаем на центральную ячейку
        self.grid.push(2 * 120 + 60, 2 * 120 + 60)

        # Проверяем, что центральная ячейка показывает правильное количество бомб вокруг
        self.assertTrue(self.grid.cells[2][2].is_excavated())
        self.assertEqual(self.grid.cells[2][2].state_visual, '3')

    def test_push_no_bombs_around(self):
        # Никаких бомб вокруг центральной ячейки
        for i in range(5):
            for j in range(5):
                self.grid.cells[i][j].bomb = False

        # Нажимаем на центральную ячейку
        self.grid.push(2 * 120 + 60, 2 * 120 + 60)

        # Проверяем, что центральная ячейка не показывает никаких бомб вокруг
        self.assertTrue(self.grid.cells[2][2].is_excavated())
        self.assertEqual(self.grid.cells[2][2].state_visual, 'grow')

if __name__ == '__main__':
    unittest.main()
