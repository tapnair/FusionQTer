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


class QTEventThread(apper.Fusion360CustomThread):

    def custom_event_received(self, event_dict):
        ao = apper.AppObjects()

        msg = event_dict['msg']
        ao.ui.messageBox('Message received: ' + msg)

    def run_in_thread(self, thread, event_id, input_data=None):

        address = ('localhost', 6000)
        with Client(address, authkey=b'secret password') as conn:
            while not self.stop_flag.wait(5):
                msg = conn.recv()[0]
                args = {'msg': msg}
                self.fire_event(args)


