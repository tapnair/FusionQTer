import sys
from multiprocessing.connection import Listener, Connection

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
        output = {
            'type': 'CHANGE_PARAMETERS',
            'parameters': [{
                'name': self.ui.p1_name.text(),
                'value': self.ui.p1_value.text()
            }, {
                'name': self.ui.p2_name.text(),
                'value': self.ui.p2_value.text()
            }]
        }
        self.conn.send(output)

    @Slot()
    def on_refresh_clicked(self):
        if self.conn.poll():
            msg = self.conn.recv()
            if msg['type'] == 'MASS':
                mass_value = msg.get('mass', 0.0)

                self.ui.mass_display.display(mass_value)


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
