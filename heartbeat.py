import socket
import time
from telnetlib import Telnet

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
    print(f"Waiting to boot {TIME_TO_BOOT_SECONDS} seconds")
    counter = 0
    time.sleep(TIME_TO_BOOT_SECONDS)

def isConnected():
    print("Checking connected")
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
    print(f"Waiting to return {TIME_TO_RECHECK_SECONDS} seconds")
    time.sleep(TIME_TO_RECHECK_SECONDS)

def reset_router():
    print("Connecting through telnet to router")
    tn = Telnet(host)
    
    tn.read_until(b"login: ")
    tn.write(user.encode("ascii") + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    print("Rebooting now")
    tn.write(b"reboot\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))

def main():
    global counter
    while True:
        wait_for_boot()
        while counter < (MAX_COUNTER - 1):
            connected = isConnected()

            print(f"Lost connection? {not connected}")

            if not connected:
                counter = counter + 1
            else:
                counter = 0
            print(f"Counter: {counter}")
            wait_to_retry()

        reset_router()


if __name__ == "__main__":
    main()


