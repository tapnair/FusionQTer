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
        # Build the message with the name and value to send to Fusion 360
        # If there is a parameter with the name it will be updated to the value
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

        # Send the message to Fusion 360
        self.conn.send(output)

    @Slot()
    def on_refresh_clicked(self):
        # You must manually click the "Send Mass to QT" button in the Fusion 360 add-in
        if self.conn.poll():
            msg = self.conn.recv()
            if msg['type'] == 'MASS':
                mass_value = msg.get('mass', 0.0)
                self.ui.mass_display.display(mass_value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
    with Listener(address, authkey=b'secret password') as listener:
        with listener.accept() as conn:
            window.conn = conn
            sys.exit(app.exec_())
