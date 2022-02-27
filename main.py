from client import Client
from logger import Logger

if __name__ == '__main__':
    logger = Logger()

    with Client(logger) as client:
        client.start()

        while True:
            s = input().strip()

            if len(s) < 1:
                continue

            cmd = s.split(' ')

            if cmd[0] == 's' and len(cmd) > 3:
                client.send((cmd[1], int(cmd[2])), ' '.join(cmd[3:]))
            elif cmd[0] == 'q':
                break
