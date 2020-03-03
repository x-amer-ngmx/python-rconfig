rconfig
=======

  ``rconfig`` helps you to load configs from consul server to your environment
  variable.


Installation
------------

  Install the latest version with:

  ::

    pip install -U python-rconfig


  For command-line support, use the CLI option during installation:

  ::

    pip install -U "python-rconfig[cli]"


Usecase
-------

  First off all `rconfig` expects that you have the following key structure in
  consul

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
