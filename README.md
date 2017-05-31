# HHService

HHService is a part of Home Hero projects. HHService provides core functions for other Home Hero projects to access necessary information.

# Development

## HHService Repository

 * Clone repository

~~~~
$ git clone git@138.47.200.245:HomeHero-Projects/hh-service.git
~~~~

* Create Python virtual environment

~~~~
$ pyvenv hh-env
$ source hh-env
(hh-env)$ cd hh-service
(hh-env)$ python setup.py develop
~~~~

### Web module

* Initial JavaScript using jspm

~~~~
$ jspm install
~~~~

* Run web module

~~~~
$ source hh-env
(hh-env)$ cd hh-service
(hh-env)$ python run_web.py -d
~~~~
