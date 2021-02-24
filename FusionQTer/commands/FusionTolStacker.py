# Importing sample Fusion Command
# Could import multiple Command definitions here

import asyncio
import json
import sys
import threading

import adsk.cam
import adsk.core
import adsk.fusion
import traceback
from .Demo1Command import Demo1Command
from .FusionApper.Fusion360Utilities import get_std_out_file, get_std_err_file
from .FusionApper.FusionApper import FusionApper as apper
from .QTTest import QTTest

app = None
ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None
myCustomEvent = 'MyCustomEventId'
customEvent = None
APP_NAME = 'FusionTolStacker'
my_app = apper(APP_NAME, False)


# Define parameters for 2nd command
demo_command = my_app.add_command(
    {
        'cmd_name': 'Demo Command 1',
        'cmd_description': 'Check if a design will tip',
        'cmd_id': 'demo_command',
        'cmd_resources': './resources',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'QT Test',
        'command_visible': True,
        'command_promoted': False,
    },
    Demo1Command
)
# Define parameters for 2nd command
qt_test_command = my_app.add_command(
    {
        'cmd_name': 'QT Test',
        'cmd_description': 'Check if a design will tip',
        'cmd_id': 'qt_test_command',
        'cmd_resources': './resources',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'QT Test',
        'command_visible': True,
        'command_promoted': True,
    },
    QTTest
)

# Set to True to display various useful messages when debugging your app
debug = False


# The event handler that responds to the custom event being fired.
class ThreadEventHandler(adsk.core.CustomEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # # Make sure a command isn't running before changes are made.
            # if ui.activeCommand != 'SelectCommand':
            #     ui.commandDefinitions.itemById('SelectCommand').execute()

            # Get the value from the JSON data passed through the event.
            eventArgs = json.loads(args.additionalInfo)

            # Handle the commands
            msg = eventArgs['msg']
            ui.messageBox('Message received: ' + msg)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# The class for the new thread.
class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        from multiprocessing.connection import Client
        address = ('localhost', 6000)
        with Client(address, authkey=b'secret password') as conn:
            while not self.stopped.wait(5):
                msg = conn.recv()[0]
                args = {'msg': msg}
                app.fireCustomEvent(myCustomEvent, json.dumps(args))
        # import asyncio
        # loop = asyncio.new_event_loop()
        # queue = asyncio.Queue()
        #
        # loop.run_until_complete(get_data(queue))


async def get_data(loop, output_queue):
    # code = 'import datetime; print(datetime.datetime.now())'
    asyncio.set_event_loop(loop)
    # loop.run_forever()
    print("about to run")

    cmd = '/Users/rainsbp/Dropbox/Projects/PyCharm/QT/QTTuorial/venv/bin/python '
    args = '/Users/rainsbp/Dropbox/Projects/PyCharm/QT/QTTuorial/main.py'

    shell_cmd = cmd + ' ' + args
    # Create the subprocess; redirect the standard output
    # into a pipe.
    # proc = await asyncio.create_subprocess_exec(
    proc = await asyncio.create_subprocess_shell(
        shell_cmd,
        # args,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    print("created process" + str(proc.pid))
    process_task = asyncio.create_task(process_lines(output_queue))
    while proc.returncode is None:
        line = await proc.stdout.readline()
        if not line:
            break
        await output_queue.put(line.rstrip())

    shutdown(process_task)
    return 1

async def process_lines(_queue):

    while True:
        line = await _queue.get()
        print(line)
        _queue.task_done()
        args = {'msg': str(line)}
        app.fireCustomEvent(myCustomEvent, json.dumps(args))


def shutdown(proto):
    print("Shutdown of DummyProtocol initialized ...")

    # Set shutdown event:
    proto.cancel()
    # TODO something about finishing up the queue before exiting
    # Stop loop:
    # _loop.stop()

    # Find all running tasks:
    # pending = asyncio.Task.all_tasks()
    #
    # # Run loop until tasks done:
    # _loop.run_until_complete(asyncio.gather(*pending))

    print("Shutdown complete ...")


std_err_file = get_std_err_file(APP_NAME)
std_out_file = get_std_out_file(APP_NAME)
sys.stdout = open(std_out_file, 'w')
sys.stderr = open(std_err_file, 'w')


def run(context):
    global ui
    global app
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Register the custom event and connect the handler.
        global customEvent
        customEvent = app.registerCustomEvent(myCustomEvent)
        onThreadEvent = ThreadEventHandler()
        customEvent.add(onThreadEvent)
        handlers.append(onThreadEvent)

        # loop = asyncio.new_event_loop()
        # queue = asyncio.Queue()
        # t = threading.Thread(target=get_data, args=(loop, queue), daemon=True)
        # t.start()

        # Create a new thread for the other processing.
        global stopFlag
        stopFlag = threading.Event()
        myThread = MyThread(stopFlag)
        myThread.start()



    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        print(traceback.format_exc())
        print(e)

    my_app.run_app()


def stop(context):
    my_app.stop_app()
    try:
        if handlers.count:
            customEvent.remove(handlers[0])
        stopFlag.set()
        app.unregisterCustomEvent(myCustomEvent)
        ui.messageBox('Stop addin')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
