# Dish

Dish is a simple webserver that listens on all interfaces on several common web
ports and serves a static web page. Dish checks each incoming request's Host
header to see if it is something other than current machine's own name, i.e.
is somebody pointing their own name at our machine? Dish reports such events
by posting a notification to an AWS SNS queue.

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

You can view Dish in your web browser at http://localhost:5000, but it's more
helpful to send requests with curl:

    $ curl -H 'host: foobar' --data foo=bar 'http://127.0.0.1:5000/'
    REPORTED Connection from 127.0.0.1
    POST http://foobar/
    Host: foobar
    User-Agent: curl/7.54.0
    Accept: */*
    Content-Length: 7
    Content-Type: application/x-www-form-urlencoded

    ImmutableMultiDict([('foo', 'bar')])⏎

The server will report back the client's IP address, HTTP method, request URI,
headers, and form data. If the host header does not match one of the expected
hosts, then the request is "reported", i.e. a copy of the information is posted
to an AWS SNS queue.

To run in production mode, use the supplied Apache configuration along with
`mod_wsgi`.
