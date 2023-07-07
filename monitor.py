import os
import threading
import time

import psutil


def start_monitor():
    # 创建线程对象
    my_thread = threading.Thread(target=monitoring)
    # 启动线程
    my_thread.start()
    # 主线程继续执行其他任务
    print("Hello from the main thread!")


def monitoring():
    while True:
        pid = os.getpid()
        # Get CPU and memory usage
        cpu_percent = psutil.cpu_percent()
        mem_stats = psutil.virtual_memory()

        # Get disk usage statistics for the current directory
        disk_stats = psutil.disk_usage('/Volumes')
        disk_percent = disk_stats.percent
        # Print the obtained values
        print(f"PID: {pid}, CPU Usage: {cpu_percent}%, Memory Usage: {mem_stats.percent}%, Disk Usage: {disk_percent}%")

        # Wait for some time before checking again
        time.sleep(3)
