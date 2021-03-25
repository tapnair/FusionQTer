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


# This command is only active if the option to start the thread in config.py is False
# Manually start the Fusion 360 Client Connection to the Standalone QT App Listener
class LaunchReceiverCommand(apper.Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        fusion_app: apper.FusionApp = self.fusion_app
        qt_event_thread: apper.Fusion360CustomThread = fusion_app.events[0]

        qt_event_thread.start_thread()


# Manually restart the Fusion 360 Client Connection to the Standalone QT App Listener
# Required if you restart the QT App or start a new one.
# This command kills the current Client Thread and starts a new one
class RestartReceiverCommand(apper.Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        fusion_app: apper.FusionApp = self.fusion_app
        qt_event_thread: apper.Fusion360CustomThread = fusion_app.events[0]

        qt_event_thread.restart_thread()


