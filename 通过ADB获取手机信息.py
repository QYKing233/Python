import os
import subprocess
import telebot

# 定义telegram机器人
bot = telebot.TeleBot("YOUR_TOKEN")

# 定义推送消息函数
def send_messages(message):
    bot.send_message(ChatID, message)

# adb连接以下设备
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

        # 获取品牌信息
        brand = run_adb_command("adb shell getprop ro.product.brand")

        # 获取型号信息
        model = run_adb_command("adb shell getprop ro.product.model")

        # 获取安卓版本
        version = run_adb_command("adb shell getprop ro.build.version.release")

        # 获取电量信息
        battery_info = run_adb_command("adb shell dumpsys battery | grep 'level' | awk -F ':' '{print $2}'").replace(" ","")  # 仅获取电量部分信息

        # 将信息存储在字典中
        data = ''
        datas = {
            "品牌👉": brand,
            "型号👉": model,
            "版本👉":"Android " + version,
            "电量👉": battery_info
        }

        # 打印字典中的信息
        for key, value in datas.items():
            data = data + (f"{key}{value}") + '\n'
        # 推送到Telegram
        send_messages(data)
    except:
      pass
      os.system("adb disconnect")
