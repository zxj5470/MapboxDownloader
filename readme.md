# Mapbox 瓦片下载

> 当前使用版本 Python 3.8
> 依赖：requests=2.28.1   
> 可下载 Mapbox 瓦片地图，也可以下载高程地图，只需要修改名称即可。


## 可能需要修改的代码：

- `filename`: 修改保存的文件路径，默认在当前目录 `tiles/{filename}` 下。
- `downloadZ(zoom)` 下载的瓦片层级
- `token` mapbox token，用官网的 token 居然可以正常下载emmmm

```python
filename = "mapbox-terrain"

# 要下载的瓦片层级
zoom = 1
downloadZ(zoom)
```

## 执行
```commandline
python main.py
```

## 数据情况

下载第 8 层大约需要 20 分钟。

目前已知的数据量 (TerrainRGB)
```
32K     ./0
120K    ./1
432K    ./2
1.7M    ./3
6.0M    ./4
22M     ./5
191M    ./6
672M    ./7
2.21G     ./8
```