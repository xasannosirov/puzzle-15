import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer

from random import shuffle

class Button(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(120,120)
        self.setStyleSheet("""
            background: #4A55A2;
            border-radius: 15%;
            font-size: 70px;
            font-family: Bad Script;
            """)
        
class ExtraButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(150,60)
        self.setStyleSheet("""
            background: #F39F5A;
            border-radius: 10%;
            font-size: 25px;
            """)

class Game(QWidget):
    def __init__(self, size):
        super().__init__()
        self.size = size

        self.setWindowTitle("Game Puzzle")
        self.setStyleSheet("""
            font-size: 30px;
            background: #C5DFF8""")
        self.initUI()
        self.show()

    def initUI(self):
        self.v_box = QVBoxLayout()
        self.h_box_top = QHBoxLayout()
        self.h_box_bottom = QHBoxLayout()
        self.grid = QGridLayout()

        self.label_time = QLabel('Time: 0 s')
        self.label_moves = QLabel('Moves: 0 ')

        self.btn_restart = ExtraButton('Restart')
        self.btn_start = ExtraButton('Pause')

        self.btn_start.clicked.connect(self.start_stop)
        self.btn_restart.clicked.connect(self.Show_restart)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.restart()
        self.create_grid()
        self.connection_btn()
        self.create_window()
        if self.check_winner():
            print("Win")
            self.start_stop()
            self.btn_start.setEnabled(False)

    def create_grid(self):
        for x in range(self.size):
            for y in range(self.size):
                self.grid.addWidget(self.matrix[x][y], x, y)

    def create_window(self):
        self.h_box_top.addWidget(self.label_time)
        self.h_box_top.addStretch()
        self.h_box_top.addWidget(self.label_moves)

        self.h_box_bottom.addWidget(self.btn_restart)
        self.h_box_bottom.addStretch()
        self.h_box_bottom.addWidget(self.btn_start)

        self.v_box.addLayout(self.h_box_top)
        self.v_box.addLayout(self.grid)
        self.v_box.addLayout(self.h_box_bottom)

        self.setLayout(self.v_box)

    def restart(self):
        self.numbers = self.create_numbers(1)
        self.count_move = 0
        self.label_moves.setText(f'Moves: {self.count_move}')

        self.count = 0
        self.start = True

        i = 0
        self.matrix = list()
        for _ in range(self.size):
            row = list()
            for _ in range(self.size):
                row.append(Button(self.numbers[i]))
                i+=1
            self.matrix.append(row)
    
    def create_numbers(self, num = 0):
        nums = list(range(1, self.size*self.size))
        nums = list(map(str, nums)) + ['']
        if num:
            shuffle(nums)
        
        return nums
    
    def connection_btn(self):
        for x in range(self.size):
            for y in range(self.size):
                self.matrix[x][y].clicked.connect(self.change_position_btn)
                if not self.matrix[x][y].text():
                    self.matrix[x][y].hide()

    def change_position_btn(self):
        btn = self.sender()
        for i in range(self.size):
            for j in range(self.size):
                if btn == self.matrix[i][j]:
                    if i-1 >= 0 and self.matrix[i-1][j].text() == '': 
                        self.matrix[i-1][j].setText(btn.text())
                        self.matrix[i-1][j].show()
                        btn.setText('')
                        btn.hide()  
                        self.count_move +=1

                    elif i+1 < self.size and self.matrix[i+1][j].text() == '':                        
                        self.matrix[i+1][j].setText(btn.text())
                        self.matrix[i+1][j].show()
                        btn.setText('')
                        btn.hide()
                        self.count_move +=1

                    elif j-1 >= 0 and self.matrix[i][j-1].text() == '':
                        self.matrix[i][j-1].setText(btn.text())
                        self.matrix[i][j-1].show()
                        btn.setText('')
                        btn.hide()
                        self.count_move +=1
                    
                    elif j+1 < self.size and self.matrix[i][j+1].text() == '':                        
                        self.matrix[i][j+1].setText(btn.text())
                        self.matrix[i][j+1].show()
                        btn.setText('')
                        btn.hide()
                        self.count_move +=1  
                    self.label_moves.setText(f'Moves: {self.count_move}')
                    if self.check_winner():
                        print("Win")
                        self.start_stop()
                        self.btn_start.setEnabled(False)
                        
    def showTime(self):
        if self.start:
            self.count += 1
            text = f"Time: {self.count} s"
            self.label_time.setText(text)

    def start_stop(self):
        if self.start:
            self.btn_start.setText('Start')
            self.disable_buttons()
        else:
            self.btn_start.setText('Pause')
            self.activate_buttons()
        self.start = not self.start 

    def disable_buttons(self):
        for x in range(self.size):
            for y in range(self.size):
                self.matrix[x][y].setEnabled(False)  

    def activate_buttons(self):
        for x in range(self.size):
            for y in range(self.size):
                self.matrix[x][y].setEnabled(True)   

    def check_winner(self):
        numbers = self.create_numbers()
        i = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.matrix[x][y].text() != numbers[i]:
                    return False
                i+=1 
        return True
    
    def Show_restart(self):
        self.new = Game(self.size)
        self.close()
