openhim-mediator-multitenant
============================

An OpenHIM mediator that supports multiple tenants, each potentially with
multiple upstream APIs.

For more information about the OpenHIM, see the [OpenHIM documentation][docs].

For more information on OpenHIM mediators, see the 
[OpenHIM Developer Guide][dev].


Installation
------------

To install locally, use the following commands:

    $ git clone https://github.com/dimagi/openhim-mediator-multitenant.git
    $ pip install -r requirements.txt

Copy the sample environment variable values with ...

    $ cp env/sample env/MY_ENVIRONMENT

... where "MY_ENVIRONMENT" is the name you give your local environment. A 
reasonable name might be "development". Edit the new file, and change the
values of the environment variables according to your needs. 

To understand what the variables refer to, check the 
`mediator/mediator/settings.py` file, where most of them are used. The
variables whose names start with "PROXY_" are used when the mediator is
deployed with a proxy server. For more context see the nginx configuration file
`docker/templates/mediator.conf` and Amazon Web Services task configuration
file `docker/templates/Dockerrun.aws.json`.


Deployment
----------

This mediator is intended to be deployed to an AWS Elastic Beanstalk
multi-container Docker environment, or any platform that supports Docker. It
could also be installed on AWS Lambda with Amazon API Gateway. It was developed
on an AWS EC2 instance.


### Deploying to AWS Elastic Beanstalk

You will need an Elastic Beanstalk multi-container Docker environment, an
Elastic Block Storage volume for a TLS/SSL certificate, and a database. Amazon
RDS for PostgreSQL would be a reasonable choice.

Install the AWS EB CLI, and make sure you can SSH into your environment.

Copy the sample environment variable values to, say, env/aws_eb, or whatever
you would like to call your AWS Elastic Beanstalk environment. e.g.

    $ cp env/sample env/aws_eb

Change the environment variable values accordingly.

Set the environment variables locally with ...

    $ . env/aws_eb

... and build an Elastic Beanstalk artifact:

    $ scripts/build-eb-artifact.sh

Deploy the artifact to Elastic Beanstalk:

    $ scripts/deploy-eb.sh

Alternatively, building the artifact and deploying it can be done in a single
step using:

    $ scripts/deploy-eb.sh -a



### Deploying with docker-compose

You can find the Docker image of this codebase on [Docker Hub][hub]. You can
refer to it in your `docker-compose.yaml` file with 
`dimagi/openhim-mediator-multitenant:latest`.

There is an example `docker-compose.yaml` file in the `docker/templates/`
directory useful for development. (In production the OpenHIM core and console
are probably deployed independently.) It will give you a good example of the
mediator service definition, and the environment variables you will need to
set.


  [docs]: https://openhim.readthedocs.io/en/latest/about.html
  [dev]: https://openhim.readthedocs.io/en/latest/dev-guide/mediators.html
  [hub]: https://hub.docker.com/r/dimagi/openhim-mediator-multitenant
