# Ask and recieve

A very simple example of how microservices can be tied together with a RESTful API in Flask.

## Automatic launch

Run *run_services.py*. The front-end will be available at localhost:5003.

## Manual launch

To run the back-end, launch *ask_me.py* and *ask_processor.py*.

To run the front-end, launch *front_end.py* to communicate with the services. You can also curl from the terminal, or simply use the *rest_cli.py* program.

```text
curl 127.0.0.1:5000/ask/ -d "This is a test."
```

TODO
* Implement HTTPS