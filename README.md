About
=====

A simple timecard command line utility in Python. There are others that
exist on GitHub, but I wanted to write my own for fun. This version uses
a SQLite database in Dropbox, so can be used across computers.

Installing
==========

    $ python setup.py install

Using
=====

To start working on a project/task:

    $ tc start project_name

To stop working on a project/task:

    $ tc stop project_name

In future, I'll add some statistics commands, but for now the priority
is to start logging tasks.

