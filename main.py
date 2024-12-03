import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from sympy import symbols, Eq, solve
import re


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Авторизация')
        self.setStyleSheet("background-color: #343a40; font-family: Arial, sans-serif; color: #fff;")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel('Введите логин и пароль')
        self.label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Логин')
        self.username_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px;")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px;")
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Войти', self)
        self.login_button.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px; font-size: 16px; border: none; border-radius: 5px;"
        )
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == 'игорь' and password == '12345':
            self.accept_login()
        else:
            self.show_error_message('Неправильный логин или пароль')

    def accept_login(self):
        self.main_window = NonlinearEquationSolver()
        self.main_window.resize(440, 400)
        self.main_window.show()
        self.close()

    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Ошибка")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


class NonlinearEquationSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Решение нелинейных уравнений')
        self.setStyleSheet("background-color: #343a40; font-family: Arial, sans-serif; color: #fff;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.label = QLabel('Введите нелинейное уравнение:')
        self.label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(self.label)

        self.equation_input = QLineEdit(self)
        self.equation_input.setPlaceholderText('Например: x**2 - 4 = 0')
        self.equation_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px;")
        layout.addWidget(self.equation_input)

        self.solve_button = QPushButton('Решить', self)
        self.solve_button.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px; font-size: 16px; border: none; border-radius: 5px;"
        )
        self.solve_button.clicked.connect(self.solve_equation)
        layout.addWidget(self.solve_button)
        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet(
            "padding: 10px; font-size: 16px; border: 2px solid #007BFF; border-radius: 5px; background-color: #343a40;"
        )
        layout.addWidget(self.result_text)

        self.reset_button = QPushButton("Сбросить", self)
        self.reset_button.setStyleSheet("background: #eee; color: #007BFF; padding: 5px 20px;")
        self.reset_button.clicked.connect(self.reset_handler)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Ошибка")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

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
            modSolutions: list[str] = []
            for i in range(len(solutions)):
                modSolutions.append(f"x{i+1} = {solutions[i]}")
            for i in range(len(modSolutions)):
                if ("sqrt" in modSolutions[i]):
                    modSolutions[i] = modSolutions[i].replace("sqrt", "√")
            self.result_text.setPlainText(f'Корни: {modSolutions}')
        except Exception as e:
            self.show_error_message(str(e))

    def reset_handler(self):
        self.equation_input.clear()
        self.result_text.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())