from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import uic
import sys
import random

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        self.player_turn = True  # Player 1 starts
        self.play_against_bot = False  # Default to two-player mode
        self.difficulty_level = 'Easy'  # Default bot difficulty

        uic.loadUi('Tic_Tac_Toe_UI.ui', self)

        # Adding widgets
        self.pushButton_1 = self.findChild(QPushButton, 'pushButton')
        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        self.pushButton_3 = self.findChild(QPushButton, 'pushButton_3')
        self.pushButton_4 = self.findChild(QPushButton, 'pushButton_4')
        self.pushButton_5 = self.findChild(QPushButton, 'pushButton_5')
        self.pushButton_6 = self.findChild(QPushButton, 'pushButton_6')
        self.pushButton_7 = self.findChild(QPushButton, 'pushButton_7')
        self.pushButton_8 = self.findChild(QPushButton, 'pushButton_8')
        self.pushButton_9 = self.findChild(QPushButton, 'pushButton_9')
        self.label = self.findChild(QLabel, 'label')
        self.newGameButton = self.findChild(QPushButton, 'pushButton_10')
        self.modeSelectComboBox = self.findChild(QComboBox, 'modeSelectComboBox')
        self.difficultyComboBox = self.findChild(QComboBox, 'difficultyComboBox')

        # Connecting buttons
        self.pushButton_1.clicked.connect(lambda: self.PushingButton(self.pushButton_1))
        self.pushButton_2.clicked.connect(lambda: self.PushingButton(self.pushButton_2))
        self.pushButton_3.clicked.connect(lambda: self.PushingButton(self.pushButton_3))
        self.pushButton_4.clicked.connect(lambda: self.PushingButton(self.pushButton_4))
        self.pushButton_5.clicked.connect(lambda: self.PushingButton(self.pushButton_5))
        self.pushButton_6.clicked.connect(lambda: self.PushingButton(self.pushButton_6))
        self.pushButton_7.clicked.connect(lambda: self.PushingButton(self.pushButton_7))
        self.pushButton_8.clicked.connect(lambda: self.PushingButton(self.pushButton_8))
        self.pushButton_9.clicked.connect(lambda: self.PushingButton(self.pushButton_9))
        self.newGameButton.clicked.connect(self.NewGame)
        self.modeSelectComboBox.currentIndexChanged.connect(self.ModeChanged)
        self.difficultyComboBox.currentIndexChanged.connect(self.DifficultyChanged)

        # Set the label to display the first turn message
        self.label.setText("Player 1 (X) turn")
        
        self.show()
        self.newGameButton.hide()  # Initially hide the new game button

    def ModeChanged(self):
        mode = self.modeSelectComboBox.currentText()
        self.play_against_bot = mode == 'Play against Bot'

    def DifficultyChanged(self):
        self.difficulty_level = self.difficultyComboBox.currentText()

    def NewGame(self):
        button_list = [
            self.pushButton_1, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5, self.pushButton_6,
            self.pushButton_7, self.pushButton_8, self.pushButton_9
        ]
        for button in button_list:
            button.setText('')  # Clear the text
            button.setEnabled(True)  # Ensure all buttons are enabled
            palette = button.palette()
            palette.setColor(QPalette.Button, QColor(240, 240, 240))  # Default color
            button.setPalette(palette)
            button.setAutoFillBackground(False)

        self.label.setText("Player 1 (X) turn")
        self.newGameButton.hide()  # Hide the new game button after resetting
        self.player_turn = True  # Reset to Player 1's turn

    def Check(self):
        winning_combinations = [
            [self.pushButton_1, self.pushButton_2, self.pushButton_3],
            [self.pushButton_4, self.pushButton_5, self.pushButton_6],
            [self.pushButton_7, self.pushButton_8, self.pushButton_9],
            [self.pushButton_1, self.pushButton_4, self.pushButton_7],
            [self.pushButton_2, self.pushButton_5, self.pushButton_8],
            [self.pushButton_3, self.pushButton_6, self.pushButton_9],
            [self.pushButton_1, self.pushButton_5, self.pushButton_9],
            [self.pushButton_3, self.pushButton_5, self.pushButton_7]
        ]
        
        for combination in winning_combinations:
            text1 = combination[0].text()
            text2 = combination[1].text()
            text3 = combination[2].text()
            
            if text1 != '' and text1 == text2 == text3:
                for btn in combination:
                    palette = btn.palette()
                    palette.setColor(QPalette.Button, QColor(0, 255, 0))
                    btn.setPalette(palette)
                    btn.setAutoFillBackground(True)
                
                self.DisableButtons()
                self.newGameButton.show()
                self.label.setText(f"{text1} wins!")
                return
        
        all_filled = all(btn.text() != '' for btn in [
            self.pushButton_1, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5, self.pushButton_6,
            self.pushButton_7, self.pushButton_8, self.pushButton_9
        ])
        
        if all_filled:
            self.label.setText("It's a draw!")
            self.newGameButton.show()

    def DisableButtons(self):
        button_list = [
            self.pushButton_1, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5, self.pushButton_6,
            self.pushButton_7, self.pushButton_8, self.pushButton_9
        ]
        
        for button in button_list:
            button.setEnabled(False)

    def PushingButton(self, btn):
        if btn.text() == "":
            if self.player_turn:
                btn.setText("X")
                self.label.setText("Player 2's turn (O)")
            else:
                btn.setText("O")
                self.label.setText("Player 1's turn (X)")

            btn.setEnabled(False)
            self.Check()
            self.player_turn = not self.player_turn

            # If playing against the bot and it's the bot's turn
            if self.play_against_bot and not self.player_turn:
                self.BotMove()

    def BotMove(self):
        # Easy Level: Random valid move
        if self.difficulty_level == 'Easy':
            self.EasyBotMove()

        # Medium Level: Add blocking logic here
        elif self.difficulty_level == 'Medium':
            if not self.TryBlocking():  # Try blocking first, if no block possible, play random
                self.EasyBotMove()

        # Hard Level: Optimal move using Minimax or advanced logic
        elif self.difficulty_level == 'Hard':
            self.HardBotMove()

        self.Check()  # Check after the bot moves

    def EasyBotMove(self):
        available_buttons = [
            btn for btn in [
                self.pushButton_1, self.pushButton_2, self.pushButton_3,
                self.pushButton_4, self.pushButton_5, self.pushButton_6,
                self.pushButton_7, self.pushButton_8, self.pushButton_9
            ] if btn.text() == ""
        ]
        if available_buttons:
            selected_button = random.choice(available_buttons)
            selected_button.setText("O")
            selected_button.setEnabled(False)
            self.label.setText("Player 1's turn (X)")
            self.player_turn = True

    def TryBlocking(self):
        # Implement blocking logic to prevent player from winning
        for combination in [
            [self.pushButton_1, self.pushButton_2, self.pushButton_3],
            [self.pushButton_4, self.pushButton_5, self.pushButton_6],
            [self.pushButton_7, self.pushButton_8, self.pushButton_9],
            [self.pushButton_1, self.pushButton_4, self.pushButton_7],
            [self.pushButton_2, self.pushButton_5, self.pushButton_8],
            [self.pushButton_3, self.pushButton_6, self.pushButton_9],
            [self.pushButton_1, self.pushButton_5, self.pushButton_9],
            [self.pushButton_3, self.pushButton_5, self.pushButton_7]
        ]:
            texts = [btn.text() for btn in combination]
            if texts.count("X") == 2 and texts.count("") == 1:
                index = texts.index("")
                combination[index].setText("O")
                combination[index].setEnabled(False)
                self.label.setText("Player 1's turn (X)")
                self.player_turn = True
                return True
        return False

    def HardBotMove(self):
        # Call the minimax algorithm to determine the best move
        best_score = -float('inf')
        best_move = None
        board = [
            self.pushButton_1.text(), self.pushButton_2.text(), self.pushButton_3.text(),
            self.pushButton_4.text(), self.pushButton_5.text(), self.pushButton_6.text(),
            self.pushButton_7.text(), self.pushButton_8.text(), self.pushButton_9.text()
        ]

        for idx, btn in enumerate([self.pushButton_1, self.pushButton_2, self.pushButton_3,
                                   self.pushButton_4, self.pushButton_5, self.pushButton_6,
                                   self.pushButton_7, self.pushButton_8, self.pushButton_9]):
            if btn.text() == "":  # If the spot is available
                board[idx] = "O"
                score = self.minimax(board, False)  # Call minimax for the player
                board[idx] = ""  # Reset the spot

                if score > best_score:  # Find the best move
                    best_score = score
                    best_move = btn

        if best_move:
            best_move.setText("O")
            best_move.setEnabled(False)
            self.label.setText("Player 1's turn (X)")
            self.player_turn = True

    def minimax(self, board, is_maximizing):
        # Check for terminal states: win, lose, draw
        if self.check_winner(board) == "O":
            return 1  # Bot wins
        elif self.check_winner(board) == "X":
            return -1  # Player wins
        elif "" not in board:
            return 0  # Draw

        # Maximize for 'O' (the bot)
        if is_maximizing:
            best_score = -float('inf')
            for idx in range(9):
                if board[idx] == "":  # Is the spot available?
                    board[idx] = "O"
                    score = self.minimax(board, False)
                    board[idx] = ""  # Undo the move
                    best_score = max(score, best_score)
            return best_score

        # Minimize for 'X' (the player)
        else:
            best_score = float('inf')
            for idx in range(9):
                if board[idx] == "":  # Is the spot available?
                    board[idx] = "X"
                    score = self.minimax(board, True)
                    board[idx] = ""  # Undo the move
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, board):
        # Check rows, columns, and diagonals for a winner
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combination in winning_combinations:
            if board[combination[0]] == board[combination[1]] == board[combination[2]] != "":
                return board[combination[0]]

        return None  # No winner yet

# Initialize the application and the UI
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
