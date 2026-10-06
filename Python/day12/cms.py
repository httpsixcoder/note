"""
    客户管理系统
"""
import sys

from customer import Customer


class CMS:
    """客户管理系统"""
    def __init__(self):
        # 创建用于存放客户信息的字典
        # key:customer_id       value:客户对象
        # {100:Customer(100,zs),200:Customer(200,zs)}
        self.customer_id_dict = {}
        # key:customer_name     value:客户对象字典
        # 例如：{"zs":{100:Customer(100,zs),200:Customer(200,zs)}}
        self.customer_name_dict = {}

    def start(self):
        """启动系统"""
        while True:
            self.display_menu()
            choice= int(input("请输入要执行的操作"))
            match choice:
                case 1:
                    print("添加客户")
                    self.add_customer()
                case 2:
                   print("删除客户")
                case 3:
                    print("修改客户")
                case 4:
                    print("查询客户")
                case 5:
                    print("显示所有客户")
                    self.show_all_customer()
                case 6:
                    print("已经成功退出系统")
                    sys.exit(0)
                case _:
                    print("请输入合理的操作")
    @staticmethod
    def display_menu():
        """显示菜单项"""
        print("----欢迎访问客户管理系统----")
        print(f"|{'1.添加客户':^20}|")
        print(f"|{'2.删除客户':^20}|")
        print(f"|{'3.修改客户':^20}|")
        print(f"|{'4.查询客户':^20}|")
        print(f"|{'5.显示所有的客户':^18}|")
        print(f"|{'6.退出系统':^20}|")
        print("-------------------------")

    def add_customer(self):
        """ 添加客户"""
        customer_id=self.add_customer_id()
        if  not customer_id :
            return
        customer_name=self.add_customer_name()
        if  not customer_name :
            return
        customer_age=self.set_customer_age()
        customer_email=self.set_customer_email()
        customer_phone=self.set_customer_phone()
        cus=Customer(customer_id,customer_name,customer_age,customer_email,customer_phone)
        # 添加id查找字典
        self.customer_id_dict[customer_id] = cus
        # 添加name查找字典
        if self.customer_name_dict.get(customer_name):
            self.customer_name_dict[customer_name][customer_id] = cus
        else:
            self.customer_name_dict[customer_name] = {customer_id: cus}
        print("用户添加成功")

    def add_customer_id(self):
        """添加客户id"""
        for i in range(3):
            if i<2:
                customer_id=input("请输入客户的id")
                if Customer.check_id(customer_id):
                    break
                else:
                    print("客户的id只能是数字")
            else:
                customer_id = input("最后一次机会，请珍惜，请输入客户的id")
                if Customer.check_id(customer_id):
                    break
                else:
                    print("机会耗尽，终止添加客户")
                    return False
        if customer_id in self.customer_id_dict:
            print("客户id已存在，终止添加客户")
            return False
        return customer_id

    @staticmethod
    def add_customer_name():
        """添加客户姓名"""
        for i in range(3):
            if i<2:
                customer_name=input("请输入客户的姓名")
                if Customer.check_name(customer_name):
                    break
                else:
                    print("客户的姓名只能是纯字母或数字")
            else:
                customer_name = input("最后一次机会，请珍惜，请输入客户的姓名")
                if Customer.check_name(customer_name):
                    break
                else:
                    print("机会耗尽，终止添加客户")
                    return False
        return customer_name

    @staticmethod
    def set_customer_age():
        """添加客户年龄"""
        customer_age = input("请输入客户的年龄")
        if Customer.check_age(customer_age):
            return customer_age
        else:
            print("输入的年龄不合理，使用默认值")
            return "None"

    @staticmethod
    def set_customer_email():
        """添加客户邮箱"""
        customer_email = input("请输入客户的邮箱")
        if Customer.check_email(customer_email):
            return customer_email
        else:
            print("输入的邮箱不合理，使用默认值")
            return "None"

    @staticmethod
    def set_customer_phone():
        """添加客户电话号"""
        customer_phone = input("请输入客户的电话号")
        if Customer.check_phone(customer_phone):
            return customer_phone
        else:
            print("输入的电话号不合理，使用默认值")
            return "None"

    def show_all_customer(self):
        """显示所有客户"""
        if len(self.customer_id_dict)==0:
            print("暂时还没有客户")
        else:
            print("-"*113)
            for cus in self.customer_id_dict.values():
                print(cus)
            print("-"*113)


if __name__ == "__main__":
    c = CMS()
    c.start()

