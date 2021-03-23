"""
FusionQTer.py
=============
Fusion 360 Add-in for interacting with a standalone QT App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2021 by Patrick Rainsberry.
:license: MIT, see LICENSE for more details.
"""

import adsk.core
import traceback

try:
    from . import config
    from .apper import apper

    from .commands.LaunchQTAppCommand import RestartReceiverCommand, LaunchReceiverCommand
    from .commands.SendToQTAppCommand import SendToQTAppCommand
    from .commands.QTEventThread import QTEventThread

    # Create our addin definition object
    my_addin = apper.FusionApp(config.app_name, config.company_name, False)
    my_addin.root_path = config.app_path

    #  You can set the listener to not start automatically in the config file
    if not config.auto_start_thread:
        my_addin.add_command(
            'Start Receiver Thread',
            LaunchReceiverCommand,
            {
                'cmd_description': 'If Auto Start is False, use this command to initially start the thread',
                'cmd_id': 'LaunchReceiverCommand',
                'workspace': 'FusionSolidEnvironment',
                'toolbar_panel_id': 'Commands',
                'cmd_resources': 'command_icons',
                'command_visible': True,
                'command_promoted': True,
            }
        )

    my_addin.add_command(
        'Restart Receiver Thread',
        RestartReceiverCommand,
        {
            'cmd_description': 'Restarts Receiver (If you had to relaunch QT App)',
            'cmd_id': 'RestartReceiverCommand',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Commands',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    my_addin.add_command(
        'Send Mass to QT App',
        SendToQTAppCommand,
        {
            'cmd_description': 'Send Mass Props to QT App',
            'cmd_id': 'Sen  dToQTApp',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Commands',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    # The following sets up the communication to the other app and creates:
    # A new thread that starts a Client listening for events on the designated port (6000)
    # A Custom Event that responds to the listener in the thread
    my_addin.add_custom_event(config.event_id, QTEventThread, config.auto_start_thread)


#  *******************Ignore below this line**************************
except:
    app = adsk.core.Application.get()
    ui = app.userInterface
    if ui:
        ui.messageBox('Initialization Failed: {}'.format(traceback.format_exc()))

# Set to True to display various useful messages when debugging your app
debug = False


def run(context):
    my_addin.run_app()


def stop(context):
    my_addin.stop_app()
