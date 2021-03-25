"""
QTEventThread.py
================
Python module for creating a thread to listen for events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2021 by Patrick Rainsberry.
:license: MIT, see LICENSE for more details.
"""
from ..apper import apper
from multiprocessing.connection import Client
from .. import config
from . import utils


# This class leverages the apper implementation of a Fusion 360 Custom Event and spawns a new thread
class QTEventThread(apper.Fusion360CustomThread):
    # This function is called everytime the self.fire_event(args) is called from the run_in_thread() function
    def custom_event_received(self, event_dict):
        ao = apper.AppObjects()
        msg = event_dict['msg']
        msg_type = msg.get('type', False)

        if msg_type:
            if msg_type == 'TEXT':
                ao.ui.messageBox(f"Message received: {msg.get('text', 'No text in message')}")

            elif msg_type == 'CHANGE_PARAMETERS':
                utils.change_parameters(msg.get('parameters', []))

            elif msg_type == 'GET_PARAMETERS':
                utils.send_parameters_message()

            elif msg_type == 'GET_MASS':
                utils.send_mass_message()
        else:
            ao.ui.messageBox(f'Received unknown message: {str(msg)}')

    #  This function runs in a seperate thread and waits for messages from the external app
    def run_in_thread(self, thread, event_id, input_data=None):
        address = ('localhost', 6000)
        with Client(address, authkey=b'secret password') as conn:
            config.conn = conn
            while not self.stop_flag.isSet():
                try:
                    msg = conn.recv()
                    args = {'msg': msg}
                    self.fire_event(args)

                except EOFError:
                    self.stop_flag.set()

