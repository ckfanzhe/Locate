# ip定位接口的使用
# author:fanzhe date:8.22


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
    print(cookiedict)

    return cookiedict['ci_session']

def get_locate(key, debug=0):
    '''
    用于根据秘钥查询定位信息
    :param key: 查询的秘钥
    :param debug: 用于错误调试
    :return: 返回查询结果
    '''
    null = ''  # 定义返回的数据类型,防止错误


    re_data = {
        'key': str(key)
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    response = requests.get(url='https://met.red/h/tools/ipInfoList', headers=headers)
    cookies = getCookieByRequestUrl(response)
    if debug:
        print(response.text)
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
    url = 'https://met.red/h/tools/getKeyIpList'
    response = requests.post(url=url, data=re_data, headers=headers)
    if debug:
        print(response.text)
    result = eval(response.text)['code']


    if result==0:
        data = eval(response.text)['data']

        if debug:
            print('data:{}'.format(data))
            print(data[0])
            print(data[0]['ip'])
            print(data[0]['type'])
            print(data[0]['address'])
            print(data[0]['time'])
            print(data[0]['accuracy'])
        content = ''
        for s in data:
            print('\n s is:{}'.format(s))
            content = content + '\nip地址:' + s['ip'] + '\n定位类型:' + s['type'] + '\n位置:' + s['address'] + '\n点击时间:' + s['time']
        print(content)
        return [content]
    else:
        return ['error']


if __name__ == '__main__':
    key = '******'  # 测试代码所用秘钥,请改为自己的
    get_locate(key, 1)