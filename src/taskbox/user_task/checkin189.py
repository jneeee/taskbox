import base64
import re
import time

import requests
import rsa

from taskbox.taskbase.task import Task
from taskbox.utils.tools import LOG


__all__ = ['Cloud189']

class CheckIn(object):
    client = requests.Session()
    login_url = "https://cloud.189.cn/api/portal/loginUrl.action?" \
                "redirectURL=https://cloud.189.cn/web/redirect.html?returnURL=/main.action"
    submit_login_url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
    sign_url = ("https://api.cloud.189.cn/mkt/userSign.action?rand=%s"
                "&clientType=TELEANDROID&version=8.6.3&model=SM-G930K")

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.res = []

    def check_in(self):
        self.login()
        rand = str(round(time.time() * 1000))
        url = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN"
        url2 = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                          ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                          "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                          "4 clientChannelId/qq proVersion/1.0.6",
            "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
            "Host": "m.cloud.189.cn",
            "Accept-Encoding": "gzip, deflate",
        }
        response = self.client.get(self.sign_url % rand, headers=headers)
        net_disk_bonus = response.json()["netdiskBonus"]
        if response.json()["isSign"] == "false":
            self.res.append(f"未签到，签到获得 {net_disk_bonus}M 空间")
        else:
            self.res.append(f"已经签到过了，签到获得 {net_disk_bonus}M 空间")
        response = self.client.get(url, headers=headers)
        if "errorCode" in response.text:
            self.res.append(response.text)
        else:
            prize_name = (response.json() or {}).get("prizeName")
            self.res.append(f"抽奖获得 {prize_name}")
        response = self.client.get(url2, headers=headers)
        if "errorCode" in response.text:
            self.res.append(response.text)
        else:
            prize_name = (response.json() or {}).get("prizeName")
            self.res.append(f"抽奖获得 {prize_name}")
        return self.res

    @staticmethod
    def rsa_encode(rsa_key, string):
        rsa_key = f"-----BEGIN PUBLIC KEY-----\n{rsa_key}\n-----END PUBLIC KEY-----"
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
        result = _b64_to_hex((base64.b64encode(rsa.encrypt(f"{string}".encode(), pubkey))).decode())
        return result

    def login(self):
        r = self.client.get(self.login_url)
        captcha_token = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
        lt = re.findall(r'lt = "(.+?)"', r.text)[0]
        return_url = re.findall(r"returnUrl = '(.+?)'", r.text)[0]
        param_id = re.findall(r'paramId = "(.+?)"', r.text)[0]
        j_rsa_key = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
        self.client.headers.update({"lt": lt})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0",
            "Referer": "https://open.e.189.cn/",
        }
        data = {
            "appKey": "cloud",
            "accountType": "01",
            "userName": f"{{RSA}}{self.rsa_encode(j_rsa_key, self.username)}",
            "password": f"{{RSA}}{self.rsa_encode(j_rsa_key, self.password)}",
            "validateCode": "",
            "captchaToken": captcha_token,
            "returnUrl": return_url,
            "mailSuffix": "@189.cn",
            "paramId": param_id,
        }
        r = self.client.post(self.submit_login_url, data=data, headers=headers, timeout=5)
        LOG.info(r.json()["msg"])
        if '图形验证码错误' in r.json()["msg"]:
            raise Exception("账户风控中，请手动登录后重试")
        redirect_url = r.json()["toUrl"]
        self.client.get(redirect_url)


def _b64_to_hex(a):
    def _chr(a):
        return "0123456789abcdefghijklmnopqrstuvwxyz"[a]
    b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    d = ""
    e = 0
    c = 0
    for i in range(len(a)):
        if list(a)[i] != "=":
            v = b64map.index(list(a)[i])
            if 0 == e:
                e = 1
                d += _chr(v >> 2)
                c = 3 & v
            elif 1 == e:
                e = 2
                d += _chr(c << 2 | v >> 4)
                c = 15 & v
            elif 2 == e:
                e = 3
                d += _chr(c)
                d += _chr(v >> 2)
                c = 3 & v
            else:
                e = 0
                d += _chr(c << 2 | v >> 4)
                d += _chr(15 & v)
    if e == 1:
        d += _chr(c << 2)
    return d


class Cloud189(Task):

    name_zh = '天翼云盘签到'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def step(self, config_d):
        res = CheckIn(config_d.get('phone'), config_d.get('pswd189')).check_in()
        # 'checkin189' : {'time':x, 'checkin_space':x, 'lottery_space':x, 'total':x}
        return res

    def get_conf_list(self):
        return {
            'phone': '电话号码',
            'pswd189': '密码',
        }

Cloud189.register()
