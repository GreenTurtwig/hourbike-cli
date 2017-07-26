Hourbike CLI
============
**A CLI for Hourbike schemes across the UK.**

About
-----
This command line application allows you to find information about the bicycle stations closest to your current location.

Currently supported cities and towns are: Lincoln (hirebike), Liverpool (CityBike), Reading (ReadyBike), Sheffield (Sheffield ByCycle) and Southport (Southport Cycle Hire)

.. image:: http://i.imgur.com/Tvujnp4.png

Installation
------------
.. code-block::

    $ pip install hourbike-cli

Usage
-----
For help use the -h option.

.. code-block::

    $ hourbike -h

To get the nearest bike stations to a loction, type:

.. code-block::

    $ hourbike liverpool "liverpool cathedral"
