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
        # key:customer_name     value:客户对象字典{id:客户对象}
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
                    self.delete_customer()
                case 3:
                    print("修改客户")
                    self.update_customer()
                case 4:
                    print("查询客户")
                    self.search_customer()
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
                    print("客户的姓名只能是纯字母")
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

    def search_customer(self):
        """搜索客户"""
        search_type=input("请输入客户的id或者姓名")
        if Customer.check_id(search_type):
            if search_type in self.customer_id_dict:
                print("-" * 113)
                print(self.customer_id_dict[search_type])
                print("-" * 113)
            else:
                print(f"不存在id为{search_type}的客户")
        elif Customer.check_name(search_type):
            if search_type in self.customer_name_dict:
                print("-" * 113)
                for cus in self.customer_name_dict[search_type].values():
                    print(cus)
                print("-" * 113)
            else:
                print(f"不存在姓名为{search_type}的客户")
        else:
            print("搜索内容不合法")

    def update_customer(self):
        """修改客户信息"""
        # 【只修改customer_id_dict就可以，因为customer_name_dict和customer_id_dict指向同一个对象】
        customer_id=input("请输入客户id")
        if Customer.check_id(customer_id):
            if customer_id in self.customer_id_dict:
                # age
                print(f"旧的客户的年龄为{self.customer_id_dict[customer_id].c_age}")
                customer_age=input("请输入新的年龄信息")
                if Customer.check_age(customer_age):
                    self.customer_id_dict[customer_id].c_age=customer_age
                    print(f"修改成功，客户的年龄为{self.customer_id_dict[customer_id].c_age}")
                else:
                    print(f"修改失败，年龄不合法，已保存原有数据")
                # email
                print(f"旧的客户的邮箱为{self.customer_id_dict[customer_id].c_email}")
                customer_email = input("请输入新的邮箱信息")
                if Customer.check_email(customer_email):
                    self.customer_id_dict[customer_id].c_email = customer_email
                    print(f"修改成功，客户的邮箱为{self.customer_id_dict[customer_id].c_email}")
                else:
                    print(f"修改失败，邮箱不合法，已保存原有数据")
                # phone
                print(f"旧的客户的手机号为{self.customer_id_dict[customer_id].c_phone}")
                customer_phone = input("请输入新的手机号信息")
                if Customer.check_phone(customer_phone):
                    self.customer_id_dict[customer_id].c_phone = customer_phone
                    print(f"修改成功，客户的手机号为{self.customer_id_dict[customer_id].c_phone}")
                else:
                    print(f"修改失败，手机号不合法，已保存原有数据")
            else:
                print(f"不存在id为{customer_id}的客户")
        else:
            print("客户id不合法")

    def delete_customer(self):
        """删除客户"""
        # 删除需要删除customer_id_dict和customer_name_dict两个【因为引用为2，需要都做删除操作】
        customer_id=input("请输入想要删除的客户id")
        if Customer.check_id(customer_id):
            if customer_id in self.customer_id_dict:
                customer_name=self.customer_id_dict[customer_id].c_name
                # 删除 customer_id_dict
                del self.customer_id_dict[customer_id]
                # 删除 customer_name_dict
                if len(self.customer_name_dict[customer_name])==1:
                    del self.customer_name_dict[customer_name]
                else:
                    del self.customer_name_dict[customer_name][customer_id]
                print("删除成功")
            else:
                print(f"不存在id为{customer_id}的客户")
        else:
            print("客户id不合法")



if __name__ == "__main__":
    c = CMS()
    c.start()

