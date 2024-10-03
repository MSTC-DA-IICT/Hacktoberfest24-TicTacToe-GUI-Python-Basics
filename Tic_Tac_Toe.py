import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                             QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem,
                             QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class TicTacToeButton(QPushButton):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.setText("")
        self.setFixedSize(50, 50)
        self.setStyleSheet("font-size: 20px; font-weight: bold;")

class TicTacToeGame(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.init_game()

    def init_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.layout = QGridLayout()
        self.buttons = {}
        
        for x in range(3):
            for y in range(3):
                button = TicTacToeButton(x, y)
                button.clicked.connect(self.make_move)
                self.buttons[(x, y)] = button
                self.layout.addWidget(button, x, y)
        
        self.setLayout(self.layout)

    def make_move(self):
        if not self.parent.current_match or not self.parent.current_player:
            return

        button = self.sender()
        if button.text() == "":
            current_symbol = self.parent.player_symbols[self.parent.current_player]
            current_color = self.parent.player_colors[self.parent.current_player]
            button.setText(current_symbol)
            button.setStyleSheet(f"color: {current_color.name()}; font-size: 20px; font-weight: bold;")
            self.board[button.x][button.y] = current_symbol
            
            winner = self.check_winner()
            if winner is not None:
                self.parent.round_complete(winner)
            else:
                self.parent.switch_player()

    def check_winner(self):
        # Check rows, columns and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        # Check for draw
        if all(self.board[i][j] != '' for i in range(3) for j in range(3)):
            return 'Draw'
        
        return None

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for button in self.buttons.values():
            button.setText("")
            button.setStyleSheet("font-size: 20px; font-weight: bold;")

class PlayerSetupWidget(QWidget):
    def __init__(self, player_num):
        super().__init__()
        self.layout = QHBoxLayout()
        self.name_label = QLabel(f"Player {player_num}:")
        self.name_input = QLineEdit()
        self.color_button = QPushButton("Choose Color")
        self.color = QColor(0, 0, 0)  # Default color is black
        self.color_indicator = QLabel("■")
        self.color_indicator.setStyleSheet(f"color: {self.color.name()}; font-size: 20px;")
        
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.color_button)
        self.layout.addWidget(self.color_indicator)
        
        self.color_button.clicked.connect(self.choose_color)
        self.setLayout(self.layout)

    def choose_color(self):
        color = QColorDialog.getColor(self.color, self, "Choose Color")
        if color.isValid():
            self.color = color
            self.color_indicator.setStyleSheet(f"color: {color.name()}; font-size: 20px;")

class TournamentManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe Tournament")
        self.setMinimumSize(800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        self.game_widget = TicTacToeGame(parent=self)
        self.setup_ui()
        
        self.reset_tournament_data()

    def reset_tournament_data(self):
        self.players = []
        self.matches = []
        self.current_match = None
        self.current_player = None
        self.player_symbols = {}
        self.player_colors = {}
        self.round_scores = {}
        self.points_table = {}
        self.current_round = 0
        self.tournament_stage = "setup"

    def setup_ui(self):
        # Left side - Game and controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Player setup
        player_setup = QWidget()
        player_layout = QVBoxLayout(player_setup)
        self.player_setups = []
        for i in range(4):  # Limiting to 4 players for simplicity
            player_widget = PlayerSetupWidget(i+1)
            self.player_setups.append(player_widget)
            player_layout.addWidget(player_widget)
        player_setup.setLayout(player_layout)
        
        start_button = QPushButton("Start Tournament")
        start_button.clicked.connect(self.start_tournament)
        reset_button = QPushButton("Reset Tournament")
        reset_button.clicked.connect(self.reset_tournament)
        
        left_layout.addWidget(player_setup)
        left_layout.addWidget(self.game_widget)
        left_layout.addWidget(start_button)
        left_layout.addWidget(reset_button)
        
        # Right side - Tournament info
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.status_label = QLabel("Tournament Status: Setup")
        self.current_match_label = QLabel("Current Match: None")
        self.current_round_label = QLabel("Current Round: 0/5")
        self.round_score_label = QLabel("Round Scores: None")
        
        self.points_table_widget = QTableWidget()
        self.points_table_widget.setColumnCount(2)
        self.points_table_widget.setHorizontalHeaderLabels(["Player", "Points"])
        
        right_layout.addWidget(self.status_label)
        right_layout.addWidget(self.current_match_label)
        right_layout.addWidget(self.current_round_label)
        right_layout.addWidget(self.round_score_label)
        right_layout.addWidget(self.points_table_widget)
        
        self.main_layout.addWidget(left_widget)
        self.main_layout.addWidget(right_widget)

    def start_tournament(self):
        self.players = []
        self.player_colors = {}
        
        for setup in self.player_setups:
            name = setup.name_input.text()
            if name:
                self.players.append(name)
                self.player_colors[name] = setup.color
        
        if len(self.players) < 2:
            QMessageBox.warning(self, "Not Enough Players", "Please enter at least 2 player names.")
            return
        
        self.tournament_stage = "round-robin"
        self.matches = [(p1, p2) for i, p1 in enumerate(self.players) 
                        for p2 in self.players[i+1:]]
        self.points_table = {player: 0 for player in self.players}
        self.start_next_match()
        self.update_ui()

    def start_next_match(self):
        if not self.matches:
            self.end_tournament()
            return
        
        self.current_match = self.matches.pop(0)
        self.round_scores = {player: 0 for player in self.current_match}
        self.current_round = 0
        self.start_next_round()
        
    def start_next_round(self):
        self.current_round += 1
        self.game_widget.reset_game()
        self.player_symbols = {
            self.current_match[0]: 'X',
            self.current_match[1]: 'O'
        }
        self.current_player = self.current_match[0]
        self.update_ui()

    def switch_player(self):
        self.current_player = self.current_match[1] if self.current_player == self.current_match[0] else self.current_match[0]
        self.update_ui()

    def round_complete(self, result):
        if result == 'Draw':
            QMessageBox.information(self, "Round Complete", "This round is a draw!")
        else:
            winner = None
            for player, symbol in self.player_symbols.items():
                if symbol == result:
                    winner = player
                    break
            
            if winner is not None:
                self.round_scores[winner] += 1
                QMessageBox.information(self, "Round Complete", f"{winner} wins this round!")
        
        if self.current_round < 5:
            self.start_next_round()
        else:
            self.end_match()

    def end_match(self):
        match_winner = max(self.round_scores.items(), key=lambda x: x[1])[0]
        self.points_table[match_winner] += 5
        QMessageBox.information(self, "Match Complete", 
                               f"Match Winner: {match_winner}\nScores: {self.round_scores}")
        self.start_next_match()

    def end_tournament(self):
        winner = max(self.points_table.items(), key=lambda x: x[1])[0]
        QMessageBox.information(self, "Tournament Ended", f"Tournament Winner: {winner}")
        self.tournament_stage = "complete"
        self.current_match = None
        self.update_ui()

    def reset_tournament(self):
        self.reset_tournament_data()
        self.game_widget.reset_game()
        for setup in self.player_setups:
            setup.name_input.clear()
            setup.color = QColor(0, 0, 0)
            setup.color_indicator.setStyleSheet("color: #000000; font-size: 20px;")
        self.update_ui()

    def update_ui(self):
        self.status_label.setText(f"Tournament Status: {self.tournament_stage.capitalize()}")
        
        if self.current_match:
            self.current_match_label.setText(f"Current Match: {self.current_match[0]} vs {self.current_match[1]}")
            self.current_round_label.setText(f"Current Round: {self.current_round}/5")
            if self.current_player:
                current_symbol = self.player_symbols[self.current_player]
                current_color = self.player_colors[self.current_player].name()
                self.status_label.setText(f"Current Player: {self.current_player} "
                                         f"(<span style='color: {current_color}'>{current_symbol}</span>)")
                self.status_label.setTextFormat(Qt.RichText)
        else:
            self.current_match_label.setText("Current Match: None")
            self.current_round_label.setText("Current Round: 0/5")
        
        round_scores_text = "Round Scores: "
        if self.round_scores:
            round_scores_text += ", ".join([f"{player}: {score}" for player, score in self.round_scores.items()])
        self.round_score_label.setText(round_scores_text)
        
        self.points_table_widget.setRowCount(len(self.points_table))
        for row, (player, points) in enumerate(self.points_table.items()):
            self.points_table_widget.setItem(row, 0, QTableWidgetItem(player))
            self.points_table_widget.setItem(row, 1, QTableWidgetItem(str(points)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tournament = TournamentManager()
    tournament.show()
    sys.exit(app.exec_())