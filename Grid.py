from random import randint  # Импортируем функцию randint из модуля random
import pygame  # Импортируем модуль pygame
# Импорт необходимых модулей
from Cell import Cell  # Импортируем класс Cell из модуля cell

from collections import deque


# Определяем класс Grid (Сетка)
class Grid:
    def __init__(self, x, y, w, h, board_size, bombs_cnt) -> None:
        # Инициализация прямоугольника сетки
        self.rect = pygame.Rect(x, y, w, h)
        self.board_size = board_size  # Размер сетки (доски)
        self.bombs_cnt = bombs_cnt  # Количество бомб, которые нужно разместить
        self.cell_h = self.rect.height / self.board_size  # Высота каждой ячейки
        self.cell_w = self.rect.width / self.board_size  # Ширина каждой ячейки
        self.cells = []  # Список для хранения ячеек
        self.bombs_is_planting = False  # Флаг для проверки, были ли размещены бомбы

        self.cells_excavated_cnt = 0    # количество раскопаных бомб

        Cell.load_resources(self.cell_w, self.cell_h)   # загружаем ресурсы для ячеек (staticmethod)

        # Создаем ячейки в сетке
        for i in range(self.board_size):
            tmp_block = []  # Временный список для хранения ряда ячеек
            for j in range(self.board_size):
                x_pos = self.rect.x + j * self.cell_w  # Вычисляем позицию x ячейки
                y_pos = self.rect.y + i * self.cell_h  # Вычисляем позицию y ячейки
                tmp_block.append(Cell(x_pos, y_pos, self.cell_w, self.cell_h))  # Создаем ячейку и добавляем в ряд
            self.cells.append(tmp_block)  # Добавляем ряд в сетку

    # Вычисляем индекс ячейки в сетке по координатам
    def calc_cell_index(self, x, y):
        return [int((y - self.rect.y) // self.cell_h), int((x - self.rect.x) // self.cell_w)]

    # Размещение бомб в сетке
    def planting_bombs(self, x, y):
        cnt = 0  # Счетчик количества размещенных бомб
        pushed_cell_ind = self.calc_cell_index(x, y)  # Получаем индекс нажатой ячейки
        while cnt < self.bombs_cnt:
            i_ind = randint(0, self.board_size - 1)  # Случайный индекс ряда
            j_ind = randint(0, self.board_size - 1)  # Случайный индекс столбца
            if pushed_cell_ind != [i_ind, j_ind] and not self.cells[i_ind][j_ind].is_bomb():
                self.cells[i_ind][j_ind].set_bomb()  # Устанавливаем бомбу в ячейке
                cnt += 1  # Увеличиваем счетчик
        self.bombs_is_planting = True  # Устанавливаем флаг, что бомбы были размещены

    # Получаем координаты ячеек вокруг заданной ячейки
    def get_cors_around(self, i_ind, j_ind):
        cors = []  # Список для хранения координат
        for i in range(i_ind - 1, i_ind + 2):
            for j in range(j_ind - 1, j_ind + 2):
                # добавляем все координаты которые в поле и не равняются текущим
                if min(i, j) >= 0 and max(i, j) < self.board_size and [i_ind, j_ind] != [i, j]:
                    cors.append([i, j])  # Добавляем координаты в список, если они в пределах сетки
        return cors

    # Подсчитываем количество бомб вокруг заданной ячейки
    def bombs_cnt_around(self, i_ind, j_ind) -> int:
        bombs_cnt = 0  # Счетчик бомб
        for i, j in self.get_cors_around(i_ind, j_ind):
            bombs_cnt += self.cells[i][j].is_bomb()  # Увеличиваем счетчик, если в ячейке есть бомба
        return bombs_cnt

    # Обработка нажатия на ячейку
    def push(self, x, y) -> bool:
        if self.rect.collidepoint(x, y):
            if not self.bombs_is_planting:
                self.planting_bombs(x, y)  # Размещаем бомбы при первом нажатии

            cell_ind = self.calc_cell_index(x, y)  # Получаем индекс нажатой ячейки

            if self.cells[cell_ind[0]][cell_ind[1]].is_bomb():
                return True  # Игра окончена, если нажата бомба

            if self.cells[cell_ind[0]][cell_ind[1]].is_excavated():
                return False
            self.bfs_activate(cell_ind[0], cell_ind[1])  # Активируем ячейку и соседние ячейки
        return False

    # Итеративная активация ячеек с использованием BFS
    def bfs_activate(self, start_i, start_j) -> None:
        queue = deque([(start_i, start_j)])  # Очередь для хранения координат ячеек, которые нужно обработать
        visited = set((start_i, start_j))  # Множество для отслеживания посещенных ячеек

        while queue:  # Пока очередь не пуста
            i_ind, j_ind = queue.popleft()  # Извлекаем ячейку из очереди

            if self.cells[i_ind][j_ind].is_bomb():  # Пропускаем ячейку, если в ней есть бомба
                continue

            bombs_cnt = self.bombs_cnt_around(i_ind, j_ind)  # Получаем количество бомб вокруг ячейки

            if bombs_cnt != 0:  # Если вокруг ячейки есть бомбы, устанавливаем число и продолжаем
                self.cells[i_ind][j_ind].set_num(bombs_cnt)
                self.cells_excavated_cnt += 1
                continue

            self.cells[i_ind][j_ind].push()  # Раскрываем ячейку
            self.cells_excavated_cnt += 1

            cors_around = self.get_cors_around(i_ind, j_ind)  # Получаем координаты соседних ячеек

            for i, j in cors_around:  # Проходим по соседним ячейкам
                if (i, j) not in visited and not self.cells[i][j].is_excavated():  # Если ячейка не посещена и не выкопана
                    queue.append((i, j))  # Добавляем ячейку в очередь
                    visited.add((i, j))  # Помечаем ячейку как посещенную

    def set_flag(self, x, y) -> None:
        cell_ind = self.calc_cell_index(x, y)  # Получаем индекс нажатой ячейки
        self.cells[cell_ind[0]][cell_ind[1]].set_flag()

    def is_win(self):
        return self.cells_excavated_cnt == self.board_size ** 2 - self.bombs_cnt

    # Отрисовка сетки
    def draw(self, window) -> None:
        for block in self.cells:
            for cell in block:
                cell.draw(window)  # Отрисовываем каждую ячейку на окне

    # Отрисовка сетки с демонстрайией бомб
    def draw_true(self, window) -> None:
        for block in self.cells:
            for cell in block:
                cell.draw_true(window)  # Отрисовываем каждую ячейку на окне