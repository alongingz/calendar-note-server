import os
import time


def status_server(server_name):
    server_pid = os.popen("pgrep -f {}".format(server_name))
    if server_pid:
        return server_pid
    return False


def start_server(start_command):
    os.popen(start_command)


def stop_server(server_name):
    os.popen("pkill -f {}".format(server_name))


def restart_server(server_name, start_command):
    if status_server(server_name):
        stop_server(server_name)
        time.sleep(3)
        start_server(start_command)
        time.sleep(2)
        if status_server(server_name):
            print("*** restart {} success. ***".format(server_name))
        else:
            print("*** no start!!! ***")
    else:
        start_server(start_command)
        time.sleep(2)
        if status_server(server_name):
            print("*** start {} success. ***".format(server_name))
        else:
            print("*** no start!!! ***")


if __name__ == '__main__':
    server_name = "run_calendar_server"
    start_command = "nohup python3 {}.py 2>&1 &".format(server_name)
    restart_server(restart_server, start_command)
