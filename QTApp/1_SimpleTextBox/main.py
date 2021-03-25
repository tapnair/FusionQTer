"""
main.py
=======
Standalone QT App for communicating with a Fusion 360 Add-in
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2021 by Patrick Rainsberry.
:license: MIT, see LICENSE for more details.
"""

import sys
from multiprocessing.connection import Listener

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QTextEdit)


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.button = QPushButton("Send Message to Fusion 360")
        self.text = QLabel("Fusion 360 Messaging Demo 1")
        self.text.setAlignment(Qt.AlignCenter)
        self.textbox = QTextEdit()
        self.textbox.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.send_msg)

        self.conn = None

    @Slot()
    def send_msg(self):
        plain_text = self.textbox.toPlainText()
        self.conn.send({
            'type': 'TEXT',
            'text': plain_text
        })


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.resize(300, 200)
    widget.show()

    address = ('localhost', 6000)
    with Listener(address, authkey=b'secret password') as listener:
        with listener.accept() as conn:
            widget.conn = conn
            sys.exit(app.exec_())
