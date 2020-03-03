rconfig
=======

  .. image:: https://travis-ci.org/ArtemAngelchev/python-rconfig.svg?branch=master
      :target: https://travis-ci.org/ArtemAngelchev/python-rconfig

  .. image:: http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat


  ``rconfig`` helps you to bring configs from a consul server to your
  application.


Installation
------------

  Install the latest version with:

  ::

    pip install -U python-rconfig


  For command-line support, use the CLI option during installation:

  ::

    pip install -U "python-rconfig[cli]"


Usage
-----

  First off all ``rconfig`` expects that you have the following key structure
  on the consul server:

  ::

    <root-key>
        |____<common-config-key>
        |          |
        |          |___<some-env-key>
        |          |           |_____<key-value>
        |          |           |_____<key-value>
        |          |
        |          |___<another-env-key>
        |                      |_____<key-value>
        |                      |_____<key-value>
        |____<app-config-key>
                   |
                   |___<some-env-key>
                   |           |_____<key-value>
                   |           |_____<key-value>
                   |
                   |___<another-env-key>
                               |_____<key-value>
                               |_____<key-value>


  Here root key stands for the name of the project when some have multiple
  applications that grouped under some kind of common purpose (often when talk
  about microservices).
  Under common configuration key, you should store configurations that common
  to all your applications in the project, in this case, it's much easier to
  change the config in one place than go to multiple.
