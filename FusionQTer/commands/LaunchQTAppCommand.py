import adsk.core

import os
import subprocess

from ..apper import apper
from .. import config


@apper.lib_import(config.app_path)
def launch_qt_app():
    ao = apper.AppObjects()
    base_path = "/Users/rainsbp/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/FusionQTer/"
    # python_command = f"{base_path}QTApp/venv/bin/python"
    python_command = f"python"
    script = f"{base_path}QTApp/main.py"
    qt_command = f'{python_command} {script}'
    # print(qt_command)
    # ao.ui.messageBox(qt_command)

    # activate_command = f"source {base_path}QTApp/venv/bin/activate"
    # result = os.system(activate_command)
    # print(result)
    #
    # result = os.system(qt_command)
    # print(result)

    # subprocess.run([python_command, script])


class LaunchQTAppCommand(apper.Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        launch_qt_app()


class LaunchReceiverCommand(apper.Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        fusion_app: apper.FusionApp = self.fusion_app
        qt_event_thread: apper.Fusion360CustomThread = fusion_app.events[0]

        qt_event_thread.start_thread()


