"""
main.py
=======
Standalone QT App for communicating with a Fusion 360 Add-in
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2021 by Patrick Rainsberry.
:license: MIT, see LICENSE for more details.
"""

import sys
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QLineEdit, QTextEdit)
from PySide6.QtCore import Slot, Qt
from multiprocessing.connection import Listener


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
                      "Hola Mundo", "Привет мир"]

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        self.textbox = QTextEdit()
        self.textbox.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

        self.conn = None

    @Slot()
    def magic(self):
        plain_text = self.textbox.toPlainText()
        self.conn.send(
            {
                'type': 'TEXT',
                'object': plain_text
            }
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    address = ('localhost', 6000)  # family is deduced to be 'AF_INET'

    with Listener(address, authkey=b'secret password') as listener:
        with listener.accept() as conn:
            widget.conn = conn
            sys.exit(app.exec_())


