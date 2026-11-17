import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QSettings, Qt, pyqtSignal
from security import hash_password, verify_password


class FirstPageWidget(QtWidgets.QWidget):

    next_page_requested = pyqtSignal(str)
    close_button_func = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.settings = QSettings("Python GUIs", 'Password holder')

        font_family= "'Segoe UI', 'Helvetica Neue', sans-serif;"

        self.close_button = QtWidgets.QPushButton("×", self)
        self.close_button.clicked.connect(self.close_button_func.emit)
        self.close_button.setGeometry(360, 10, 30, 30)
        self.close_button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #888888;
                        border: none;
                        font-size: 20px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        color: #ffffff;
                    }
                """)

        self.welcome_text = QtWidgets.QLabel(parent=self, text="Welcome")
        self.welcome_text.setGeometry(50, 45, 300, 50)
        self.welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_text.setStyleSheet("""
                    QLabel {
                        font-size: 28px;
                        font-weight: 300;
                        color: #ffffff;
                        letter-spacing: 2px;
                        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                    }
                """)

        self.error_label = QtWidgets.QLabel(parent=self, text="")
        self.error_label.setGeometry(125, 115, 150, 20)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet(f"""
            QLabel {{
                color: #ff4d4d;
                font-size: 12px;
                font-weight: 400;
                {font_family}
            }}
        """)

        self.account_password = QtWidgets.QLineEdit(parent=self)
        self.account_password.setGeometry(110, 145, 180, 32)
        self.account_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        if not self.settings.contains('master_hash'):
            self.account_password.setPlaceholderText("Create Master Password")
        else:
            self.account_password.setPlaceholderText("Enter Master Password")


        self.account_password.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: #3b3b3b;
                        color: #ffffff;
                        border: 1px solid #555555;
                        border-radius: 6px;
                        padding: 4px 8px;
                        padding-right: 28px;
                        font-size: 13px;
                        selection-background-color: #0d6efd;
                        selection-color: #ffffff;
                {font_family}
            }}
                """)


        self.toggle_btn = QtWidgets.QPushButton("👁", self.account_password)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)

        self.toggle_btn.setGeometry(150, 2, 28, 28)
        self.toggle_btn.setStyleSheet("""
                    QPushButton, QPushButton:hover, QPushButton:pressed {
                        background-color: transparent !important;
                        background: transparent !important;
                        border: none !important;
                        color: #aaaaaa;
                        font-size: 14px;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        color: #ffffff;
                    }
                """)

        self.enter_button = QtWidgets.QPushButton("Enter", self)
        self.enter_button.clicked.connect(self.handle_login)
        self.enter_button.setGeometry(160, 190, 80, 32)
        self.enter_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #0d6efd;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        font-size: 13px;
                        font-weight: 600;
                        {font_family}
                    }}
                    QPushButton:hover {{
                        background-color: #0b5ed7;
                    }}
                    QPushButton:pressed {{
                        background-color: #0a58ca;
                    }}
                """)

    def handle_login(self):
        password = self.account_password.text()

        if not password:
            self.error_label.setText("Password cannot be empty")
            return

        if not self.settings.contains('master_hash'):
            p_hash, salt = hash_password(password)
            self.settings.setValue('master_hash', p_hash)
            self.settings.setValue('master_salt', salt)

            self.error_label.setText("")
            self.account_password.clear()
            self.next_page_requested.emit(password)

        else:
            try:
                stored_hash = bytes(self.settings.value('master_hash'))
                stored_salt = bytes(self.settings.value('master_salt'))

                if verify_password(stored_hash, stored_salt, password):
                    self.error_label.setText("")
                    self.account_password.clear()
                    self.next_page_requested.emit(password)
                else:
                    self.error_label.setText("Invalid Password")
                    self.account_password.clear()
            except Exception as e:
                print(f"Login Error: {e}")
                self.error_label.setText("Login Error")

    def toggle_password_visibility(self, checked: bool):
        if checked:
            self.account_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.account_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)