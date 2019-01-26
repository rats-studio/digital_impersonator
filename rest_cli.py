import requests
import json
from communicator import Communicator

MENU_TEXT = """

Choose the following options:

[1] : Convert text one time.
[2] : Convert text in a continous stream.
[3] : Check the last saved entry.

[0] : Exit.
\n> """


def main():
    options = input(MENU_TEXT)
    c = Communicator()

    if options == "1":
        to_send = input("Type what you want to send\n> ")

        # turn input into dict to pass through request.post() as json
        # conversion between dict and json is automatic 
        to_send  = {"entry_string": to_send}
        c.send_recieve(to_send)
    elif options == "2":
        print("Type what you want to send. \nType 'q' to quit.")

        while True:
            to_send = input("\n> ")

            if to_send == "q":
                quit()

            # turn input into dict to pass through request.post() as json
            # conversion between dict and json is automatic
            to_send  = {"entry_string": to_send}
            c.send_recieve(to_send)
    elif options == "3":
        c.read_last()
    elif options == "0":
        quit()
    else:
        print("Option not recognised. Try again.")
        main()


if __name__ == "__main__":
    main()
