import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle('PyQt5 Simple App')
        self.resize(300, 200)

        # Create GUI elements
        self.label = QLabel('Enter some text and press the button:', self)
        self.line_edit = QLineEdit(self)
        self.button = QPushButton('Add to List', self)
        self.list_widget = QListWidget(self)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        # Connect button click to a function
        self.button.clicked.connect(self.add_to_list)

    def add_to_list(self):
        text = self.line_edit.text()
        if text:
            self.list_widget.addItem(text)
            self.line_edit.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())
