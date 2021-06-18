import sys

from pika import exceptions

from middle_vec_angle import MiddleVecAngle

if __name__ == "__main__":
    a = MiddleVecAngle("middle vector angle")
    try:
        a.listen()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            pass
    except exceptions.ConnectionClosedByBroker:
        print('Connection closed')
        try:
            sys.exit(0)
        except SystemExit:
            pass