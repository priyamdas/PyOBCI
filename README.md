Python Library for OpenBCI
==============
This repository's purpose is to allow for programmers to interface with OpenBCI technology directly, both to acquire data and to write programs that can use that data on a live setting, using Python.

If this is not what you are looking for, you can visit http://openbci.com/downloads and browse other OpenBCI software that will fit your needs.

## Dependency List
--------------

OpenBCI 8 and 32 bit board with 8 or 16 channels.
* Python 2.7 or later (https://www.python.org/download/releases/2.7/)
* Numpy 1.7 or later (http://www.numpy.org/)

Use of specific features and scripts may require additional packages.

## Setup and Installation
-------------
Refer to http://docs.openbci.com/tutorials/01-GettingStarted 

## Repository Hierarchy
--------------
### open_bci.py

This file contains the class definition that instantiates an OpenBCI Board object and various helpful commands to interact with the board, including initializing communication with it.

### test.py

A simple piece of example code that should print values. 

### Utilities

The `utilities` folder contains numerous tools with which to collect and sort data from the OpenBCI board.

* `classifier`

 A good starting point. It includes openbci_collector.py (a class that tracks data and stores it in a CSV file) and pyeeg.py (a Python module to extract EEG features)

* `pybrain_examples`

 Code that can be used in conjunction with PyBrain - the Python Machine Learning Library

* `udp`

 This folder contains scripts needed to run a UDP server that streams OpenBCI data and a sample client for the server.

## Additional Information
-------------------

To learn more about the Cognitive Technology Group, check out the Facebook page!
https://www.facebook.com/groups/CogTechBerkeley/

This readme was adapted from that of https://github.com/OpenBCI/OpenBCI_Python

