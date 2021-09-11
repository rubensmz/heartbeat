import socket
import time
from telnetlib import Telnet
import logging
from logging.handlers import RotatingFileHandler

# Configure logger
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
log_file = "heartbeat.log"
rotating_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
rotating_handler.setFormatter(log_formatter)
rotating_handler.setLevel(logging.INFO)
log = logging.getLogger('root')
log.setLevel(logging.INFO)
log.addHandler(rotating_handler)

TIME_TO_BOOT_SECONDS = 120
TIME_TO_RECHECK_SECONDS = 30
MAX_COUNTER = 3

host = "192.168.1.1"
user = "admin"
password = "admin"

ADDRESS = "1.1.1.1"
PORT    = 53
TIMEOUT = 10

counter = 0

def wait_for_boot():
    global counter
    log.info(f"Waiting to boot {TIME_TO_BOOT_SECONDS} seconds")
    counter = 0
    time.sleep(TIME_TO_BOOT_SECONDS)

def isConnected():
    log.info("Checking connected")
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection((ADDRESS, PORT), TIMEOUT)
        if sock is not None:
            sock.close
        return True
    except OSError:
        pass
    return False

def wait_to_retry():
    log.info(f"Waiting to retry in {TIME_TO_RECHECK_SECONDS} seconds")
    time.sleep(TIME_TO_RECHECK_SECONDS)

def reset_router():
    log.info("Connecting through telnet to router")
    tn = Telnet(host)

    tn.read_until(b"login: ")
    tn.write(user.encode("ascii") + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    log.info("Rebooting now")
    tn.write(b"reboot\n")
    tn.write(b"exit\n")
    log.info(tn.read_all().decode('ascii'))

def main():
    global counter
    while True:
        wait_for_boot()
        while counter < (MAX_COUNTER - 1):
            connected = isConnected()

            log.info(f"Lost connection? {not connected}")

            if not connected:
                counter = counter + 1
            else:
                counter = 0
            log.info(f"Counter: {counter}")
            wait_to_retry()

        # reset_router()


if __name__ == "__main__":
    main()


