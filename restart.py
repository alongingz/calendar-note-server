import os
import time


def get_pid(itme):
    """
    通过项目名查询 pid
    :param itme: 项目名
    :return: pid
    """
    pids = os.popen("pgrep -f {}".format(itme))
    pids = pids.read()
    print(item, "的进程pid：", pids, type(pids))
    return pids


def kill_item(item):
    """
    通过项目名kill进程
    :param item: 项目名
    :return: 结果
    """
    result = os.popen("pkill -f {}".format(item))
    print("killed --------", result.read())
    return result.read()


def start_item(item, start_commond):
    """
    通过项目名和启动命令 启动项目
    :param item: 项目名
    :param start_commond: 启动命令
    :return:
    """
    result = os.popen(start_commond)
    print("starting-------{}".format(str(result.read())))
    time.sleep(10)
    if get_pid(item):
        print("{} started".format(item))


def start(item, start_command):
    print("当前项目启动状态：{}".format(get_pid(item)))
    if get_pid(item):  # 启动时重启
        print("当前项目已启动, 准备kill------------")
        kill_item(item)
        print("kill 成功--------------")
        time.sleep(10)
        start_item(item, start_command)
        print("重启成功-----------------")
    else:  # 未启动时启动
        start_item(item, start_command)


if __name__ == '__main__':
    item = "run_calendar_server"  # 项目名
    start_command = "nohup python -u run_calendar_server.py >qa_tools_calendar.log 2>&1 &"  # 后台启动命令
    start(item, start_command)

