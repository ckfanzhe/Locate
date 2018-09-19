# ip定位api使用
# author:fanzhe date:8.22

import re
import requests
import random

def getCookieByRequestUrl(response):

    """
    根据请求的响应获取cookie信息
    :param response: 请求网站后的响应
    :return:
    """
    cookiejar = response.cookies
    cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    # print(cookiedict)

    return cookiedict['ci_session']


def get_link(key, debug=0):
    '''
    用于获取定位用的链接
    :param key:用于生成定位链接的秘钥
    :param debug: 用于查看错误信息
    :return:
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    re_data = {
        'key': str(key)
    }
    response = requests.get(url='https://met.red/h/tools/createMyUrl/', headers=headers)
    cookies = getCookieByRequestUrl(response)
    
    if debug:
        print(cookies)
        
    cookies_ci = 'ci_session=' + str(cookies)
    temp_value = random.randint(5000,8000)
    cookiesvalue = cookies_ci + '; Hm_lvt_6566ca99331702c0cf4223d9fcca30c1=153490{};Hm_lpvt_6566ca99331702c0cf4223d9fcca30c1=153490{};'.format(temp_value,temp_value)
    
    if debug:
        print(cookiesvalue)
    
    
    headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'15',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':cookiesvalue,
    'Host':'met.red',
    'Origin':'https://met.red',
    'Referer':'https://met.red/h/tools/createMyUrl',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }


    
    # 判断值：
    if debug:
        print(re_data)
    url = 'https://met.red/h/tools/saveMyUrl'
    response = requests.post(url=url, data=re_data, headers=headers)  # 获取根据秘钥生成的链接
    if debug:
        print(response.text)

    result= eval(response.text)['code']
    if result==0:
        # 方案一正则匹配结果
        local_url = re.search(r'server=(.*)"',str(response.content)).group(1)
        final = 'https://met.red/h/index/push?server=' + str(local_url)
        return [final]
    else:
        # print('秘钥错误或者已经被使用')
        return ['error']
if __name__ == '__main__':
    key = '******'  # 测试代码用秘钥,请每次改成不同值
    get_link(key,1)