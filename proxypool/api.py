import json
from flask import Flask, g
from proxypool.db import *

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


def get_conn():
    """
    获取
    :return:
    """
    website = 'all'
    # RedisClient("proxies", "baidu")
    setattr(g, website + '_proxies', eval('RedisClient' + '("proxies", "' + website + '")'))
    website = 'baidu'
    setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
    # RedisClient("accounts", "baidu")
    setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
    return g


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie, 访问地址如 /weibo/random
    :return: 随机Cookie
    """
    g = get_conn()
    if website == 'all':
        proxies = getattr(g, website + '_proxies').random()
        return proxies
    else:
        account = getattr(g, website + '_cookies').random()
        cookies = getattr(g, website + '_cookies').get(account)
        return {'account': account, 'cookies': cookies}


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    添加用户, 访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return: 
    """
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, website + '_proxies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
