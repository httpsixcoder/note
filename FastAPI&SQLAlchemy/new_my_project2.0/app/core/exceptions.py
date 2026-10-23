"""
    自定义业务异常，区别于系统错误
"""


class BusinessException(Exception):
    def __init__(self, message: str):
        self.message = message
