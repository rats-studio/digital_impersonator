# Digital impersonator

Digital impersonator is a project about using nltk and a RESTful API in Flask to impersonate someone based on a corpus.

## Automatic launch

Run *run_services.py*. The front-end will be available at localhost:5003.

## Manual launch

To run the back-end, launch *back_end_processor.py*.

To run the front-end, launch *front_end.py* and *front_end_worker.py* to communicate with the services. Instead of the front end, you can also curl from the terminal, or simply use the *rest_cli.py* program. However, the *front_end_worker.py* still have to be running.

```text
curl 127.0.0.1:5000/ask/ -d "This is a test."
```

**TODO:**
* Implement HTTPS

**More TODO's:**
* route all requests through communicator.py, or remove communicator all together
* front-end/back-end-files into python packages
* think about config.py-file for settings (handy for future security-stuff as well)
* docstrings docstrings docstrings
