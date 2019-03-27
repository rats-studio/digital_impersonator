from sys import executable
from subprocess import Popen

Popen([executable, "run-client.py"])
Popen([executable, "run-server.py"])

input("Press ENTER to exit.")
