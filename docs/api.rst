Web API
=======



For the Semantic Map 
++++++++++++++++++++

This function calculates and returns all the data for the semantic map of a word.

Pyhton Function::

>>> api_semantics()

URL::

<ROOT>/api/semantics


Parameters
----------

* iso (string)
* term (unicode string)

The Python function takes no parameters, this is due to the fact that it is only called in Javascript.
The parameters can only be passed using an HTTP request::

<ROOT>/api/semantics?iso=<iso>&term=<term>

For example::

http://www.poio.eu/api/semantics?iso=bar&term=brezn


Return
------

* graphdata (json)

The Python function has no return. The data is returned as Json in the HTTP response, somewhat like an html file.
The returned data is a list (array) of 50 lists wich have 3 elements: the word, the x coordinates and the y coordinates.

`Example here. 
<http://www.poio.eu/api/semantics?iso=bar&term=brezn>`_



For the Prediction
++++++++++++++++++

This funtion predicts and returns similar words to the one supplied.

Python Funtion::

>>> api_prediction()

URL::

<ROOT>/api/prediction


Parameters
----------

* iso (string)
* text (unicode string)

The Python function takes no parameters, this is due to the fact that it is only called in Javascript.
The parameters can only be passed using an HTTP request::

<ROOT>/api/prediction?iso=<iso>&text=<text>

For example::

http://www.poio.eu/api/prediction?iso=bar&term=brez


Return
------

* predictions (json)

The Python function has no return. The data is returned as Json in the HTTP response, somewhat like an html file.
The returned data is a list (array) of 6 predicted words.

`Example here. 
<http://www.poio.eu/api/prediction?iso=bar&text=brez>`_



For the Supported Languages
+++++++++++++++++++++++++++

This function checks for all the supported languages and returns them in ISO-639-3.

Pyhton Function::

>>> api_languages()

URL::

<ROOT>/api/languages


Parameters
----------

This function takes no parameters, neither from Python nor from an HTTP request.


Return
------

* languages_list (json)

The Python function has no return. The data is returned as Json in the HTTP response, somewhat like an html file.
The returned data is a list (array) of all the supported languages.

`Example here. 
<http://www.poio.eu/api/languages>`_



For the corpus files
++++++++++++++++++++

This function looks for all the avaible corpus files for a given language and returns a list with the paths of those files.

Pyhton Function::

>>> api_corpus()

URL::

<ROOT>/api/corpus


Parameters
----------

* iso (string)

The Python function takes no parameters, this is due to the fact that it is only called in Javascript.
The parameters can only be passed using an HTTP request::

<ROOT>/api/corpus?iso=<iso>

For example::

http://www.poio.eu/api/corpus?iso=bar


Return
------

* files (json)

The Python function has no return. The data is returned as Json in the HTTP response, somewhat like an html file.
The returned data is a list (array) of all the paths for all the avaible corpus files for the given language.

`Example here. 
<http://www.poio.eu/api/corpus?iso=bar>`_