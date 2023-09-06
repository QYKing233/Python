import subprocess
import time
import telebot

# 定义telebot
bot = telebot.TeleBot("TOKEN")

# 定义推送消息函数
def send_messages(message):
    bot.send_message(ChatID, message)


# 定义推送图片函数
def send_photo():
    bot.send_photo(groupid, open('screen.png', 'rb'))

# 定义run函数
def run(command):
    result = subprocess.run(command, shell=True)
    return result


devices = ['192.168.233.214:5555']
for device in devices:
    # Disconnect from any connected devices
    print("断开所有安卓设备链接")
    run("adb disconnect")

    try:
        # Connect to the specified device
        print("链接" + device)
        run("adb connect " + device)

        # 唤醒屏幕
        print("唤醒屏幕")
        run("adb shell input keyevent 224")

        # 等待3s
        print("3s后打开钉钉")
        for wait in range(0, 3):
            print(3 - wait)
            time.sleep(1)

        # 打开钉钉
        print("打开钉钉")
        run("adb shell am start -n com.alibaba.android.rimet/com.alibaba.android.rimet.biz.LaunchHomeActivity")

        # 等待30s
        print("停留30s")
        for wait in range(0, 30):
            print(30 - wait)
            time.sleep(1)
        print("跳转到打卡页面")
        run('''adb shell am start -a android.intent.action.VIEW -d "dingtalk://dingtalkclient/page/link?url=https://attend.dingtalk.com/attend/index.html?corpId=ding6c7a37f98aae1b0c35c2f4657eb6378f"
''')

        # 等待30s
        print("停留30s")
        for wait in range(0, 30):
            print(30 - wait)
            time.sleep(1)

        # 截屏
        print("截图")
        run("adb shell input keyevent 224")
        time.sleep(3)
        run("adb shell screencap -p /sdcard/screen.png")
        time.sleep(3)
        check_screen = run("adb shell ls /sdcard/screen.png")
        while check_screen.returncode != 0:
            print("截图失败丨重新截图")
            run("adb shell input keyevent 224")
            time.sleep(3)
            run("adb shell screencap -p /sdcard/screen.png")
            time.sleep(3)
            check_screen = run("adb shell ls /sdcard/screen.png")
        print("截图成功")

        # 等待3s
        print("停留3s")
        for wait in range(0, 3):
            print(3 - wait)
            time.sleep(1)

        # 拉取screen.png到当前目录
        print("拉取截图到服务器")
        pull = run("adb pull /sdcard/screen.png ./")
        while pull.returncode != 0:
            print("拉取失败丨重新拉取")
            run("adb disconnect")
            run("adb connect " + device)
            pull = run("adb pull /sdcard/screen.png ./")
        print("拉取成功")

        print("从服务器推送截图到TG机器人")
        send_photo()

        print("3s后关闭钉钉返回主界面并熄灭屏幕")
        for wait in range(0, 3):
            print(3 - wait)
            time.sleep(1)

        # 关闭钉钉
        run("adb shell rm -rf /sdcard/screen*.png")
        run("rm -rf ./screen.png")
        run("adb shell am force-stop com.alibaba.android.rimet")
        time.sleep(2)
        run("adb shell input keyevent 3")
        time.sleep(2)
        run("adb shell input keyevent 223")
    except:
        pass
        print("断开所有安卓设备链接")
        run("adb disconnect")
