"""
阿里云盘签到

"""


import requests
from loguru import logger
import telebot
import math

# refresh_token
refresh_tokens = ['填写APP抓包的refresh_tokens']

# telegram_token
CHATID = ''
TOKEN = ''

# 定义telebot
bot = telebot.TeleBot(TOKEN)


# 推送消息
def send_messages(message):
    bot.send_message(CHATID, message)

# 创建日志记录器
logger.add('日志.log', format='{message}', mode='w+')


# 使用refresh_token更新access_token
def update_token(token):
    url = 'https://auth.aliyundrive.com/v2/account/token'
    json = {
        'grant_type': 'refresh_token',
        'refresh_token': token
    }
    try:
        with requests.post(url=url, json=json) as response:
            result = response.json()['access_token']
            logger.success('用户昵称：' + response.json()['nick_name'])
            logger.success('用户账号：' + response.json()['user_name'])
            return result
    except:
        logger.error('获取access_token失败')


def daily_check(token):
    url = 'https://member.aliyundrive.com/v2/activity/sign_in_list'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    try:
        with requests.post(url=url, headers=headers, json={"_rx-s": "mobile"}) as response:
            result = response.json()
            logger.success('签到天数：第' + str(result['result']['signInCount']) + '天')
            return result['result']['signInCount']
    except:
        logger.error('签到失败')



def reward(token, signInDay):
    url = 'https://member.aliyundrive.com/v1/activity/sign_in_reward'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    try:
        with requests.post(url=url, headers=headers, json={"_rx-s": "mobile", "signInDay": signInDay}) as response:
            result = response.json()
            logger.success('签到结果：' + result['result']['notice'])
    except:
        logger.error('领取奖励失败')




def capacty_info(token):
    url = 'https://api.aliyundrive.com/adrive/v1/user/getUserCapacityInfo'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    try:
        with requests.post(url=url, headers=headers) as response:
            result = response.json()
            # print(result)
            logger.success('云盘容量：' + str('{:.2f}'.format(float(result['drive_capacity_details']['drive_total_size'] / (1024 * 1024 * 1024 * 1024)))) + 'TB')
            logger.success('已用容量：' + str('{:.2f}'.format(float(result['drive_capacity_details']['drive_used_size'] / (1024 * 1024 * 1024 * 1024)))) + 'TB')


    except:
        logger.error('查询容量失败')




if __name__ == '__main__':
    for refresh_token in refresh_tokens:
        access_token = update_token(refresh_token)
        try:
            if access_token != None:
                signInCount = daily_check(access_token)
                if signInCount != None:
                    reward(access_token, signInCount)
                capacty_info(access_token)
            with open('日志.log', mode='r', encoding='utf-8') as file:
                message = file.read()
                send_messages('🔥阿里云盘签到🔥\n\n' + message)
        except:
            logger.error('未知错误')
