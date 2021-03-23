import sys
from multiprocessing.connection import Listener, Connection

from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from DynamicParameters import Ui_MainWindow

# Data for an empty parameter table
default_data = [{
    "name": "**",
    "value": "**"
}]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.table_model = TableModel(default_data)
        self.ui.parameter_table.setModel(self.table_model)

        self.conn: Connection
        self.conn = None

    @Slot()
    def on_send_clicked(self):
        # Send new values of the parameters as defined in the table
        self.conn.send({
            'type': 'CHANGE_PARAMETERS',
            'object': self.table_model.parameters
        })

    @Slot()
    def on_refresh_clicked(self):
        # If there is a new value of mass available update the LCD display
        # Make sure to loop through any previous values that may be on the stack
        while self.conn.poll():
            msg = self.conn.recv()
            mass_value = msg.get('mass', False)
            if mass_value:
                self.ui.mass_display.display(mass_value)

    @Slot()
    def on_get_clicked(self):
        # Send Request for parameter info
        self.conn.send({'type': 'GET_PARAMETERS'})

        # Wait for response and update the table model
        self.table_model.beginResetModel()
        self.table_model.parameters = self.conn.recv()
        self.table_model.endResetModel()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self.parameters = data

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if not 0 <= index.row() < len(self.parameters):
            return None

        if role == QtCore.Qt.DisplayRole:
            name = self.parameters[index.row()]["name"]
            value = self.parameters[index.row()]["value"]
            if index.column() == 0:
                return name
            elif index.column() == 1:
                return value
        return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.parameters)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Value"
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.parameters):
            parameter = self.parameters[index.row()]
            if index.column() == 0:
                parameter["name"] = value
            elif index.column() == 1:
                parameter["value"] = value
            else:
                return False

            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        elif index.column() == 0:
            return QtCore.Qt.ItemIsEnabled
        elif index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
    with Listener(address, authkey=b'secret password') as listener:
        with listener.accept() as conn:
            window.conn = conn
            sys.exit(app.exec_())
