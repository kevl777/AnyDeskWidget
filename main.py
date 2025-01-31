import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QHBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtWidgets import QStyle

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.always_on_top = True  # По умолчанию включено
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AnyDesk Widget')
        self.setGeometry(300, 300, 250, 150)  # Увеличенная ширина для отображения всех элементов
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint if self.always_on_top else Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.content_frame = self.create_content_frame()
        layout.addWidget(self.content_frame)
        self.setLayout(layout)

    def create_content_frame(self):
        content_frame = QFrame()
        content_frame.setFrameShape(QFrame.StyledPanel)
        content_frame.setFrameShadow(QFrame.Raised)
        content_frame.setStyleSheet("""
            background-color: rgba(50, 50, 50, 0.7);
            border-radius: 10px;
            padding: 10px;
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            border-radius: 5px;
        """)
        self.input_field.returnPressed.connect(self.handle_connect)  # Подключаемся по нажатию Enter
        layout.addWidget(self.input_field)
        self.connect_button = QPushButton('Connect')
        self.connect_button.setFont(QFont("Arial", 12))
        self.connect_button.setStyleSheet("""
            background-color: rgba(50, 50, 50, 0.7);
            color: white;
            border: none;
            border-radius: 5px;
        """)
        self.connect_button.clicked.connect(self.handle_connect)
        layout.addWidget(self.connect_button)
        content_frame.setLayout(layout)
        return content_frame

    def handle_connect(self):
        anydesk_id = self.input_field.text().replace(' ', '')
        if anydesk_id:
            password = 'your_fixed_password'  # Фиксированный пароль
            os.startfile(f'anydesk://{anydesk_id}?password={password}')

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        close_action = context_menu.addAction("Close")
        always_on_top_action = context_menu.addAction("Always on Top")
        always_on_top_action.setCheckable(True)
        always_on_top_action.setChecked(self.always_on_top)
        always_on_top_action.triggered.connect(lambda: self.toggle_always_on_top())
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == close_action:
            self.close()

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.always_on_top)
        self.show()

    def enterEvent(self, event):
        self.connect_button.setStyleSheet("""
            background-color: rgba(50, 50, 50, 0.5);
            color: white;
            border: none;
            border-radius: 5px;
        """)

    def leaveEvent(self, event):
        self.connect_button.setStyleSheet("""
            background-color: rgba(50, 50, 50, 0.7);
            color: white;
            border: none;
            border-radius: 5px;
        """)

    def closeEvent(self, event):
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Запрещаем закрытие приложения при закрытии последнего окна
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()