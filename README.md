# IP Squatting

Code for experiments with IP squatting.


## Dish

Dish is a simple webserver that listens on all interfaces on several common web
ports and serves a static web page. Dish checks each incoming request's Host
header to see if it is something other than current machine's own name, i.e.
is somebody pointing their own name at our machine?

Dish logs events to AWS Document DB.

Before running Dish, you first need to configure AWS.

1. Create an SNS topic.
2. Create a role that has permission to post to this topic.
3. Set up your environment to use that role: [
   instructions](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#assume-role-provider)

To run Dish in development mode:

    $ cp conf.ini.template conf.ini
    $ ## edit the conf.ini ##
    $ export FLASK_APP=dish.py
    $ export FLASK_ENV=development
    $ flask run
     * Serving Flask app "dish.py" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 818-313-372

To run in production mode, skip the `FLASK_ENV` variable above.

You can view Dish in your web browser at http://localhost:5000, but it's more
helpful to send requests with curl:

    $ curl -H 'host: foobar' http://localhost:5000
    Host: foobar⏎

It simply displays whatever is in your host header.
