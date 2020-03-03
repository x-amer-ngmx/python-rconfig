rconfig
=======

  ``rconfig`` help to load configs from consul to environment variable.


Installation
------------

  ::

    pip install python-rconfig


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
