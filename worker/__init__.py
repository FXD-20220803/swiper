import os
from celery import Celery

# 1. 设置环境变量，加载 Django 的 settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')

# 2. 创建 Celery Application
celery_app = Celery('swiper')
celery_app.config_from_object('worker.config')  # 3. 加载celery配置文件
celery_app.autodiscover_tasks()  # 4. 自动发现通过装饰器定义的所有任务


# windows启动命令：celery -A worker worker --loglevel=info -P eventlet
# linux启动命令：celery -A worker worker --loglevel=info
# 加日志的话 之前命令加上 --logfile="worker/celery_app.log"

def call_by_worker(func):
    """将任务在 Celery 中异步执行, 只需要将此函数作为装饰器使用，就可以免去一些频繁的操作"""
    task = celery_app.task(func)
    # task.delay 将task加到异步任务里面
    return task.delay
