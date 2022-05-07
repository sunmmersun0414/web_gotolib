
from pywebio.input import *
from pywebio.output import *
# from pywebio.pin import *
from pywebio import start_server
import urllib.request
import urllib.parse
import http.cookiejar
import threading
from code_go import go_main

passwordtoid = {}

def get_cookie(url):
    def get_code(url):
        query = urllib.parse.urlparse(url).query
        codes = urllib.parse.parse_qs(query).get('code')
        if codes:
            return codes.pop()
        else:
            raise ValueError("Code not found in URL")

    def get_cookie_string(code):
        cookiejar = http.cookiejar.MozillaCookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
        response = opener.open(
            "http://wechat.v2.traceint.com/index.php/urlNew/auth.html?" + urllib.parse.urlencode({
                "r": "https://web.traceint.com/web/index.html",
                "code": code,
                "state": 1
            })
        )
        cookie_items = []
        for cookie in cookiejar:
            cookie_items.append(f"{cookie.name}={cookie.value}")
        cookie_string = '; '.join(cookie_items)
        return cookie_string

    code = get_code(url)
    cookie_string = get_cookie_string(code)
    return cookie_string

def read_password():
    # with open("./激活码.txt", "w")as fp:
    #     password_strs = fp.readline()
    #     print(password_strs)
    fo1 = open('./激活码.txt', 'r')
    lines2 = [l.split() for l in fo1.readlines() if l.strip()]
    # print(lines2)
    return lines2
def check_pwd():

    def check_id_password(id,pwd):
        global pwd_sign
        if pwd in passwordtoid.values():
            try:
                if passwordtoid[id] == pwd:
                    pwd_sign = 1
                else:
                    return '授权码和账号不匹配，请确认！'
            except:
                return '授权码和账号不匹配，请确认！'
        else:
            passwordtoid[id] = pwd
            print('passwordtoid: ', passwordtoid)
            pwd_sign = 1
            return 'ok'
    # input的合法性校验
    # 自定义校验函数
    # 密码框
    global pwd_sign
    pwd_sign = 0
    pwd = input('请输入授权码:', type=TEXT, help_text='详情咨询sun.h.w@foxmail.com')
    id = input('请输入账号(第一次使用可以自定义，自己要记住哦~):', type=TEXT, help_text='详情咨询sun.h.w@foxmail.com')
    def check_passowrd(pwd):
        password_strs = read_password()
        # pwd_res = input("请输入授权码:", type=TEXT)
        # print('password:', pwd, '@@', [pwd] in password_strs)
        print('pwd: ',pwd,'   ','id: ',id)
        if [pwd] not in password_strs:
            put_text('授权码错误，请确认！')
            return '授权码错误，请确认！'
        elif [pwd] in password_strs:
            check_return=check_id_password(id,pwd)
            # if pwd in passwordtoid.values():
            #     try:
            #         if passwordtoid[id] == pwd:
            #             pwd_sign = 1
            #         else:
            #             return '授权码和账号不匹配，请确认！'
            #     except:
            #         return '授权码和账号不匹配，请确认！'
            # else:
            #     passwordtoid[id] = pwd
            #     print('passwordtoid: ',passwordtoid)
            put_text(check_return)
            if pwd_sign:
                input_input()
                return True
            else:
                put_text(check_return)
                check_pwd()
    check_passowrd(pwd)


    return pwd_sign



def input_input():
    re_mail = input('输入希望接收通知的邮箱地址(不想接收可以不写):', type=TEXT, help_text='详情咨询sun.h.w@foxmail.com')
    # radio_res = radio(
    #     '选座期望场所',
    #     options=['一楼走廊 (一楼)', '一楼学生自修室 (一楼)', '二楼走廊 (二楼)','201科技图书借阅Ⅰ室 (2楼)',
    #              '202科技图书借阅Ⅱ室 (2楼)','三楼走廊 (三楼)','302社科图书借阅Ⅰ室 (3楼)','305社科图书借阅Ⅱ室 (3楼)',
    #              '四楼走廊 (四楼)','406社科图书借阅Ⅲ室 (4楼)']
    # )

    # select_res = select("选座期望场所:", ['一楼走廊 (一楼)', '一楼学生自修室 (一楼)', '二楼走廊 (二楼)','201科技图书借阅Ⅰ室 (2楼)',
    #              '202科技图书借阅Ⅱ室 (2楼)','三楼走廊 (三楼)','302社科图书借阅Ⅰ室 (3楼)','305社科图书借阅Ⅱ室 (3楼)',
    #              '四楼走廊 (四楼)','406社科图书借阅Ⅲ室 (4楼)'])


    put_image(open('code.png', 'rb').read(),width='20%',height='20%')
    put_text('请用微信扫一扫，授权登录后复制网址填入！(无需在意网页内容！)')
    myAge = input('输入获得的地址:', type=URL, help_text='详情咨询sun.h.w@foxmail.com')
    print('myAge is:', myAge)
    def check_age(url,re_mail):
        try:
            cookie_string = get_cookie(url)
            put_text(cookie_string)
            # cookie_string = {"cookie":cookie_string}
            # cookie = get_cookie(cookie_string)
            from util.utils import often_seat
            oftenseat = often_seat(cookie_string)
            put_text(oftenseat)
            # seat_tmp=input(label="位置信息", name='seat', type=TEXT, value=oftenseat[0] + '和' + oftenseat[3], readonly=True)
            threading.Thread(target=go_main, args=[cookie_string,re_mail,oftenseat]).start()
            return cookie_string
        except:
            put_text('地址错误：请重试!')
            return '错误：请重试!'

    # myAge = input('输入获得的地址:', type=URL, help_text='详情咨询sun.h.w@foxmail.com')
    # print('myAge is:', myAge)
    # put_text('请用以下内容替换掉status.json文件中cookie:后的内容（注意最后括号保留）')
    print(check_age(myAge,re_mail))



if __name__ == '__main__':
    start_server(applications=[check_pwd, ],
        debug=False,
        auto_open_webbrowser=False,
        remote_access=True,port=54643,reconnect_timeout=5)
    # start_server(
    #     applications=[input_input, ],
    #     debug=True,
    #     auto_open_webbrowser=False,
    #     remote_access=True,
    # )


