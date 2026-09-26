"""
    该案例演示了愤怒的小鸟
"""
class Birds:
    def __init__(self, name, color,skill_description):
        self.name = name
        self.color = color
        self.skill_description = skill_description
    def fly(self):
        print(f"{self.name}正在飞行...")
    def call(self):
        print(f"{self.name} 发出叫声...")
    def use_skill(self):
        print(f"{self.name}使用了技能：{self.skill_description}")

class RedBirds(Birds):
    def __init__(self):
        super().__init__("红火", "红色", "撞击前方障碍物，造成大量伤害")
    def fly(self):
        print("红火稳定飞行...")
    def call(self):
        print("红火发出嗷~嗷~嗷~")

class YellowBirds(Birds):
    def __init__(self):
        super().__init__("小黄", "黄色", "瞬间加速，穿透薄障碍物")

    def fly(self):
        print("小黄快速向前飞行...")

    def call(self):
        print("小黄发出嗖~嗖~嗖~")


class BlueBirds(Birds):
    def __init__(self):
        super().__init__("小蓝", "蓝色", "分裂成三只小鸟，分散攻击")

    def fly(self):
        print("小蓝优雅向前飞行...")
    def call(self):
        print("小蓝发出阿~嘿~阿~嘿~阿~嘿~")


class Obstacle:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength
    def be_attacked(self,bird):
        print(f"{bird.name} 冲向了 {self.name}")
        bird.use_skill()
        if isinstance(bird, RedBirds):
            damage = 80
        elif isinstance(bird, YellowBirds):
            damage = 50
        elif isinstance(bird, BlueBirds):
            damage = 30 * 3
        self.strength -= damage
        if self.strength<0:
            self.strength = 0
            print(f"{self.name} 被摧毁了！")
        else:
            print(f"{self.name} 还剩余 {self.strength} 点强度")

# 模拟游戏过程【入口判断语句】
# if __name__ == "__main__":
"""
在 Python 中，每个文件（模块）都有一个内置变量叫 __name__。
情况 A：你直接运行这个 .py 文件
    比如你在终端敲 python game.py。
    此时 Python 会把 __name__ 的值设为 "__main__"（字符串）。
    所以 __name__ == "__main__" 结果为 True，下面的代码会被执行。
情况 B：这个文件被当作模块，被另一个文件 import 导入
    比如另一个文件写了 import game。
    此时 Python 会把 __name__ 的值设为该文件的名字 "game"。
    所以 __name__ == "__main__" 结果为 False，下面的代码不会执行。
"""

# 创建不同颜色的小鸟
red_bird = RedBirds()
yellow_bird = YellowBirds()
blue_bird = BlueBirds()

 # 创建障碍物
obstacle1 = Obstacle("木头堡垒", 100)
obstacle2 = Obstacle("石头塔楼", 200)

 # 红鸟攻击木头堡垒
obstacle1.be_attacked(red_bird)
 # 黄鸟攻击石头塔楼
obstacle2.be_attacked(yellow_bird)
 # 蓝鸟攻击石头塔楼
obstacle2.be_attacked(blue_bird)
