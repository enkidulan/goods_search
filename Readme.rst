************************************
Buildout for Shopping Search project
************************************

Installation notes
==================

For environment set up zc.buildout is used (https://pypi.python.org/pypi/zc.buildout/2.3.1)
To build buildout run following command:

.. code:: bash

    $ python3.4 bootstrap-buildout.py
    $ bin/buildout


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

