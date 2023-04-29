# -*- coding: utf-8 -*-
"""
//更新时间：2023/4/29
//作者：wdvipa
//支持青龙和actions定时执行
//使用方法：创建变量 名字：cg163 内容的写法：Authorization  多个账号用回车键隔开
//例如: 
bearer 11111
bearer 22222
//更新内容：支持青龙执行
//如需推送将需要的推送写入变量cg163_fs即可多个用&隔开
如:变量内输入push需再添加cg163_push变量 内容是push的token即可
"""
import requests
import os
import time
import re
import json

requests.urllib3.disable_warnings()

#------------------设置-------------------
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'

#初始化环境变量开头
cs = 0
ZData = "5"
ttoken = ""
tuserid = ""
push_token = ""
SKey = ""
QKey = ""
ktkey = ""
msgs = ""
datas = ""
message = ""
#检测推送
if cs == 1:
  if "cs_cg163" in os.environ:
    datas = os.environ.get("cs_cg163")
  else:
    print('您没有输入任何信息')
    exit
if cs == 2:
    datas =""
else:
  if "cg163_fs" in os.environ:
    fs = os.environ.get('cg163_fs')
    fss = fs.split("&")
    if("tel" in fss):
        if "cg163_telkey" in os.environ:
            telekey = os.environ.get("cg163_telkey")
            telekeys = telekey.split('\n')
            ttoken = telekeys[0]
            tuserid = telekeys[1]
    if("qm" in fss):
        if "cg163_qkey" in os.environ:
            QKey = os.environ.get("cg163_qkey")
    if("stb" in fss):
        if "cg163_skey" in os.environ:
            SKey = os.environ.get("cg163_skey")
    if("push" in fss):
        if "cg163_push" in os.environ:
            push_token = os.environ.get("cg163_push")
    if("kt" in fss):
        if "cg163_ktkey" in os.environ:
            ktkey = os.environ.get("cg163_ktkey")
  if "cg163" in os.environ:
    datas = os.environ.get("cg163")
  else:
    print('您没有输入任何信息')
    exit
groups = datas.split('\n')
#初始化环境变量结尾

class cg163anelQd(object):
    def __init__(self,au):
        # Authorization
        self.au = au
        ##############推送渠道配置区###############
        # 酷推qq推送
        #self.ktkey = ktkey
        # Telegram私聊推送
        self.tele_api_url = 'https://api.telegram.org'
        self.tele_bot_token = ttoken
        self.tele_user_id = tuserid
        ##########################################


    def buildHeaders(self,authorization):  # 更改headers
        session.headers["Authorization"] = authorization


    def check(self):  # 验证
        current = 'https://n.cg.163.com/api/v2/client-settings/@current'
        result = requests.get(url=current, headers=session.headers)
        return result


    def sign(self):  # 签到
        sign_url = 'https://n.cg.163.com/api/v2/sign-today'
        result = requests.post(url=sign_url, headers=session.headers)
        return result

    
    # Qmsg私聊推送
    def Qmsg_send(msg):
        if QKey == '':
            return
        qmsg_url = 'https://qmsg.zendee.cn/send/' + str(QKey)
        data = {
            'msg': msg,
        }
        requests.post(qmsg_url, data=data)

    # Server酱推送
    def server_send(self, msg):
        if SKey == '':
            return
        server_url = "https://sctapi.ftqq.com/" + str(SKey) + ".send"
        data = {
            'text': self.name + "大学习通知",
            'desp': msg
        }
        requests.post(server_url, data=data)

    # 酷推QQ推送
    def kt_send(msg):
        if ktkey == '':
            return
        kt_url = 'https://push.xuthus.cc/send/' + str(ktkey)
        data = ('大学习完成，点击查看详细信息~\n' + str(msg)).encode("utf-8")
        requests.post(kt_url, data=data)

    #Telegram私聊推送
    def tele_send(self, msg: str):
        if self.tele_bot_token == '':
            return
        tele_url = f"{self.tele_api_url}/bot{self.tele_bot_token}/sendMessage"
        data = {
            'chat_id': self.tele_user_id,
            'parse_mode': "Markdown",
            'text': msg
        }
        requests.post(tele_url, data=data)
        
    # Pushplus推送
    def pushplus_send(msg):
        if push_token == '':
            return
        token = push_token
        title= '大学习通知'
        content = msg
        url = 'http://www.pushplus.plus/send'
        data = {
            "token":token,
            "title":title,
            "content":content
            }
        body=json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type':'application/json'}
        re = requests.post(url,data=body,headers=headers)
        print(re.status_code)


    def main(self):
        global msgs
        # 更新Authorization
        self.buildHeaders(au)
        #检测账号
        self.checkReturn = self.check()
        if self.checkReturn.status_code == 200:
            self.checkResult = "成功"
            #每日签到
            self.signReturn = self.sign()
            if self.signReturn.status_code == 200:
                self.signResult = "成功"
            elif self.signReturn.status_code == 400:
                self.signResult = "你已经签到过了"
            else:
                self.signResult = "失败，code=" + \
                str(self.signReturn.status_code)+"，请通过code判断失败原因"
        elif self.checkReturn.status_code == 401:
            self.checkResult = "登录信息可能已经失效"
            self.signResult = "账号验证失败，无法签到"
        else:
            self.checkResult = "失败，code="+str(self.checkReturn.status_code)+"，请通过code判断失败原因"
            self.signResult = "账号验证失败，无法签到"
        message = '''⏰当前时间：{} 
        网易云游戏签到
    ####################
    🧐账号验证：{}
    💻签到结果：{}
    ####################
    祝您过上美好的一天！'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),
                          self.checkResult,
                          self.signResult)
        print(message)
        msgs = msgs + '\n' + message
        return message


if __name__ == '__main__':  # 直接运行和青龙入口
  i = 0
  n = 0
  print("已设置不显示账号密码等信息")
  while i < len(groups):
    n = n + 1
    group = groups[i]
    au = group
    msgs = msgs + "第" + str(n) + "用户的签到结果"
    print("第" + str(n) + "个用户开始签到")
    session = requests.session()
    #--------------------以下非特殊情况不要动---------------------
    session.headers = {
      'Authorization': '', 
      'Connection': 'keep-alive',
      'Content-Length': '0',
      'Accept': 'application/json, text/plain, */*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
      'Host': 'n.cg.163.com',
      'Origin': 'https://cg.163.com',
      'Referer': 'https://cg.163.com/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-site',
      'User-Agent': UserAgent,
      'X-Platform': '0'
    }
    #--------------------以上非特殊情况不要动---------------------
    run = cg163anelQd(au)
    run.main()
    time.sleep(5)
    i += 1
  else:
    #cg163anelQd.server_send( msgs )
    cg163anelQd.kt_send( msgs )
    #cg163anelQd.Qmsg_send(cg163anelQd.name+"\n"+cg163anelQd.email+"\n"+ msgs)
    #cg163anelQd.tele_send(cg163anelQd.name+"\n"+cg163anelQd.email+"\n"+ msgs)
    cg163anelQd.pushplus_send( msgs )
