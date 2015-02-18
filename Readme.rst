************************************
Buildout for Shopping Search project
************************************

Installation notes
==================

For environment set up zc.buildout is used (https://pypi.python.org/pypi/zc.buildout/2.3.1)

Before building it you need to set up environment version you would like to have.
Currently there is *production* and *development* configuration available, to
set config do following:

.. code-block:: bash

    $ cp buildout.cfg.example buildout.cfg
    $ vim buildout.cfg

and in buildout.cfg uncomment one of profiles extends  you would like to be
activated, for example if you would like your environment to be build in
*production* mode the part section of buildout should look like this:

.. code-block::

    [buildout]
    extends =
        profiles/production.cfg
    #    profiles/devel.cfg


To build buildout run following command:

.. code:: bash

    $ python3.4 bootstrap-buildout.py
    $ bin/buildout

And do not forget to syncdb:

.. code-block:: bash

    $ bin/django syncdb

Frontend part of application is located in ngbp folder. It requeires to have
installed Node.js on system. Frontend are based on https://github.com/ngbp/ngbp


Services set up
===============

Amazon service
--------------

Application uses Amazon Advertising API. You need to set your aws_key,
aws_secret and aws_associate_tag in configuration section. You can
register and get API keys on AWSECommerce page -
http://docs.aws.amazon.com/AWSECommerceService/latest/DG/Welcome.html
or generate keys on https://console.aws.amazon.com/iam/home#security_credential


**Important links**:

    * Item search API: http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html
    * Locale Information for the JP Marketplace: http://docs.aws.amazon.com/AWSECommerceService/latest/DG/LocaleJP.html

TODO: add more instruction, make unified set up; add other services


Yahoo! Japan Shopping API
-------------------------

What do you need to use Yahoo! Japan Shopping API:
    1. Get Yahoo! JAPAN ID (register on https://account.edit.yahoo.co.jp/registration)
    2. Register Application to get Application ID and Secret.
    3. In buildout.cfg file set appid variable to your Application ID

**Important links**:
    * Shopping API: http://developer.yahoo.co.jp/webapi/shopping/

Project structure
=================


This project has two independent parts:
    * front-end
    * back-end

Front end
---------

Front-end doesn't care about back-end at all and can be used separately,
it's single file javascript application based on AngularJS and ngpb
environment.

TODO: describe API calls here

Back end
--------

Back-end is based in Django framework and more like API to search.

TODO: describe API calls here


Site Management
===============

To start djnago server run command

.. code:: bash

    bin/django runserver


If you want to play around frontend then read ngbp instruction. In most cases
if would be enough to have buildout built in development and run following
commands:

.. code-block:: bash

    $ cd ngbp
    $ ../bin/grunt watch

After it you can edit front-end sources which is located in *ngbp/build/src*
folder.


