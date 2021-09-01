from proxypool.db import RedisClient


if __name__ == '__main__':
    con = RedisClient()
    print(con.pop())
