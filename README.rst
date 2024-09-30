rconfig
=======

  .. image:: https://travis-ci.org/ArtemAngelchev/python-rconfig.svg?branch=master
      :target: https://travis-ci.org/ArtemAngelchev/python-rconfig

  .. image:: https://coveralls.io/repos/github/ArtemAngelchev/python-rconfig/badge.svg?branch=master
      :target: https://coveralls.io/github/ArtemAngelchev/python-rconfig?branch=master

  .. image:: https://badge.fury.io/py/python-rconfig.svg
      :target: https://badge.fury.io/py/python-rconfig

  .. image:: http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat


  ``rconfig`` helps bring configuration, stored remotely on a ``Consul``
  server, to  your application.


Installation
------------

  Install the latest version with:

  ::

    pip3 install -U python-rconfig


  For command-line support, use the CLI option during installation:

  ::

    pip3 install -U "python-rconfig[cli]"


  For command-line and yaml support:

  ::

    pip3 install -U "python-rconfig[cli,yaml]"


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


Command-line Interface
----------------------

  CLI offers you an ability to load config from ``Consul`` (within a few ways)
  without a need of changing application code.

  ::

    Usage: rconfig [OPTIONS] COMMAND [ARGS]...

    Options:
      -h, --host TEXT     Host of a consul server  [required]
      -a, --access TEXT   Access key for a consul server  [required]
      -p, --port INTEGER  Port of consul server  [default: 8500]
      -k, --key TEXT      Consul key  [required]
      --help              Show this message and exit.

    Commands:
      export  Print out bash command export for all found config
      list    Show all config for given keys


  Let's look at few examples.

  ::

    <your-awesome-app>
        |____<prod>
               |___<LOG_LEVEL -> "WARNING">
               |___<LOG_FILE_HANDLER -> 1>


  To load ``prod`` config of ``you-awesome-app``, issue:

  ::

    $ rconfig -h localhost -a access-key -k 'your-awesome-app/prod' list

    {'LOG_LEVEL': 'WARNING',
     'LOG_FILE_HANDLER': 1}


  To export config to different formats, use:

  Bash:
  ::

    $ rconfig -h localhost -a access-key -k 'your-awesome-app/prod' export -f bash

    export LOG_LEVEL='WARNING'
    export LOG_FILE_HANDLER='1'

  ::

    $ rconfig -h localhost -a access-key -k 'your-awesome-app/prod' export -f bash:inline

    export LOG_LEVEL='WARNING' LOG_FILE_HANDLER='1'

  Yaml:
  ::

    $ rconfig -h localhost -a access-key -k 'your-awesome-app/prod' export -f yaml

    LOG_LEVEL: WARNING
    LOG_FILE_HANDLER: 1

  Json:
  ::

    $ rconfig -h localhost -a access-key -k 'your-awesome-app/prod' export -f json

    {"LOG_LEVEL": "WARNING", "LOG_FILE_HANDLER": 1}

  ::

    $ rconfig -h localhost -a access-key -k 'your-awesome-app/prod' export -f json:pretty

    {
        "LOG_LEVEL": "WARNING",
        "LOG_FILE_HANDLER": 1
    }

