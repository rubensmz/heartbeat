import socket
import time
from telnetlib import Telnet
import logging
from logging.handlers import RotatingFileHandler

# Configure logger
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
log_file = "heartbeat.log"
# Maximum of 5 MB
rotating_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
rotating_handler.setFormatter(log_formatter)
rotating_handler.setLevel(logging.INFO)
log = logging.getLogger('root')
log.setLevel(logging.INFO)
log.addHandler(rotating_handler)

TIME_TO_BOOT_SECONDS = 180
TIME_TO_RECHECK_SECONDS = 30
MAX_COUNT_FAIL = 3
MAX_COUNT_OK   = 20

host = "192.168.1.1"
user = "admin"
password = "admin"

ADDRESS = "1.1.1.1"
PORT    = 53
TIMEOUT = 10

count_lost = 0
count_ok   = 0

def wait_for_boot():
    global count_lost
    log.info(f"Waiting to boot {TIME_TO_BOOT_SECONDS} seconds")
    count_lost = 0
    time.sleep(TIME_TO_BOOT_SECONDS)

def isConnected():
    log.debug("Checking connected")
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
    log.debug(f"Waiting to retry in {TIME_TO_RECHECK_SECONDS} seconds")
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
    global count_lost
    while True:
        wait_for_boot()
        count_ok   = 0
        count_lost = 0
        while count_lost < (MAX_COUNT_FAIL - 1):
            connected = isConnected()

            if not connected:
                count_lost = count_lost + 1
                count_ok   = 0
                log.info(f"Connect lost during last {count_lost} tries")
            else:
                count_lost = 0
                count_ok = count_ok + 1
                if count_ok > (MAX_COUNT_OK + 1):
                    log.info(f"Connection OK during last {count_ok} tries")
                    count_ok = 0

            wait_to_retry()

        reset_router()


if __name__ == "__main__":
    main()
