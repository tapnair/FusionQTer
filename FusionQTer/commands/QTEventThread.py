"""
QTEventThread.py
================
Python module for creating a thread to listen for events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2021 by Patrick Rainsberry.
:license: MIT, see LICENSE for more details.
"""
from ..apper import apper
from multiprocessing.connection import Client, Connection
from .. import config
from . import utils


def change_parameters(new_parameters: dict):
    ao = apper.AppObjects()

    for new_parameter in new_parameters:
        current_parameter = ao.design.userParameters.itemByName(new_parameter['name'])
        if current_parameter is not None:
            new_value = float(new_parameter['value'])
            if current_parameter.value != new_value:
                current_parameter.value = new_value

    msg = utils.get_mass_message()
    config.conn.send(msg)


def get_parameters():
    all_parameters = []
    ao = apper.AppObjects()
    parameters = ao.design.userParameters

    for parameter in parameters:
        all_parameters.append(
            {
                'name': parameter.name,
                'value': parameter.value
            }
        )
    config.conn.send(all_parameters)


class QTEventThread(apper.Fusion360CustomThread):
    def custom_event_received(self, event_dict):
        ao = apper.AppObjects()

        msg = event_dict['msg']
        if msg['type'] == 'TEXT':
            ao.ui.messageBox('Message received: ' + msg['object'])

        elif msg['type'] == 'CHANGE_PARAMETERS':
            change_parameters(msg['object'])

        elif msg['type'] == 'GET_PARAMETERS':
            get_parameters()

    def run_in_thread(self, thread, event_id, input_data=None):
        address = ('localhost', 6000)
        with Client(address, authkey=b'secret password') as conn:
            config.conn = conn
            msg = utils.get_mass_message()
            config.conn.send(msg)
            while not self.stop_flag.wait(5):
                msg = conn.recv()
                args = {'msg': msg}
                self.fire_event(args)
