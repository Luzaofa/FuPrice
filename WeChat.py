__author__ = 'Luzaofa'
__date__ = '2019/11/1 19:49'

import os
import time
import itchat
import datetime
import configparser


class Config(object):
    '''解析配置文件'''

    def get_config(self, lable, value):
        cf = configparser.ConfigParser()
        cf.read("CONFIG.conf")
        config_value = cf.get(lable, value)
        return config_value


class WeChat(object):
    '''给微信好友或群发送指定消息'''

    def __init__(self, user, code):
        '''
        自动登录方法，hotReload=True可以缓存，不用每次都登录
        但是第一次执行时会出现一个二维码，需要手机微信扫码登录
        '''
        itchat.auto_login(hotReload=True)
        self.TOUSER = user  # 好友昵称
        self.TOROOM = user  # 群名称
        self.CODE = code  # 发送方式（0：用户 1：群）

    def send_2_user(self, contents):
        '''
        功能描述:发送信息到个人
        :param contents: 文本信息
        :return:
        '''
        try:
            userfinfo = itchat.search_friends(self.TOUSER)
            if len(userfinfo) > 0:
                userid = userfinfo[0]["UserName"]
                itchat.send_msg(msg=contents, toUserName=userid)
                print('当前时间:【{0}】用户:【{1}】信息发送成功【{2}】'.format(time.strftime("%H:%M:%S"), self.TOUSER, contents))
            else:
                print('未获取到用户信息')
        except Exception as e:
            print('用户:【{0}】信息发送失败'.format(self.TOUSER), e)

    def send_2_rooms(self, contents, now_time):
        '''
        功能描述:发送信息到群
        :param contents: 文本信息
        :return:
        '''
        try:
            chatroomName = self.TOROOM
            itchat.get_chatrooms(update=True)
            chatrooms = itchat.search_chatrooms(name=chatroomName)
            if len(chatrooms) > 0:
                chatroom = chatrooms[0]["UserName"]
                itchat.send(contents, toUserName=chatroom)
                print('当前时间:【{0}】报价信息已成功发送到【{1}】【{2}】'.format(now_time, self.TOROOM, contents))
            else:
                print('未获取到群信息!')
        except Exception as e:
            print('报价信息向【{0}】发送失败!'.format(self.TOROOM), e)

    def main(self, contents, now_time):
        '''
        逻辑模块
        :param contents: 发送的信息
        :return:
        '''
        try:
            f = './itchat.pkl'
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%H')
                if int(mtime) < int(time.localtime().tm_hour):
                    os.remove('./itchat.pkl')
                    print('超过一小时，需重新登陆！')
            except:
                pass

            if self.CODE == 0:
                self.send_2_user(contents)
            elif self.CODE == 1:
                self.send_2_rooms(contents, now_time)
            else:
                print('请选择合适的发送方式！')
        except Exception:
            print('无法正常登陆！')


if __name__ == '__main__':
    code = 0  # 发送方式（0：用户 1：群）
    user = '回身挽流光'  # 好友昵称（回身挽流光） / 群名称（软件测试）
    contents = '软件测试'  # 发送内容
    wx = WeChat(user=user, code=code)
    wx.main(contents)
