import socket
import time

TIME_TO_BOOT_SECONDS = 5
TIME_TO_RECHECK_SECONDS = 10
MAX_COUNTER = 3

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
    print("Resetting router")

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


