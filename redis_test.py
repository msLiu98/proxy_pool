from proxypool.db import RedisClient


if __name__ == '__main__':
    con = RedisClient('proxies')
    print(con.random())
