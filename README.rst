FusionQTer
==========


Demo app showing communication between a standalone QT Application and a Fusion 360 Add-in.

This repo contains essentially two independant applications.

**/QTApp**

This is a "standalone" python app that uses PySide (QT) to create a simple GUI.

**/FusionQTer**

This is actually the directory of the Fusion 360 add-in

In Fusion 360 open the add-ins dialog

Press the green plus sign

Navigate to this directory to add this as a recognized add-in within Fusion 360

Usage
-----

**Step 1**

Run the python file ``QTApp/main.py`` in a virtual environment.

*See below on how to create the virtual environment.*

Assuming you are in a terminal in the ``QTApp`` Directory:

.. code-block:: bash

    python3 ./main.py

You can also use your IDE (VS Code, PyCharm, etc.) to create a run configuration for this.


**Step 2**
Start the addin from within Fusion 360.

**Note:**

It is important to do it in this order!

If you close the QT APP or make changes and restart it you need to restart
the connection thread in Fusion 360.
You should see a command that will do this from the Fusion 360 GUI.

Installation
------------

You need to create a virtual environment in the QTApp Directory to run the standalone app.

Open a terminal and navigate to the root directory of this repo.

Then execute the following commands:

.. code-block:: bash

    cd QTApp
    python3 -m venv venv/
    pip3 install -r requirements.txt
    source venv/bin/activate


Requirements
^^^^^^^^^^^^

 - PySide6

 - shiboken6

License
-------

Samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.

Authors
-------

`FusionQTer` was written by `Patrick Rainsberry <patrick.rainsberry@autodesk.com>`_.
