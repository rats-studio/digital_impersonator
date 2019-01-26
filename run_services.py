from sys import executable
from subprocess import Popen

Popen([executable, "front_end_worker.py"])
Popen([executable, "back_end_worker.py"])
Popen([executable, "front_end.py"])

input("Press ENTER to exit.")