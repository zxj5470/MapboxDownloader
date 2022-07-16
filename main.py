import os
import sys
import time

import requests
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import threading

# 配置文件目录
import config

lock = threading.Lock()
# 线程池
pool = ThreadPoolExecutor(max_workers=config.max_workers)

pat = config.pat
filename = config.filename
token = config.token
URL = "https://a.tiles.mapbox.com/v4/mapbox.terrain-rgb/{z}/{x}/{y}.png?access_token=" + token

headers = {
    'Host': 'a.tiles.mapbox.com',
    'Origin': 'http://localhost:3000',
    'Referer': 'http://localhost:3000/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
}

numOK = 0
allsize = 1


def _download(z, x, y, filename, errorlen=50):
    global numOK
    global allsize
    """
    :param z: 瓦片层级
    :param x:
    :param y:
    :param filename: 文件夹名称
    :param errorlen: 错误长度。认为返回小于50个字节就是错误数据。（Mapbox 的 forbidden），纯空白数据时为 800 个字节左右
    :return:
    """
    path = '%s/%s/%i/%i' % (pat, filename, z, x)

    # 文件夹不存在时创建
    if not os.path.isdir(path):
        os.makedirs(path)
    file = '%s/%i.png' % (path, y)

    # 文件存在时跳过
    if os.path.exists(file):
        with lock:
            numOK += 1
        return

    # 文件不存在开始下载
    url = URL
    map_url = url.format(x=x, y=y, z=z)
    r = requests.get(map_url, headers=headers)

    if (r.content.__len__() < errorlen):
        with lock:
            numOK += 1
        return
    with open(file, 'wb') as f:
        with lock:
            numOK += 1

        for chunk in r.iter_content(chunk_size=1024):
            if chunk and chunk:
                f.write(chunk)
                f.flush()


pools = []


def downloadZ(z):
    global allsize
    xrange = 1 << z
    for x in range(0, xrange):
        for y in range(0, xrange):
            a = pool.submit(_download, z, x, y, filename)
            pools.append(a)
    allsize = len(pools)


last = 0


def timerfun():
    global last
    while True:
        time.sleep(1)
        persec = numOK - last + 1
        rest = allsize - numOK
        print(persec, "每秒; 剩余", rest, "预计还需要", rest/persec,"秒", numOK/(allsize+1)*100, "%")
        last = numOK
        if (allsize == numOK):
            return


if __name__ == '__main__':
    zoom = config.zoom
    downloadZ(zoom)
    th = threading.Thread(target=timerfun)
    th.start()
    timer = threading.Timer(1, timerfun)
    wait(pools, return_when=ALL_COMPLETED, timeout=20)
