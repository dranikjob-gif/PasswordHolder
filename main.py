import sys
import os
import FirstPageWidget
import SecondPageWidget
import password_service
import security
import keyboard


from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedLayout, QMessageBox, QFrame, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QPoint, QSettings, QEasingCurve, QPropertyAnimation, QMetaObject, pyqtSlot
from PyQt6.QtGui import QIcon, QAction, QCloseEvent, QPainter, QPixmap, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            keyboard.add_hotkey("ctrl+alt+p", self.trigger_show_window)
        except Exception as e:
            print(e)

        self.setup_autostart()

        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        db_path = os.path.join(base_dir, "acc_db.db")
        self.service = password_service.PasswordManager(db_path)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)

        self.setFixedSize(400, 400)
        self.settings = QSettings("Python GUIs", 'Password holder')

        self.tray_icon = create_tray(self)
        self.setWindowIcon(self.tray_icon.icon())

        central_frame = QFrame()
        central_frame.setObjectName("MainContainer")
        self.setCentralWidget(central_frame)

        self.setStyleSheet("""
                    #MainContainer {
                        background-color: #2b2b2b;
                        border-radius: 12px;
                        border: 1px solid #3d3d3d;
                    }
                    QLabel {
                        color: #ffffff;
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
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #0b5ed7;
                    }
                    QPushButton:pressed {
                        background-color: #0a58ca;
                    }
                """)

        self.layout = QStackedLayout(central_frame)
        self.page1 = FirstPageWidget.FirstPageWidget()
        self.page2 = SecondPageWidget.SecondPageWidget()
        self.layout.addWidget(self.page1)
        self.layout.addWidget(self.page2)

        self.page1.close_button_func.connect(self.hide_animation)
        self.page2.close_button.connect(self.hide_animation)
        self.page2.change_master_password.connect(self.on_change_master_password)
        self.page1.next_page_requested.connect(self.go_to_second_page)

        self.page2.add_password.connect(self.on_add_password)
        self.page2.delete_password.connect(self.on_delete_password)
        self.page2.redact_password.connect(self.on_redact_password)

    def trigger_show_window(self) -> None:
        QMetaObject.invokeMethod(self, "show_window", Qt.ConnectionType.QueuedConnection)

    def show_animation(self) -> None:
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        end_y = screen_geometry.bottom() - self.height()
        end_x = screen_geometry.right() - self.width()

        start_x = screen_geometry.right()

        self.move(start_x, end_y)
        self.show()
        self.activateWindow()

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(350)
        self.anim.setStartValue(QPoint(start_x, end_y))
        self.anim.setEndValue(QPoint(end_x, end_y))

        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def hide_animation(self) -> None:
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        start_x = self.x()
        start_y = self.y()

        end_x = screen_geometry.right()

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(300)
        self.anim.setStartValue(QPoint(start_x, start_y))
        self.anim.setEndValue(QPoint(end_x, start_y))

        self.anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self.anim.finished.connect(self.hide)

        self.anim.start()

    @pyqtSlot()
    def show_window(self) -> None:
        if self.isVisible():
            self.hide_animation()
        else:
            self.show_animation()

    def hide_to_tray(self) -> None:
        self.hide_animation()

    def refresh_table(self) -> None:
        data = self.service.get_all_passwords()
        self.page2.set_data(data)


    def go_to_second_page(self, master_password: str) -> None:
        stored_salt = bytes(self.settings.value("master_salt"))

        self.service.initialize(master_password, stored_salt)
        self.refresh_table()
        self.layout.setCurrentIndex(1)


    def on_add_password(self, service: str, password: str):
        self.service.add_password(service, password)
        self.refresh_table()

    def on_delete_password(self, service: str):

        if not self.service.delete_password(service):
            QMessageBox.information(self, "Error", "Password with such name havent been found")
            return

        self.refresh_table()

    def on_redact_password(self, service: str, password: str):

        if not self.service.update_password(service, password):
            QMessageBox.information(self, "Error", "Password with such name havent been found")
            return

        self.refresh_table()



    def quit_app(self) -> None:
        self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.hide_to_tray()


    def on_change_master_password(self, old_mp: str, new_mp: str) -> None:

        stored_hash = bytes(self.settings.value("master_hash"))
        stored_salt = bytes(self.settings.value("master_salt"))

        if not security.verify_password(stored_hash, stored_salt, old_mp):
            QMessageBox.warning(self, "Error", "Old Master Password isnt correct")
            return

        new_hash, new_salt = security.hash_password(new_mp)

        if self.service.change_master_password(new_mp, new_salt):
            self.settings.setValue("master_hash", new_hash)
            self.settings.setValue("master_salt", new_salt)

            QMessageBox.information(self, "Success", "Password changed successfully")
            self.refresh_table()


    def setup_autostart(self) -> None:

        if not getattr(sys, "frozen", False):
            return

        autostart_key = QSettings(
            "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            QSettings.Format.NativeFormat
        )

        exe_path = f'"{sys.executable}"'

        if not autostart_key.contains("PasswordHolder"):
            autostart_key.setValue("PasswordHolder", exe_path)






def create_tray(window: MainWindow, action=tray_menu.addAction(exit_action)) -> QSystemTrayIcon:
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#0d6efd"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(2, 2, 28, 28)

    painter.setBrush(QColor("#ffffff"))
    painter.drawEllipse(12, 12, 8, 8)
    painter.end()

    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon(pixmap))
    tray_icon.setToolTip("Password Manager")

    tray_menu = QMenu()

    show_action = QAction("Show", window)
    show_action.triggered.connect(window.show_window)

    exit_action = QAction("Exit", window)
    exit_action.triggered.connect(window.quit_app)

    tray_menu.addAction(show_action)
    tray_menu.addSeparator()
    action

    tray_icon.setContextMenu(tray_menu)

    def on_tray_icon_activated(reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            window.show_window()

    tray_icon.activated.connect(on_tray_icon_activated)
    tray_icon.show()
    return tray_icon


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)


window = MainWindow()
window.show_animation()

app.exec()