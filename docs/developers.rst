Development
===========


Prepare the Server for launch
-----------------------------

This will install all requirements and prepare the Server (`Flask webapp`) for launch.


Initialize your enviroment
..........................

Start by bootstraping the buildout environment::

$ python bootstrap.py

Next you have to install all dependencies using the buildout script::

$ sudo bin/buildout


Get language data from server
.............................

You have to download all the language data from our Amazon server (this may take a while)::

$ python get_corpus_data.py


Run the tests
.............

Before starting the server you should run our tests to ensure that everything is working properly::

$ bin/test


Start the server in development mode
.....................................

Finally you can start the server::

$ bin/flask-ctl debug fg



How to get Poio Site working on Pycharm
-----------------------------------------

* Start by creating a new project with the following settings:

  * Project name: ``Poio Site``
  * Location: ``<PATH_TO>/poio-site/src/main/``
  * Project type: ``Flask Project``
  * Interpreter: ``Python 2.7``

* After you press ``Ok`` PyCharm will prompt if you want to create a project from existing sources, press Yes.

* In order to run the server from PyCharm you need to add a new confguration for the server, to do this: 
	
  * On the menu bar go to ``Run`` and open ``Edit Configurations...``;
  * Press the ``+`` sign and from the dropdown menu choose ``Python``.

* Fill in the new confifuration with the following settings and press ``Ok``:

  * Name: ``Poio Site Server``
  * Script: ``bin/flask-ctl``
  * Script parameters: ``debug fg``
  * Working directory: ``<PATH_TO>/poio-site/``

Now every time you want to start the server make sure that the selected configuration on the menu bar is ``Poio Site Server`` and just press ``Run`` (play button).