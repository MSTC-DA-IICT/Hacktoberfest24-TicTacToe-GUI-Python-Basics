from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5 import uic
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi('Tic_Tac_Toe_UI.ui', self)

        # Adding the widgets to the file
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

        # Initialize current player 
        self.current_player = 'X'
        # Connecting the buttons
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

        
        self.show()
        self.label.setText("Player X's turn") # Show whoes turn it is when the first game begins.
        self.newGameButton.setVisible(False) # Disable the New Game button at the very beginning.

    # New Game clears the whole Board
    def NewGame(self):
        # Reset all buttons to be empty and enabled
        buttons = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
               self.pushButton_4, self.pushButton_5, self.pushButton_6,
               self.pushButton_7, self.pushButton_8, self.pushButton_9]
    
        for button in buttons:
            button.setText('')  # Clear the text on the buttons
            button.setEnabled(True)  # Re-enable the buttons
            button.setStyleSheet("background-color: white")

        # Hide the "New Game" button while the game is on
        self.newGameButton.setVisible(False)

        # Reset the label (if you use it to show game messages)
        self.label.setText("Player X's turn")
    
        # Initialize the first player as X
        self.current_player = 'X'


    # Check button checks if X's is winning or O's is winning
    def Check(self):
        buttons = [[self.pushButton_1, self.pushButton_2, self.pushButton_3],
                   [self.pushButton_4, self.pushButton_5, self.pushButton_6],
                   [self.pushButton_7, self.pushButton_8, self.pushButton_9]]
    
        # Possible winning combinations (rows, columns, diagonals)
        winning_combinations = [
            # Rows
            [self.pushButton_1, self.pushButton_2, self.pushButton_3],
            [self.pushButton_4, self.pushButton_5, self.pushButton_6],
            [self.pushButton_7, self.pushButton_8, self.pushButton_9],
            # Columns
            [self.pushButton_1, self.pushButton_4, self.pushButton_7],
            [self.pushButton_2, self.pushButton_5, self.pushButton_8],
            [self.pushButton_3, self.pushButton_6, self.pushButton_9],
            # Diagonals
            [self.pushButton_1, self.pushButton_5, self.pushButton_9],
            [self.pushButton_3, self.pushButton_5, self.pushButton_7]
        ]
    
        for combo in winning_combinations:
            if combo[0].text() == combo[1].text() == combo[2].text() != "":
                # We have a winner
                winner = combo[0].text()
                self.label.setText(f"Player {winner} wins!")
            
                # Highlight winning buttons
                for button in combo:
                    button.setStyleSheet("background-color: yellow")
            
                # Disable all buttons except "New Game"
                for row in buttons:
                    for button in row:
                        button.setEnabled(False)
            
                # Show the "New Game" button after a win
                self.newGameButton.setVisible(True)
                return True
    
        # Check for a draw (if no empty button is found)
        if all(button.text() != '' for row in buttons for button in row):
            self.label.setText("It's a draw!")
            self.newGameButton.setVisible(True)
            # Disable all buttons except "New Game"
            for row in buttons:
                for button in row:
                    button.setEnabled(False)
            return True

        return False


    # Reaction when you push Buttons
    def PushingButton(self, btn):
        if btn.text() == '':
            # Insert the current player's mark (X or O)
            btn.setText(self.current_player)
        
            # Check for a winner
            if not self.Check():
                # If no winner, switch the player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.label.setText(f"Player {self.current_player}'s turn")
        else:
            self.label.setText("Invalid move! Try another spot.")


app = QApplication(sys.argv)

UIWindow = UI()

app.exec_()
