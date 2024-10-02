from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QColorDialog
from PyQt5 import uic
from PyQt5.QtGui import QColor
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        self.player_turn = True  # Player 1 starts
        self.player1_color = QColor('blue')  # Default color for Player 1
        self.player2_color = QColor('red')   # Default color for Player 2

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
        
        # Color selection buttons
        self.player1_color_button = self.findChild(QPushButton, 'player1_color_button')  # Add a button for Player 1 color
        self.player2_color_button = self.findChild(QPushButton, 'player2_color_button')  # Add a button for Player 2 color

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

        # Connect color buttons to select colors
        self.player1_color_button.clicked.connect(self.SelectPlayer1Color)
        self.player2_color_button.clicked.connect(self.SelectPlayer2Color)

        # Set the label to display the first turn message
        self.label.setText("Player 1 (X) turn")

        self.show()
        self.newGameButton.hide()  # Initially hide the new game button

    def SelectPlayer1Color(self):
        color = QColorDialog.getColor() #opens dialogue box
        if color.isValid():
            self.player1_color = color
            self.player1_color_button.setStyleSheet(f"background-color: {self.player1_color.name()};")

    def SelectPlayer2Color(self):
        color = QColorDialog.getColor() #opens dialogue box
        if color.isValid():
            self.player2_color = color
            self.player2_color_button.setStyleSheet(f"background-color: {self.player2_color.name()};")

    def NewGame(self):
        button_list = [
            self.pushButton_1, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5, self.pushButton_6,
            self.pushButton_7, self.pushButton_8, self.pushButton_9
        ]
        for button in button_list:
            button.setText('')  # Clear the text
            button.setEnabled(True)  # Ensure all buttons are enabled
            button.setStyleSheet('')  # Clear any background colors

        self.newGameButton.hide()  # Hide the new game button after resetting
        self.label.setText("Player 1 (X) turn")
        self.player_turn = True  # Reset to Player 1's turn

    def Check(self):
        pass

    def PushingButton(self, btn):
        if btn.text() == "":
            # Player 1's turn (X)
            if self.player_turn:
                btn.setText("X")
                btn.setStyleSheet(f"color: {self.player1_color.name()};")
                self.label.setText("Player 2's turn (O)")
            # Player 2's turn (O)
            else:
                btn.setText("O")
                btn.setStyleSheet(f"color: {self.player2_color.name()};")
                self.label.setText("Player 1's turn (X)")

            # Switch turn
            self.player_turn = not self.player_turn
            if self.Check():
                return
        else:
            # If the spot is already taken
            self.label.setText("Invalid move! Spot already taken.")


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
