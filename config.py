# 路径: {pat}/{filename}/{z}/{x}/{y}
pat = "G:/Data"
filename = "mapbox-terrain"

# 下载层级
zoom = 9
# 这个 token 是 mapbox 官网扒下来的。说不定哪天就不能用了……后续有能力的话自己去更新啊！！！
token = "pk.eyJ1IjoiZXhhbXBsZXMiLCJhIjoiY2p0MG01MXRqMW45cjQzb2R6b2ptc3J4MSJ9.zA2W0IkI0c6KaAhJfk9bWg"

# 最大并发，建议设置为 CPU * 4 甚至更多
max_workers = 96