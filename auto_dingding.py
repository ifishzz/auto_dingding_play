from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import time
import datetime
import random

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.multipart import MIMEMultipart


# Touch the screen on a series of coordinates.
# Slide to unlock
light_position = "300 1000 300 500"
# Click "work"
work_position = "540 2140"
# Click "time check"
check_position = "550 1420"
# Click on "off duty"
play_position = "538 1115"


# 打开钉钉以及关闭钉钉封装为一个妆饰器函数
def with_open_close_dingding(func):
    def wrapper(self, *args, **kwargs):
        print("打开钉钉")
        operation_list = [self.adbpower, self.adbclear, self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=True, stdout=subprocess.PIPE)
            process.wait()
        # 确保完全启动，并且加载上相应按键（根据手机响应速度可以调整这里）
        time.sleep(10)
        operation_list1 = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list1:
            process = subprocess.Popen(operation, shell=True, stdout=subprocess.PIPE)
            process.wait()
            # 等待点击屏幕后响应
            time.sleep(2)
        # 等待工作页面加载
        time.sleep(30)
        # 执行打卡操作
        func(self, *args, **kwargs)

        print("关闭钉钉")
        operation_list2 = [self.adbback_index, self.adbkill_dingding, self.adbpower]
        for operation in operation_list2:
            process = subprocess.Popen(operation, shell=True, stdout=subprocess.PIPE)
            process.wait()
        print("kill dingding success")

    return wrapper


class dingDing:
    def __init__(self):
        # 点亮屏幕
        self.adbpower = 'adb shell input keyevent 224'
        # 滑屏解锁
        self.adbclear = f'adb shell input swipe {light_position}'
        # 启动钉钉应用
        self.adbopen_dingding = 'adb shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1'
        # 关闭钉钉
        self.adbkill_dingding = 'adb shell am force-stop com.alibaba.android.rimet'
        # 返回桌面
        self.adbback_index = 'adb shell input keyevent 3'
        # 点击工作
        self.adbselect_work = f'adb shell input tap {work_position}'
        # 点击考勤打卡
        self.adbselect_playcard = f'adb shell input tap {check_position}'
        # 点击下班打卡
        self.adbclick_playcard = f'adb shell input tap {play_position}'

    # 上班(极速打卡)
    @with_open_close_dingding
    # 打开打卡界面
    def goto_work(self):
        print("打开打卡界面")
        operation_list = [self.adbselect_work, self.adbselect_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=True, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(2)
        time.sleep(30)
        print("open playcard success")

    # 下班
    @with_open_close_dingding
    def off_work(self):
        operation_list = [self.adbclick_playcard]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=True, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(3)

        print("afterwork playcard success")


def job1():
    print("开始打卡")
    dingDing().goto_work()


def job2():
    print("开始打卡")
    dingDing().off_work()


# BlockingScheduler
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job1, 'cron', day_of_week='1-5', hour=8, minute=random.randint(31, 35))
    scheduler.add_job(job2, 'cron', day_of_week='1-5', hour=21, minute=random.randint(1, 10))
    scheduler.start()
