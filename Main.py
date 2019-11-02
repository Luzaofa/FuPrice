__author__ = 'Luzaofa'
__date__ = '2019/11/1 21:30'

import os
import time
import random
import requests
import configparser

from WeChat import WeChat


class Config(object):
    '''解析配置文件'''

    def get_config(self, lable, value):
        cf = configparser.ConfigParser()
        cf.read("CONFIG.conf", encoding="utf-8")
        config_value = cf.get(lable, value)
        return config_value


PRICE = 0


class Pros(Config):

    def __init__(self):
        '''读取配置文件夹信息初始化 [lable] value = value'''
        super(Config, self).__init__()
        self.contract1 = self.get_config('contracts', 'contract1')
        self.contract2 = self.get_config('contracts', 'contract2')
        self.contract3 = self.get_config('contracts', 'contract3')
        self.spread = self.get_config('spread', 'spread')
        code = self.get_config('code', 'code')  # 发送方式（0：用户 1：群）
        user = self.get_config('user', 'user')  # 好友昵称（回身挽流光） / 群名称（软件测试）
        self.wx = WeChat(user=user, code=int(code))

    def get_price(self, code):
        url = 'https://hq.sinajs.cn/&list=nf_{0}'.format(code)
        response = requests.get(url=url).text
        vulues = response.split(',')[1:15]
        # 当前时间、开盘价、最高价、最低价、0、买价、卖价、最新价、0、昨日结算价、买量、卖量、持仓量、成交量
        return int(float(vulues[7]))

    def main(self):
        '''
        主入口
        :return:
        '''
        global PRICE
        while True:
            now_time = time.strftime("%H:%M:%S")
            # now_time = '09:01:00'
            # with open('time.txt', 'r') as f:
            #     value = f.read()
            #     now_time = str(value.strip())
            # print(now_time, '------')

            sleep_time = random.randint(10, 15)
            # 非交易时间段
            if (now_time > '01:00:15' and now_time < '09:00:00') or (
                    now_time > '10:15:15' and now_time < '10:30:00') or (
                    now_time > '11:30:15' and now_time < '13:30:00') or (
                    now_time > '15:00:15' and now_time < '21:00:00'):
                print('当前时间【%s】非交易时间' % (now_time))

            # 开盘、收盘报价时间段
            elif (now_time >= '09:00:00' and now_time <= '09:00:15') or (
                    now_time >= '10:15:00' and now_time <= '10:15:15') or (
                    now_time >= '10:30:00' and now_time <= '10:30:15') or (
                    now_time >= '11:30:00' and now_time <= '11:30:15') or (
                    now_time >= '13:30:00' and now_time <= '13:30:15') or (
                    now_time >= '15:00:00' and now_time <= '15:00:15') or (
                    now_time >= '21:00:00' and now_time <= '21:00:15') or (
                    now_time >= '01:00:00' and now_time <= '01:00:15'):
                quote_price = '%s %s %s' % (
                    self.get_price(self.contract1), self.get_price(self.contract2), self.get_price(self.contract3))
                contents = quote_price  # 发送内容
                PRICE = self.get_price(self.contract2)
                self.wx.main(contents, now_time)
                with open('price.txt', 'w') as f:
                    f.write(str(self.get_price(self.contract2)))

            # 盘内报价时间段
            else:
                if os.path.exists('./price.txt'):
                    # 获取报价值
                    with open('price.txt', 'r') as f:
                        value = f.read()
                        PRICE = int(value.strip())

                new_price = self.get_price(self.contract2)
                if abs(new_price - PRICE) >= int(self.spread):
                    quote_price = '%s %s %s' % (
                        self.get_price(self.contract1), new_price, self.get_price(self.contract3))
                    contents = quote_price  # 发送内容
                    self.wx.main(contents, now_time)
                    PRICE = new_price

                    # 更新报价值
                    with open('price.txt', 'w') as f:
                        f.write(str(new_price))

                if int(now_time.split(':')[0]) >= 9 and int(now_time.split(':')[0]) <= 11:
                    print('【%s】正在早盘交易【当前价格为:%s;前期报价为:%s】' % (now_time, new_price, PRICE))
                elif int(now_time.split(':')[0]) >= 13 and int(now_time.split(':')[0]) <= 15:
                    print('【%s】正在午盘交易【当前价格为:%s;前期报价为:%s】' % (now_time, new_price, PRICE))
                else:
                    print('【%s】正在晚盘交易【当前价格为:%s;前期报价为:%s】' % (now_time, new_price, PRICE))

            time.sleep(sleep_time)


if __name__ == '__main__':
    print('Start！')
    pro = Pros()
    pro.main()
    print('END')
