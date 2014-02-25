SQS Splitter
============

You know those times in your life when you think to yourself: "I wish I could
take messages from a SQS queue and automatically forward them to several
other SQS queues!" Yeah, I've been there too friend. Well worry no more.

With **SQS Splitter** and a tiny bit of configuration you can have your very own
SQS forwarding service running in a matter of minutes.

Quick Start 
-----------
**(running yourself, without heroku)**

First and foremost you're going to need a couple of environment variables set
to allow us to authenticate with AWS. Make sure you have the following
environment variables set:

**Environment Variables**

    AWS_ACCESS_KEY_ID=<Your AWS Access Key>
    AWS_SECRET_ACCESS_KEY=<Your AWS Secret Key>

Next, clone the `sqs-splitter` repository

    $ git clone https://github.com/apiguy/sqs-splitter.git
    
After that install the dependencies in `requirements.txt` by doing:

    $ pip install -r requirements.txt

Almost there, just need to configure by editing config.py:

    VERBOSE = True
    REGION = 'us-east-1'
    INCOMING_QUEUE = '<the name of the SQS queue you want to forward>'
    OUTGOING_QUEUES = [
        '<the name of a queue you want to forward to>',
        '<the name of another queue you want to forward to>'
    ]

Finally, run it with:

    $ python sqs_splitter.py


Installing on Heroku
--------------------

Sure, it's nice being able to run this locally on your own machine, but what
about getting it running on a service somewhere? Since I'm going to be running
this on Heroku, I've included a `Procfile` for your convinience.

