import tkinter as tk
import tkinter.messagebox as messagebox
from time import sleep


class LabelFrame(tk.LabelFrame):
    def __init__(self, master, name):
        super().__init__(master, text=name)
        self.PADX = 5
        self.PADY = 2

    def active(self):
        for child in self.winfo_children():
            child.configure(state='normal')

    def disable(self):
        for child in self.winfo_children():
            child.configure(state='disable')


class FrameSettings(tk.Toplevel):
    def __init__(self, parent):
        self.WINDOW_SIZE = {'width': '210', 'height': '270'}
        self.WINDOW_COORDS = {'x': str(parent.winfo_rootx() + 100), 'y': str(parent.winfo_rooty() + 80)}
        self.TITLE = 'Settings'
        self.PADX = 5
        self.PADY = 2

        super().__init__()

        self.title(self.TITLE)
        self.geometry('{width}x{height}+{x}+{y}'.format(**self.WINDOW_SIZE, **self.WINDOW_COORDS))
        self.resizable(False, False)
        self.overrideredirect(False)  # True without border
        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.labelframe_name = LabelFrame(self, 'Name')
        self.name = tk.StringVar()
        self.name.set(parent.gamer_name)
        self.labelframe_name.entry_name = tk.Entry(self.labelframe_name, textvariable=self.name)
        self.labelframe_name.entry_name.grid(column=0,
                                             row=0,
                                             sticky='NWES',
                                             padx=self.PADX,
                                             pady=self.PADY)
        self.labelframe_name.grid_columnconfigure(0, weight=1)
        self.labelframe_name.grid(column=0,
                                  row=0,
                                  sticky='NWES',
                                  padx=self.PADX,
                                  pady=self.PADY)
        self.labelframe_mark = LabelFrame(self, 'Mark')
        self.mark = tk.IntVar()
        self.mark.set(parent.gamer_mark)
        self.labelframe_mark.radiobutton_mark_x = tk.Radiobutton(self.labelframe_mark, variable=self.mark, value=1,
                                                                 text='x')
        self.labelframe_mark.radiobutton_mark_x.grid(column=0,
                                                     row=0,
                                                     sticky='NWES',
                                                     padx=self.PADX,
                                                     pady=self.PADY)
        self.labelframe_mark.radiobutton_mark_y = tk.Radiobutton(self.labelframe_mark, variable=self.mark, value=2,
                                                                 text='o')
        self.labelframe_mark.radiobutton_mark_y.grid(column=0,
                                                     row=1,
                                                     sticky='NWES',
                                                     padx=self.PADX,
                                                     pady=self.PADY)
        self.labelframe_mark.grid(column=0,
                                  row=1,
                                  sticky='NWES',
                                  padx=self.PADX,
                                  pady=self.PADY)
        self.labelframe_turn_first = LabelFrame(self, 'Turn first')
        self.turn_first = tk.IntVar()
        self.turn_first.set(parent.game.turn_first)
        self.labelframe_turn_first.checkbutton_turn_first = tk.Checkbutton(self.labelframe_turn_first,
                                                                           text='I am',
                                                                           variable=self.turn_first,
                                                                           onvalue=1,
                                                                           offvalue=2)
        self.labelframe_turn_first.checkbutton_turn_first.grid(column=0,
                                                               row=0,
                                                               sticky='NWES',
                                                               padx=self.PADX,
                                                               pady=self.PADY)
        self.labelframe_turn_first.grid(column=0,
                                        row=2,
                                        sticky='NWES',
                                        padx=self.PADX,
                                        pady=self.PADY)
        self.labelframe_cpu_level = LabelFrame(self, 'CPU level')
        self.cpu_level = tk.IntVar()
        self.cpu_level.set(parent.cpu_level)
        self.labelframe_cpu_level.spinbox_cpu_level = tk.Spinbox(self.labelframe_cpu_level,
                                                                 from_=parent.cpu_level_min,
                                                                 to=parent.cpu_level_max,
                                                                 textvariable=self.cpu_level,
                                                                 width=2)
        self.labelframe_cpu_level.spinbox_cpu_level.grid(column=0,
                                                         row=0,
                                                         sticky='NWES',
                                                         padx=self.PADX,
                                                         pady=self.PADY)
        self.labelframe_cpu_level.grid(column=0,
                                       row=3,
                                       sticky='NWES',
                                       padx=self.PADX,
                                       pady=self.PADY)
        self.button_ok = tk.Button(self, text='Ok', command=self.on_ok)
        self.button_ok.grid(column=0,
                            row=4,
                            sticky='NE',
                            padx=self.PADX,
                            pady=self.PADY)

        self.bind('<Return>', self.on_ok)
        self.bind('<KP_Enter>', self.on_ok)
        self.bind('<Escape>', self.on_destroy)

    def on_ok(self, event=None):
        self.master.gamer_name = self.name.get()
        self.master.game.turn = self.master.game.turn_first = self.master.game.turn_first_last = self.turn_first.get()
        self.master.gamer_mark = self.mark.get()
        try:
            self.cpu_level.get()
        except tk.TclError:
            self.cpu_level.set(self.master.cpu_level_min)
        if self.cpu_level.get() > self.master.cpu_level_max:
            self.cpu_level.set(self.master.cpu_level_max)
        if self.cpu_level.get() < self.master.cpu_level_min:
            self.cpu_level.set(self.master.cpu_level_min)
        self.master.cpu_level = self.cpu_level.get()
        self.destroy()

    def on_destroy(self, event=None):
        self.destroy()


class FrameAbout(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.WINDOW_SIZE = {'width': '210', 'height': '140'}
        self.WINDOW_COORDS = {'x': str(parent.winfo_rootx() + 100), 'y': str(parent.winfo_rooty() + 80)}
        self.TITLE = 'About'
        self.VERSION = '1.1'
        self.DATE = '06.06.2022'
        self.PADX = 5
        self.PADY = 2
        self.FONT_PROGRAM_NAME = ('Helvetica', 16, 'bold')
        self.FONT_VERSION = ('Helvetica', 8)

        self.title(self.TITLE)
        self.geometry('{width}x{height}+{x}+{y}'.format(**self.WINDOW_SIZE, **self.WINDOW_COORDS))
        self.resizable(False, False)
        self.overrideredirect(False)  # True without border
        self.transient(parent)
        self.grab_set()

        self.program_name = tk.Label(self)
        self.program_name.grid(column=0,
                               row=0,
                               sticky='NW',
                               padx=self.PADX,
                               pady=self.PADY)
        self.by = tk.Label(self)
        self.by.grid(column=0,
                     row=1,
                     sticky='NW',
                     padx=self.PADX,
                     pady=self.PADY)
        self.version = tk.Label(self)
        self.version.grid(column=0,
                          row=2,
                          sticky='NW',
                          padx=self.PADX,
                          pady=self.PADY + 10)
        self.button_ok = tk.Button(self, text='Ok', command=self.on_ok)
        self.button_ok.grid(column=0,
                            row=3,
                            sticky='NE',
                            padx=self.PADX,
                            pady=self.PADY)

        self.program_name.config(text='Move', font=self.FONT_PROGRAM_NAME)
        self.by.config(text='Program by Skrynnik Aleksey')
        self.version.config(text='ver. ' + self.VERSION + ' date: ' + self.DATE, font=self.FONT_VERSION)

        self.bind('<Return>', self.on_ok)
        self.bind('<KP_Enter>', self.on_ok)
        self.bind('<Escape>', self.on_ok)

    def on_ok(self, event=None):
        self.destroy()


class Menu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(label='Settings', underline=0, accelerator='Ctrl+S', command=self.master.on_settings)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', underline=0, accelerator='Ctrl+E', command=self.master.on_exit)
        self.add_cascade(label='File', menu=self.file_menu)

        self.help_menu = tk.Menu(self, tearoff=False)
        self.help_menu.add_separator()
        self.help_menu.add_command(label='About...', command=self.master.on_about)
        self.add_cascade(label='Help', menu=self.help_menu)

    def active(self):
        self.file_menu.entryconfig("Settings", state="normal")

    def disable(self):
        self.file_menu.entryconfig("Settings", state="disabled")


class Mark:
    def __init__(self, canvas, type_mark, col, row, bg_color):
        self.COLOR = '#fff'
        self.WIDTH = 9
        self.PADDING = 15

        self.cell_width = canvas.winfo_reqwidth() // 3
        self.bg_color = bg_color

        if type_mark == 1:
            x1 = (col - 1) * self.cell_width + self.PADDING
            y1 = (row - 1) * self.cell_width + self.PADDING
            x2 = col * self.cell_width - self.PADDING
            y2 = row * self.cell_width - self.PADDING
            line = (x1, y1, x2, y2)
            canvas.create_line(*line, fill=self.COLOR, width=self.WIDTH, tag='mark')
            x1 = col * self.cell_width - self.PADDING
            y1 = (row - 1) * self.cell_width + self.PADDING
            x2 = (col - 1) * self.cell_width + self.PADDING
            y2 = row * self.cell_width - self.PADDING
            line = (x1, y1, x2, y2)
            canvas.create_line(*line, fill=self.COLOR, width=self.WIDTH, tag='mark')
        if type_mark == 2:
            x1 = (col - 1) * self.cell_width + self.PADDING
            y1 = (row - 1) * self.cell_width + self.PADDING
            x2 = col * self.cell_width - self.PADDING
            y2 = row * self.cell_width - self.PADDING
            fill = (x1, y1, x2, y2)
            canvas.create_oval(*fill, outline=self.COLOR, fill=self.bg_color, width=self.WIDTH, tag='mark')


class LineWin:
    def __init__(self, canvas, row=0, col=0, diag=0, mark=0):
        self.COLOR = ['#f00', '#0f0']
        self.WIDTH = 10
        self.PADDING = 10
        self.PADDING_DIAG = 5

        self.cell_width = canvas.winfo_reqwidth() // 3
        self.middle = canvas.winfo_reqwidth() // 3 // 2

        if col != 0:
            x1 = (col - 1) * self.cell_width + self.middle
            y1 = self.PADDING
            x2 = (col - 1) * self.cell_width + self.middle
            y2 = canvas.winfo_reqheight() - self.PADDING
            line = (x1, y1, x2, y2)
            canvas.create_line(*line, fill=self.COLOR[mark-1], width=self.WIDTH, tag='linewin')
        if row != 0:
            x1 = self.PADDING
            y1 = (row - 1) * self.cell_width + self.middle
            x2 = canvas.winfo_reqwidth() - self.PADDING
            y2 = (row - 1) * self.cell_width + self.middle
            line = (x1, y1, x2, y2)
            canvas.create_line(*line, fill=self.COLOR[mark-1], width=self.WIDTH, tag='linewin')
        if diag == 1:
            x1 = self.PADDING
            y1 = self.PADDING
            x2 = canvas.winfo_reqwidth() - self.PADDING
            y2 = canvas.winfo_reqheight() - self.PADDING
            line = (x1, y1, x2, y2)
            canvas.create_line(*line, fill=self.COLOR[mark-1], width=self.WIDTH, tag='linewin')
        if diag == 2:
            x1 = canvas.winfo_reqwidth() - self.PADDING - self.PADDING_DIAG
            y1 = self.PADDING
            x2 = self.PADDING
            y2 = canvas.winfo_reqheight() - self.PADDING - self.PADDING_DIAG
            line = (x1, y1, x2, y2)
            canvas.create_line(*line, fill=self.COLOR[mark-1], width=self.WIDTH, tag='linewin')


class LabelFrameField(LabelFrame):
    def __init__(self, master, name):
        super().__init__(master, name=name)

        self.FIELD_BG_COLOR = '#000'
        self.FIELD_HEIGHT = 304
        self.FIELD_WIDTH = 304
        self.FIELD_LINE_COLOR = '#fff'
        self.FIELD_LINE_WIDTH = 2

        self.field = tk.Canvas(self, background=self.FIELD_BG_COLOR, height=self.FIELD_HEIGHT, width=self.FIELD_WIDTH)
        self.field.grid(column=0,
                        row=0,
                        sticky='NSEW',
                        padx=self.PADX,
                        pady=self.PADY)
        self.line_v1 = self.field.create_line(99, 10,
                                              99, 294,
                                              fill=self.FIELD_LINE_COLOR,
                                              width=self.FIELD_LINE_WIDTH)
        self.line_v2 = self.field.create_line(199, 10,
                                              199, 294,
                                              fill=self.FIELD_LINE_COLOR,
                                              width=self.FIELD_LINE_WIDTH)
        self.line_h1 = self.field.create_line(10, 99,
                                              294, 99,
                                              fill=self.FIELD_LINE_COLOR,
                                              width=self.FIELD_LINE_WIDTH)
        self.line_h2 = self.field.create_line(10, 199,
                                              294, 199,
                                              fill=self.FIELD_LINE_COLOR,
                                              width=self.FIELD_LINE_WIDTH)

        self.disable()

        self.field.bind('<Button-1>', self.on_click)

    def clear(self):
        self.field.delete('mark')
        self.field.delete('linewin')

    def on_click(self, event=None):
        if self.master.gaming and self.master.game.turn == 1:
            x = (self.field.winfo_pointerx() - self.field.winfo_rootx()) // 102 + 1
            y = (self.field.winfo_pointery() - self.field.winfo_rooty()) // 102 + 1
            if self.master.move_gamer(self.field, x, y, self.FIELD_BG_COLOR):
                if self.master.game_test_end() == 0:
                    self.master.game.turn = 2


class LabelFrameCount(LabelFrame):
    def __init__(self, master, name):
        super().__init__(master, name=name)
        self.FONT_OPPONENT = ('Helvetica', 14)
        self.FONT_COUNT = ('Helvetica', 16, 'bold')

        self.lable_user = tk.Label(self)
        self.grid_columnconfigure(0, weight=1)
        self.lable_user.grid(column=0,
                             row=0,
                             sticky='NE',
                             padx=self.PADX,
                             pady=self.PADY)
        self.lable_count = tk.Label(self)
        self.grid_columnconfigure(1, weight=1)
        self.lable_count.grid(column=1,
                              row=0,
                              sticky='NSEW',
                              padx=self.PADX,
                              pady=self.PADY)
        self.lable_cpu = tk.Label(self)
        self.grid_columnconfigure(2, weight=1)
        self.lable_cpu.grid(column=2,
                            row=0,
                            sticky='NW',
                            padx=self.PADX,
                            pady=self.PADY)

        self.disable()

    def set_count(self, name, cpu_level, count_gamer, count_cpu):
        self.lable_user.config(text=f'{name}', font=self.FONT_OPPONENT)
        self.lable_count.config(text=f'{count_gamer}:{count_cpu}', font=self.FONT_COUNT)
        self.lable_cpu.config(text=f'cpu{cpu_level}', font=self.FONT_OPPONENT)


class LabelFrameGame(LabelFrame):
    def __init__(self, master, name):
        super().__init__(master, name=name)
        self.BUTTON_WIDTH = 15

        self.button_new = tk.Button(self, text='New game', width=self.BUTTON_WIDTH, command=self.on_new)
        self.grid_columnconfigure(0, weight=1)
        self.button_new.grid(column=0,
                             row=0,
                             sticky='NE',
                             padx=self.PADX,
                             pady=self.PADY)
        self.button_end = tk.Button(self, text='End game', width=self.BUTTON_WIDTH, command=self.on_end)
        self.grid_columnconfigure(1, weight=1)
        self.button_end.grid(column=1,
                             row=0,
                             sticky='NW',
                             padx=self.PADX,
                             pady=self.PADY)

        self.disable()

    def active(self):
        self.button_new['state'] = 'disable'
        self.button_end['state'] = 'active'

    def disable(self):
        self.button_new['state'] = 'active'
        self.button_end['state'] = 'disable'

    def on_new(self):
        self.master.game_start()

    def on_end(self):
        self.master.game_end()


class FrameMain(tk.Tk):
    def __init__(self, title, window_size, gamer, cpu, game):
        super().__init__()

        self.THINK_TIMER = 3000 # 3 сек

        self.frame_about = None
        self.frame_settings = None

        self.WIN_X = (self.winfo_screenwidth() // 2) - (int(window_size['width']) // 2)
        self.WIN_Y = (self.winfo_screenheight() // 2) - (int(window_size['height']) // 2)
        self.WINDOW_COORDS = {'x': self.WIN_X, 'y': self.WIN_Y}
        self.PADX = 2
        self.PADY = 2

        self.__gamer = gamer
        self.__cpu = cpu
        self.game = game
        self.gaming = False

        self.labelframe_field = LabelFrameField(self, '')
        self.labelframe_count = LabelFrameCount(self, 'Score')
        self.set_count()
        self.labelframe_game = LabelFrameGame(self, '')

        self.labelframe_field.grid(column=0,
                                   row=0,
                                   sticky='NSEW',
                                   padx=self.PADX,
                                   pady=self.PADY)
        self.labelframe_count.grid(column=0,
                                   row=1,
                                   sticky='NSEW',
                                   padx=self.PADX,
                                   pady=self.PADY)
        self.labelframe_game.grid(column=0,
                                  row=2,
                                  sticky='NSEW',
                                  padx=self.PADX,
                                  pady=self.PADY)

        self.title(title)
        self.geometry('{width}x{height}+{x}+{y}'.format(**window_size, **self.WINDOW_COORDS))
        self.resizable(False, False)

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.bind('<Control-s>', self.on_settings)
        self.bind('<Control-e>', self.on_exit)

    @property
    def gamer_name(self):
        return self.__gamer.name

    @gamer_name.setter
    def gamer_name(self, name):
        self.__gamer.name = name
        self.set_count()

    @property
    def gamer_mark(self):
        return self.__gamer.mark

    @gamer_mark.setter
    def gamer_mark(self, mark):
        self.__gamer.mark = mark
        if self.__gamer.mark == self.game.MARK_X:
            self.cpu_mark = self.game.MARK_O
        else:
            self.cpu_mark = self.game.MARK_X

    @property
    def cpu_level(self):
        return self.__cpu.level

    @cpu_level.setter
    def cpu_level(self, cpu_level):
        self.__cpu.level = cpu_level
        self.set_count()

    @property
    def cpu_level_min(self):
        return self.__cpu.LEVEL_MIN

    @property
    def cpu_level_max(self):
        return self.__cpu.LEVEL_MAX

    @property
    def cpu_mark(self, ):
        return self.__cpu.mark

    @cpu_mark.setter
    def cpu_mark(self, mark):
        self.__cpu.mark = mark

    def set_count(self):
        self.labelframe_count.set_count(self.gamer_name, self.__cpu.level, self.game.count_gamer, self.game.count_cpu)

    def on_exit(self, event=None):
        self.quit()

    def on_about(self, event=None):
        self.frame_about = FrameAbout(self)

    def on_settings(self, event=None):
        self.frame_settings = FrameSettings(self)

    def game_test_end(self):
        result = self.game.end(self.game.field, self.labelframe_field.field)
        if result == self.gamer_mark:
            self.game.count_gamer += 1
            self.set_count()
            answer = messagebox.askyesno("You won!", "More game?")
            if answer:
                self.game_set_end()
            else:
                self.game_end()
        elif result == self.cpu_mark:
            self.game.count_cpu += 1
            self.set_count()
            answer = messagebox.askyesno("You lose!", "More game?")
            if answer:
                self.game_set_end()
            else:
                self.game_end()
        elif result == 3:
            answer = messagebox.askyesno("It\'s draw!", "More game?")
            if answer:
                self.game_set_end()
            else:
                self.game_end()
        return result

    def game_start(self):
        self.labelframe_field.active()
        self.labelframe_count.active()
        self.labelframe_game.active()
        self.menu.disable()
        self.unbind('<Control-s>')
        self.gaming = True
        self.set_count()
        self.timer()

    def game_end(self):
        self.labelframe_field.disable()
        self.labelframe_field.clear()
        self.game.new()
        self.labelframe_count.disable()
        self.labelframe_game.disable()
        self.menu.active()
        self.bind('<Control-s>', self.on_settings)
        self.gaming = False
        self.game.turn = self.game.turn_first

    def game_set_end(self):
        self.labelframe_field.clear()
        self.game.set_new()
        self.set_count()

    def move_gamer(self, field, x, y, field_bg_color):
        if self.__gamer.move(field, x, y, field_bg_color, self.game.field):
            return True
        else:
            return False

    def move_cpu(self, field, field_bg_color):
        self.__cpu.move(field, field_bg_color, self.game.field)

    def timer(self):
        if self.gaming:
            if self.game.turn == 2:
                self.move_cpu(self.labelframe_field.field, self.labelframe_field.FIELD_BG_COLOR)
                if self.game_test_end() == 0:
                    self.game.turn = 1
            self.after(self.THINK_TIMER, self.timer)
