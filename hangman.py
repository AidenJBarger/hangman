import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from hangman_ui2 import Ui_Hangman

word_bank_1 = ['apple', 'banana', 'orange', 'strawberry', 'grapefruit', 'blueberry', 'pineapple', 'kiwi', 'mango', 'watermelon']
word_bank_2 = ['elephant', 'giraffe', 'lion', 'tiger', 'cheetah', 'panda', 'bear', 'kangaroo', 'hippopotamus', 'rhinoceros']
word_bank_3 = ['aeroplane', 'bicycle', 'car', 'train', 'bus', 'motorcycle', 'boat', 'ship', 'submarine', 'spaceship']

class HangmanGame(QtWidgets.QMainWindow, Ui_Hangman):
    def __init__(self, parent=None):
        super(HangmanGame, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.generate_word)

        self.pushButton_2.clicked.connect(self.guess_letter)

        self.comboBox.addItems(["Fruits", "Animals", "Transport"])

        # game state
        self.current_word = ''
        self.current_guess = ''
        self.missed_letters = set()
        self.hangman_parts = [
            self.draw_head,
            self.draw_body,
            self.draw_left_arm,
            self.draw_right_arm,
            self.draw_left_leg,
            self.draw_right_leg
        ]
        scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setScene(scene)
        self.draw_stand(scene)

    def generate_word(self):
        word_bank_index = self.comboBox.currentIndex()
        if word_bank_index == 0:
            self.current_word = random.choice(word_bank_1)
        elif word_bank_index == 1:
            self.current_word = random.choice(word_bank_2)
        else:
            self.current_word = random.choice(word_bank_3)
        self.current_guess = '_' * len(self.current_word)
        self.missed_letters = set()
        self.textBrowser_2.setPlainText(self.current_word)
        self.update_display()

    def update_display(self):
        self.textBrowser_2.setText(' '.join(self.current_guess) + f"\n\nMissed letters: {' '.join(sorted(self.missed_letters))}")
        self.draw_hangman()

    def guess_letter(self):
        letter = self.lineEdit.text().lower()
        if self.current_word == '':
            QtWidgets.QMessageBox.warning(self, "No Word", "Generate a word to play.")
            return
        if len(letter) != 1 or not letter.isalpha():
            if letter == self.current_word:
                QtWidgets.QMessageBox.information(self, "Congratulations", "You have guessed the word!")
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid input", "Please enter a single letter.")
                return

        if letter in self.current_guess or letter in self.missed_letters:
            QtWidgets.QMessageBox.information(self, "Already guessed", "You have already guessed this letter.")
            return

        if letter in self.current_word:
            self.current_guess = ''.join([c if c == letter or self.current_guess[i] != '_' else '_' for i, c in enumerate(self.current_word)])
            if '_' not in self.current_guess:
                QtWidgets.QMessageBox.information(self, "Congratulations", "You have guessed the word!")
        else:
            self.missed_letters.add(letter)

        self.update_display()
        self.lineEdit.clear()

    def draw_hangman(self):
        scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setScene(scene)
        self.draw_stand(scene)

        for i, part in enumerate(self.hangman_parts[:len(self.missed_letters)]):
            part(scene)

    def draw_stand(self, scene):
        scene.addLine(30, 120, 100, 120, pen=QtGui.QPen(QtCore.Qt.black))
        scene.addLine(65, 20, 65, 120, pen=QtGui.QPen(QtCore.Qt.black))
        scene.addLine(65, 20, 100, 20, pen=QtGui.QPen(QtCore.Qt.black))
        scene.addLine(100, 20, 100, 35, pen=QtGui.QPen(QtCore.Qt.black))


    def draw_head(self, scene):
        scene.addEllipse(90, 35, 20, 20, pen=QtGui.QPen(QtCore.Qt.black))

    def draw_body(self, scene):
        scene.addLine(100, 55, 100, 85, pen=QtGui.QPen(QtCore.Qt.black))

    def draw_left_arm(self, scene):
        scene.addLine(100, 60, 90, 75, pen=QtGui.QPen(QtCore.Qt.black))

    def draw_right_arm(self, scene):
        scene.addLine(100, 60, 110, 75, pen=QtGui.QPen(QtCore.Qt.black))

    def draw_left_leg(self, scene):
        scene.addLine(100, 85, 90, 105, pen=QtGui.QPen(QtCore.Qt.black))

    def draw_right_leg(self, scene):
        scene.addLine(100, 85, 110, 105, pen=QtGui.QPen(QtCore.Qt.black))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())
