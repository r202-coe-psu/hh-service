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

* Install `hhclient` for web module
 * Clone repository
~~~~
git clone git@138.47.200.245:HomeHero-Projects/python-hhclient.git
~~~~
 * install `hhclient` in testing environment
~~~~
$ source hh-env
(hh-env)$ cd python-hhclient
(hh-env)$ python setup.py develop
~~~~

### API module
* Create API configuration file `api-development.cfg`
~~~~
# Secret key
# Can create using urandom
# >>> import os
# >>> os.urandom(22)
# b'\xca\xe0p\xfdj\xf8\xcem?\x0f\x9d\x8e\xa6\xa0\xfd\x00/t7c\x9e\x98'
SECRET_KEY = '\xca\xe0p\xfdj\xf8\xcem?\x0f\x9d\x8e\xa6\xa0\xfd\x00/t7c\x9e\x98'

# Database
MONGODB_DB = 'homehero'
~~~~

* Run api module

~~~~
$ source hh-env
(hh-env)$ cd hh-service
(hh-env)$ HHSERVICE_API_SETTINGS=$(pwd)/api-development.cfg hhservice-api -d
~~~~

* Note
 * `HHSERVICE_API_SETTINGS` = an API setting file environent
 * `api-development.cfg` = an API setting file contains configurating variables.
 * `hhservice-api` = an API executable file


### Web module

* Create WEB configuration file `web-development.cfg`
~~~~
# same as API secret key
SECRET_KEY = '\xca\xe0p\xfdj\xf8\xcem?\x0f\x9d\x8e\xa6\xa0\xfd\x00/t7c\x9e\x98'

# HHService API endpoint
HHSERVICE_APT_HOST = 'localhost'
HHSERVICE_API_PORT = 5001
~~~~

* Initial JavaScript using jspm

~~~~
$ jspm install
~~~~

* Run web module

~~~~
$ source hh-env
(hh-env)$ cd hh-service
(hh-env)$ HHSERVICE_WEB_SETTINGS=$(pwd)/web-development.cfg hhservice-web -d
~~~~
* Note
 * `HHSERVICE_WEB_SETTINGS` = a web setting file environent
 * `web-development.cfg` = a web setting file contains configurating variables.
 * `hhservice-web` = a web server executable file


