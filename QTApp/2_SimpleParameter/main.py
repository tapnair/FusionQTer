import sys
from multiprocessing.connection import Listener, wait, Connection

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow

import parameters


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = parameters.Ui_Form()
        self.ui.setupUi(self)
        self.conn: Connection
        self.conn = None

    @Slot()
    def on_button_clicked(self):
        print(
            f'{self.ui.p1_name.text()}, {self.ui.p1_value.text()}, '
            f'{self.ui.p2_name.text()}, {self.ui.p2_value.text()}'
        )
        output = {
            'type': 'PARAMETERS',
            'object': {
                self.ui.p1_name.text(): self.ui.p1_value.text(),
                self.ui.p2_name.text(): self.ui.p2_value.text()
            }
        }
        self.conn.send(output)

    @Slot()
    def on_refresh_clicked(self):
        if self.conn.poll():
            msg = self.conn.recv()
            print(str(msg))
            self.ui.mass_display.display(msg['mass'])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # sys.exit(app.exec_())

    address = ('localhost', 6000)  # family is deduced to be 'AF_INET'

    with Listener(address, authkey=b'secret password') as listener:
        with listener.accept() as conn:
            # print('connection accepted from', listener.last_accepted)
            # conn.send(["first one", True])
            window.conn = conn
            sys.exit(app.exec_())
