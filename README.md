# IP Squatting

Code for experiments with IP squatting.


## Dish

Dish is a simple webserver that listens on all interfaces on several common web
ports and serves a static web page. Dish checks each incoming request's Host
header to see if it is something other than current machine's own name, i.e.
is somebody pointing their own name at our machine? 

Dish logs events to AWS Document DB.

To run Dish in development mode:

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

    $ curl -H 'host: foobar' http://localhost:5000
    Host: foobar⏎

It simply displays whatever is in your host header.

To deploy in production mode, I am building this server into an AMI:
