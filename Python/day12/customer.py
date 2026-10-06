"""
    客户类
"""
import re


class Customer:
    """客户类"""

    def __init__(self, c_id, c_name, c_age="None", c_phone="None", c_email="None"):
        self.c_id = c_id
        self.c_name = c_name
        self.c_age = c_age
        self.c_phone = c_phone
        self.c_email = c_email

    def __str__(self):
        return (f"|ID:|{self.c_id:<15} |Name:|{self.c_name:<15} |Age:|{self.c_age:<15}"
                f"|Phone:|{self.c_phone:<15} |Email:|{self.c_email:<15}|")

    # 类方法 静态方法
    @staticmethod
    def check_id(c_id):
        return c_id.isdigit()

    @staticmethod
    def check_name(c_name):
        return c_name.isalpha()

    @staticmethod
    def check_age(c_age):
        pattern_age = r"^(?:0|[1-9]\d?|1[01]\d|120)$"
        return bool(re.fullmatch(pattern_age, c_age))

    @staticmethod
    def check_phone(c_phone):
        pattern_phone = r"^1[3-9]\d{9}$"
        return bool(re.fullmatch(pattern_phone, c_phone))

    @staticmethod
    def check_email(c_email):
        pattern_email = r"^[\w.\-]+@[\w\-]+(\.[\w\-]+)+$"
        return bool(re.fullmatch(pattern_email, c_email))
