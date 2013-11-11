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

