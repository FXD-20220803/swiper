# 配置代理人，指定代理人将任务存到哪里,这里是redis的0号库
broker_url = 'redis://82.157.36.220:6379/0'
broker_pool_limit = 1000

# 设置时区，默认UTC
timezone = 'Asia/Shanghai'
# using serializer name
accept_content = ['pickle', 'json']

task_serializer = 'pickle'

result_backend = 'redis://82.157.36.220:6379/1'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量
result_expires = 3600  # 任务结果的过期时间

worker_redirect_stdouts_level = 'INFO'
