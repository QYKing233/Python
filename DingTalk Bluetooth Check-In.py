import os
import time
import telebot
import subprocess


# 定义telebot
bot = telebot.TeleBot("YOUR_TOKEN")


# 定义推送消息函数
def send_messages(message):
    bot.send_message(ChatID, message)


# 定义推送图片函数
def send_photo():
    bot.send_photo(ChatID, open('screen.png', 'rb'))


devices = ['192.168.233.211:5555']
for device in devices:
    # Disconnect from any connected devices
    os.system("adb disconnect")

    try:
        # Connect to the specified device
        os.system("adb connect " + device)


        # 执行adb命令获取设备信息
        def run_adb_command(command):
            result = subprocess.check_output(command, shell=True, encoding="utf-8")
            return result
        
        # 跳转到签到页面
        bump = run_adb_command('''adb shell am start -a android.intent.action.VIEW -d "dingtalk://dingtalkclient/page/link?url=https://attend.dingtalk.com/attend/index.html?corpId=公司ID"''')

        # 等待15s
        time.sleep(30)

        # 截屏
        screen = run_adb_command("adb shell screencap /sdcard/screen.png")

        # 拉取screen.png到当前目录
        pull = run_adb_command("adb pull /sdcard/screen.png ./")

        send_photo()
    except:
        pass
        os.system("adb disconnect")
