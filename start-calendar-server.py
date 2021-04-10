import os
import time


def status_server(server_name):
    server_pid = os.popen("pgrep -f %" % server_name)
    if server_pid:
        return server_pid
    return False


def start_server(start_command):
    os.popen(start_command)


def stop_server(server_name):
    os.popen("pkill -f %" % server_name)


def restart_server(server_name, start_command):
    if status_server(server_name):
        stop_server(server_name)
        time.sleep(3)
        start_server(start_command)
        time.sleep(2)
        if status_server(server_name):
            print("*** restart {} success. ***".format(server_name))
    else:
        start_server(start_command)
        time.sleep(2)
        if status_server(server_name):
            print("*** start {} success. ***".format(server_name))


if __name__ == '__main__':
    server_name = "calendar_server"
    start_command = "nohup python3 calendar_server.py 2>&1 &"
    restart_server(restart_server, start_command)
