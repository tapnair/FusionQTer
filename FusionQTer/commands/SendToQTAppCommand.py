"""
LaunchQTAppCommand.py
=====================
Python module for launching and restarting a QT App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2021 by Patrick Rainsberry.
:license: MIT, see LICENSE for more details.
"""
import adsk.core

from ..apper import apper
from .. import config
from . import utils


# Manually trigger the mass update event
class SendToQTAppCommand(apper.Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        # Get Mass properties for active design
        utils.send_mass_message()
