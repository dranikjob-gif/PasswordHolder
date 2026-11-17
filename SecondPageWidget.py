import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QShowEvent



class BaseStyleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.Dialog)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.container = QtWidgets.QFrame(self)
        self.main_layout.addWidget(self.container)

        self.layout = QtWidgets.QVBoxLayout(self.container)

        self.setStyleSheet("""

                    QDialog {
                        background: transparent;
                    }

                    QFrame {
                        background-color: #2b2b2b;
                        border-radius: 12px;
                        border: 1px solid #3d3d3d;
                    }
                    QLabel {
                        color: #ffffff;
                        font-size: 13px;
                        border: none;
                    }
                    QLineEdit {
                        background-color: #3b3b3b;
                        color: #ffffff;
                        border: 1px solid #555555;
                        border-radius: 6px;
                        padding: 4px;
                    }
                    QPushButton {
                        background-color: #0d6efd;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 5px 12px;
                    }
                    QPushButton:hover {
                        background-color: #0b5ed7;
                    }
                """)


    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        QTimer.singleShot(0, self.start_animation)


    def start_animation(self) -> None:

        parent = self.parent() or self.nativeParentWidget()
        if parent:
            parent_geo = parent.geometry()

            target_x = parent_geo.x() + (parent_geo.width() - self.width())

            end_y = parent_geo.y() - self.height() - 8
            start_y = parent_geo.y()

            self.move(target_x, start_y)

            self.anim = QPropertyAnimation(self, b"pos", self)
            self.anim.setDuration(250)
            self.anim.setStartValue(QPoint(target_x, start_y))
            self.anim.setEndValue(QPoint(target_x, end_y))
            self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.anim.start()


class SettingsDialog(BaseStyleDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setFixedSize(300, 180)

        self.layout.addWidget(QtWidgets.QLabel("New Master Password:", self))
        self.new_mp = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.new_mp)

        self.layout.addWidget(QtWidgets.QLabel("Old Master Password:", self))
        self.old_mp = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.old_mp)

        btn_layout = QtWidgets.QHBoxLayout()
        redact_mp_btn = QtWidgets.QPushButton("Change Master Password", self)
        redact_mp_btn.clicked.connect(self.accept)
        btn_layout.addWidget(redact_mp_btn)

        cancel_btn = QtWidgets.QPushButton("Cancel", self)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        self.layout.addLayout(btn_layout)

    def get_data(self):
        return self.old_mp.text(), self.new_mp.text()


class RedactPasswordDialog(BaseStyleDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Redact Password")
        self.setFixedSize(300, 180)

        self.layout.addWidget(QtWidgets.QLabel("Name:", self))
        self.service_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.service_input)

        self.layout.addWidget(QtWidgets.QLabel("Password:", self))
        self.password_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.password_input)

        btn_layout = QtWidgets.QHBoxLayout()
        self.redact_button = QtWidgets.QPushButton("Redact", self)
        self.redact_button.clicked.connect(self.accept)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        btn_layout.addWidget(self.redact_button)
        btn_layout.addWidget(self.cancel_button)

        self.layout.addLayout(btn_layout)


    def get_data(self):
        return self.service_input.text(), self.password_input.text()



class DeletePasswordDialog(BaseStyleDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Delete Password")
        self.setFixedSize(300, 110)

        self.layout.addWidget(QtWidgets.QLabel("Name:", self))
        self.service_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.service_input)

        btn_layout = QtWidgets.QHBoxLayout()
        self.delete_button = QtWidgets.QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.accept)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        btn_layout.addWidget(self.delete_button)
        btn_layout.addWidget(self.cancel_button)

        self.layout.addLayout(btn_layout)


    def get_data(self):
        return self.service_input.text()

class AddPasswordDialog(BaseStyleDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Password")
        self.setFixedSize(300, 180)


        self.layout.addWidget(QtWidgets.QLabel("Name:", self))
        self.service_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.service_input)

        self.layout.addWidget(QtWidgets.QLabel("Password:", self))
        self.password_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.password_input)

        btn_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.accept)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.cancel_button)

        self.layout.addLayout(btn_layout)


    def get_data(self):
        return self.service_input.text(), self.password_input.text()



class SecondPageWidget(QtWidgets.QWidget):

    add_password = pyqtSignal(str, str)
    delete_password = pyqtSignal(str)
    redact_password = pyqtSignal(str, str)
    close_button = pyqtSignal()
    change_master_password = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super().__init__(parent)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 15)

        # 1. Верхняя панель с кнопкой закрытия
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addStretch()

        settings_button = QtWidgets.QPushButton("Settings", self)
        settings_button.clicked.connect(self.open_settings_dialog)
        top_layout.addWidget(settings_button)

        close_btn = QtWidgets.QPushButton("×", self)
        close_btn.clicked.connect(self.close_button.emit)
        close_btn.setFixedSize(28, 28)
        # Персональный стиль для крестика, чтобы он не стал синей кнопкой
        close_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #888888;
                        border: none;
                        font-size: 18px;
                        font-weight: bold;
                        padding: 0px;
                        min-height: 0px;
                    }
                    QPushButton:hover {
                        color: #ffffff;
                    }
                """)
        top_layout.addWidget(close_btn)
        main_layout.addLayout(top_layout)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Password"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.table)

        btn_layout = QtWidgets.QHBoxLayout()

        self.add_btn = QtWidgets.QPushButton("Add", self)
        self.delete_btn = QtWidgets.QPushButton("Delete", self)
        self.redact_btn = QtWidgets.QPushButton("Redact", self)

        self.add_btn.clicked.connect(self.open_add_dialog)
        self.delete_btn.clicked.connect(self.open_delete_dialog)
        self.redact_btn.clicked.connect(self.open_redact_dialog)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.redact_btn)

        main_layout.addLayout(btn_layout)

        self.setStyleSheet("""
                    QPushButton {
                        background-color: #0d6efd;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 6px 12px;
                        min-height: 22px;
                        font-size: 12px;
                        font-weight: 600;
                        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                    }
                    QPushButton:hover {
                        background-color: #0b5ed7;
                    }
                    QPushButton:pressed {
                        background-color: #0a58ca;
                    }
                    QTableWidget {
                        background-color: #212121;
                        color: #ffffff;
                        gridline-color: #3d3d3d;
                        border: 1px solid #3d3d3d;
                        border-radius: 8px;
                        font-family: 'Segoe UI', sans-serif;
                    }
                    QHeaderView::section {
                        background-color: #1a1a1a;
                        color: #ffffff;
                        font-weight: bold;
                        border: 1px solid #3d3d3d;
                        padding: 4px;
                    }
                    QTableWidget::item:selected {
                        background-color: #0d6efd;
                        color: #ffffff;
                    }
                """)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.window())
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            old_mp, new_mp = dialog.get_data()
            if old_mp and new_mp:
                self.change_master_password.emit(old_mp, new_mp)
        dialog.deleteLater()


    def open_add_dialog(self):
        dialog = AddPasswordDialog(self.window())
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            service, password = dialog.get_data()
            if service and password:
                self.add_password.emit(service, password)

        dialog.deleteLater()


    def open_delete_dialog(self):
        dialog = DeletePasswordDialog(self.window())
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            name = dialog.get_data()
            if name:
                self.delete_password.emit(name)

        dialog.deleteLater()

    def open_redact_dialog(self):
        dialog = RedactPasswordDialog(self.window())
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            name, password = dialog.get_data()
            if name:
                self.redact_password.emit(name, password)

        dialog.deleteLater()


    def set_data(self, records):
        self.table.setRowCount(len(records))

        for row_idx, (name, password) in enumerate(records):
            item_name = QtWidgets.QTableWidgetItem(str(name))
            item_password = QtWidgets.QTableWidgetItem(str(password))
            self.table.setItem(row_idx, 0, item_name)
            self.table.setItem(row_idx, 1, item_password)


