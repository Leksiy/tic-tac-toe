import frame
from copy import deepcopy
from random import randint


class Gamer:
    def __init__(self):
        self.mark = 1
        self.name = 'user'

    def move(self, field, x, y, field_bg_color, game_field):
        if game_field.move(x-1, y-1, self.mark):
            frame.Mark(field, self.mark, x, y, field_bg_color)
            return True
        else:
            return False


class CPU:
    def __init__(self):
        self.LEVEL_MIN = 0
        self.LEVEL_MAX = 7

        self.level = 0
        self.mark = 2

    def move(self, field, field_bg_color, game_field):
        game_field_weight = FieldWeight()
        game_field_new = deepcopy(game_field)
        for i in range(len(game_field_weight.field)):
            for j in range(len(game_field_weight.field[i])):
                if game_field.field[i][j] == 0:
                    game_field_weight.field[i][j] = 50
                else:
                    game_field_weight.field[i][j] = -1
        self.weight(game_field_weight, game_field_new, self.level, self.mark)
        mark_max = -1
        for i in range(len(game_field_weight.field)):
            for j in range(len(game_field_weight.field[i])):
                if game_field_weight.field[i][j] > mark_max:
                    mark_max = game_field_weight.field[i][j]
        cell = True
        while cell:
            x = randint(1, 3)
            y = randint(1, 3)
            if game_field_weight.field[x-1][y-1] == mark_max:
                cell = False
                game_field.move(x-1, y-1, self.mark)
                frame.Mark(field, self.mark, x, y, field_bg_color)
        del game_field_weight

    def weight(self, field_weight, field_new, level, mark):
        if level > 0:
            for i in range(len(field_weight.field)):
                for j in range(len(field_weight.field[i])):
                    if field_weight.field[i][j] == 50:
                        field_weight.field[i][j] = -1
                        field_new.move(i, j, mark)
                        if field_new.end() == mark:
                            field_weight.field[i][j] = 100
                        else:
                            level -= 1
                            field_weight_next = deepcopy(field_weight)
                            for i1 in range(len(field_weight_next.field)):
                                for j1 in range(len(field_weight_next.field[i])):
                                    if field_weight_next.field[i1][j1] > -1:
                                        field_weight_next.field[i1][j1] = 50
                            field_new_next = deepcopy(field_new)
                            if mark == 1:
                                mark = 2
                            else:
                                mark = 1
                            self.weight(field_weight_next, field_new_next, level, mark)
                            field_weight.field[i][j] = 50
                            win = False
                            win_count = 0
                            for i1 in range(len(field_weight_next.field)):
                                for j1 in range(len(field_weight_next.field[i])):
                                    if field_weight_next.field[i1][j1] == 100:
                                        win = True
                                        win_count += 1
                                    elif 10 > field_weight_next.field[i1][j1] > -1 and not win:
                                        field_weight.field[i][j] += 10
                                    elif 50 > field_weight_next.field[i1][j1] > 10 and not win:
                                        field_weight.field[i][j] += 1
                                    elif field_weight_next.field[i1][j1] > 50 and not win:
                                        field_weight.field[i][j] -= 1
                            if win:
                                field_weight.field[i][j] = 10 - win_count
                            if mark == 1:
                                mark = 2
                            else:
                                mark = 1
                            # print('cpu2', field_weight.field)
                            # print('hum', field_weight_next.field)
                            level += 1
                            del field_weight_next, field_new_next
                        field_new.remove(i, j)


class FieldWeight:
    def __init__(self):
        self.field = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]


class Field(FieldWeight):

    def __init__(self):
        super().__init__()

    def move(self, x, y, mark):
        if self.field[x][y] == 0:
            self.field[x][y] = mark
            return True
        else:
            return False

    def remove(self, x, y):
        self.field[x][y] = 0

    def end(self, canvas=None):
        result = 0
        for i in range(len(self.field)):
            if self.field[i][0] == self.field[i][1] and self.field[i][1] == self.field[i][2] and self.field[i][0] != 0:
                result = self.field[i][0]
                if canvas is not None:
                    frame.LineWin(canvas, row=0, col=i + 1, diag=0, mark=self.field[i][0])
        for i in range(len(self.field)):
            if self.field[0][i] == self.field[1][i] and self.field[1][i] == self.field[2][i] and self.field[0][i] != 0:
                result = self.field[0][i]
                if canvas is not None:
                    frame.LineWin(canvas, row=i + 1, col=0, diag=0, mark=self.field[0][i])
        if self.field[0][0] == self.field[1][1] and self.field[1][1] == self.field[2][2] and self.field[0][0] != 0:
            result = self.field[0][0]
            if canvas is not None:
                frame.LineWin(canvas, row=0, col=0, diag=1, mark=self.field[0][0])
        if self.field[2][0] == self.field[1][1] and self.field[1][1] == self.field[0][2] and self.field[1][1] != 0:
            result = self.field[1][1]
            if canvas is not None:
                frame.LineWin(canvas, row=0, col=0, diag=2, mark=self.field[1][1])
        if result == 0:
            result = 3
            for i in range(len(self.field)):
                for j in range(len(self.field[i])):
                    if self.field[i][j] == 0:
                        result = 0
        return result


class Game:
    def __init__(self):
        self.MARK_X = 1
        self.MARK_O = 2

        self.field = Field()
        self.count_cpu = 0
        self.count_gamer = 0
        self.turn_first = 1
        self.turn_first_last = 1
        self.turn = self.turn_first

    @staticmethod
    def end(field, canvas):
        result = field.end(canvas)
        return result

    def new(self):
        self.set_new()
        self.count_cpu = 0
        self.count_gamer = 0
        self.turn_first_last = self.turn = self.turn_first

    def set_new(self):
        del self.field
        self.field = Field()
        if self.turn_first_last == 1:
            self.turn = 2
            self.turn_first_last = 2
        else:
            self.turn = 1
            self.turn_first_last = 1


if __name__ == '__main__':
    WINDOW_SIZE = {'width': '325', 'height': '422'}
    APP_NAME = 'Крестики/Нолики'

    app = frame.FrameMain(APP_NAME, WINDOW_SIZE, Gamer(), CPU(), Game())
    app.mainloop()
