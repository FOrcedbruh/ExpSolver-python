import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from sympy import symbols, Eq, solve
import re

class NonlinearEquationSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Решение нелинейных уравнений')
        self.setStyleSheet("background-color: #343a40; font-family: Arial, sans-serif; color: #fff")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel('Введите нелинейное уравнение:')
        self.label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(self.label)

        self.equation_input = QLineEdit(self)
        self.equation_input.setPlaceholderText('Например: x**2 - 4')
        self.equation_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px;")
        layout.addWidget(self.equation_input)

        self.solve_button = QPushButton('Решить', self)
        self.solve_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; font-size: 16px; border: none; border-radius: 5px;")
        self.solve_button.clicked.connect(self.solve_equation)
        layout.addWidget(self.solve_button)

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px; background-color: #343a40;")
        layout.addWidget(self.result_text)

        self.reset_button = QPushButton("Сбросить", self)
        self.reset_button.setStyleSheet("background: #eee; color: #007BFF; padding: 5px 20px")
        self.reset_button.clicked.connect(self.reset_handler)
        layout.addWidget(self.reset_button)
        

        self.setLayout(layout)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)       
        msg_box.setText("Ошибка")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def preprocess_equation(self, equation_str):
        equation_str = equation_str.replace('^', '**')
        equation_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation_str)
        return equation_str

    def solve_equation(self):
        equation_str = self.equation_input.text()
        try:
            equation_str = self.preprocess_equation(equation_str)
            x = symbols('x')
            left, right = equation_str.split('=')
            equation = Eq(eval(left), eval(right))
            solutions = solve(equation, x)
            self.result_text.setPlainText(f'Корни: {solutions}')
        except Exception as e:
            self.show_error_message(str(e))
            

    def reset_handler(self):
        self.equation_input.clear()
        self.result_text.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = NonlinearEquationSolver()
    solver.resize(440, 400)
    solver.show()
    sys.exit(app.exec_())