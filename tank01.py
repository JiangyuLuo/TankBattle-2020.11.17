'''
坦克大战的功能分析
1.项目中有哪些类
2.每个类中有哪些方法

1.坦克类（我方，敌方）
    射击
    移动
    显示坦克的方法
2.子弹类
    移动
    显示子弹的方法
3.墙壁类
    属性：是否可通过
4.爆炸效果类
    展示保证效果
5.音效类
    播放音乐
6.主类
    开始游戏
    结束游戏

添加事件
左上角文字绘制：输出敌方坦克的数量
边界碰撞
坦克优化：
敌方坦克的随机移动
子弹移动,碰到墙壁消失，最多三发
我方子弹与敌方坦克碰撞的
精灵类Sprite类
完善爆炸效果类
在窗口中展示爆炸效果
我方坦克无限重生用esc键
我方坦克与敌方坦克发生碰撞 让我方不能再继续移动 stay()
敌方坦克与我方发生碰撞 敌方不能再移动 stay()

'''
import pygame, random

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = 'white'


# 定义一个基类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)


class MainGame():
    window = None
    my_tank = None
    # 存储敌方坦克的列表
    enemyTankList = []
    # 定义坦克数量
    enemyTankCount = 5
    # 存储我方子弹列表
    myBulletList = []
    # 存储敌方子弹列表
    enemyBulletList = []
    # 存储爆炸效果
    explodeList = []
    # 存储墙壁列表
    wallList = []
    # 创建游戏时钟
    clock = pygame.time.Clock()

    def __init__(self):
        pass

    # 开始游戏
    def startGame(self):
        # 加载主窗口
        # 初始化窗口
        pygame.display.init()
        # 设置窗口大小
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置标题
        pygame.display.set_caption('坦克大战')
        # 初始化我方坦克，
        self.createMyTank()
        MainGame.my_tank = Tank(350, 250)
        # 初始化敌方坦克并将敌坦添加到列表中
        self.createEnemyTank()
        # 初始化墙壁
        self.createwall()

        while 1:

            # 给窗口填充颜色
            MainGame.window.fill(BG_COLOR)
            # 设置时钟
            MainGame.clock.tick(30)
            # 添加事件
            self.getEvent()

            # 绘制文字
            MainGame.window.blit(self.getTextSurface(f'敌方坦克剩余数量: %s' % (self.enemyTankCount)), [5, 5])

            # 判断我方坦克是否存活
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
            else:
                # 删除我方坦克
                del MainGame.my_tank
                MainGame.my_tank = None
            # 调用坦克显示的方法
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
            # 循环便利敌方坦克列表，展示敌方坦克
            self.blitEnemyTank()

            # 循环遍历我方坦克的子弹
            self.blitMyBullet()
            # 循环遍历敌方子弹列表
            self.blitEnemyBullet()
            # 循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            # 循环遍历墙壁列表，展示效果
            self.blitWall()
            # 调用移动方法 如果坦克的开关开启， 才可以移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与敌方坦克发生碰撞
                    # MainGame.my_tank.myTank_hit_enemyTank()
            pygame.display.update()

    # 初始化墙壁
    def createwall(self):
        for i in range(6):
            # 初始化墙壁
            wall = Wall(i * 130, 220)
            # 将墙壁添加到列表中
            MainGame.wallList.append(wall)

    # 创建我方坦克的方法
    def createMyTank(self):
        MainGame.my_tank = MyTank(350, 400)

    # 初始化敌方坦克并将敌坦添加到列表中
    def createEnemyTank(self):
        top = 25
        # 循环生成敌方坦克
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0, SCREEN_WIDTH - 60)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.enemyTankList.append(enemy)

    # 循环便利敌方坦克列表，展示敌方坦克
    # 修改敌方坦克的方向： 可以新增一个步数，当移动时候，步数进行递减，
    # 当步数<=0 时修改方向
    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            # 判断当前坦克是否活着
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randMove()
                # 发射子弹
                enemyBullet = enemyTank.shot()
                # 敌方子弹是否为none， 如果不是则添加到敌方子弹列表中
                if enemyBullet:
                    # 将敌方子弹存储刀敌方子弹列表中
                    MainGame.enemyBulletList.append(enemyBullet)
            else:
                # 删除
                MainGame.enemyTankList.remove(enemyTank)

    # 循环遍历我方子弹存储列表
    def blitMyBullet(self):
        for myBullet in MainGame.myBulletList:
            # 判断当前的子弹状态，如果是则进行显示移动，Vice versa
            if myBullet.live:
                myBullet.displayBullet()
                # 用子弹的移动方法
                myBullet.move()
                # 调用检测我方子弹和敌方坦克发生碰撞
                myBullet.myBullet_hit_enemyTank()
            # 否则在列表中删除
            else:
                MainGame.myBulletList.remove(myBullet)

    # 循环遍历敌方子弹存储列表 == blitMyBullet()
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletList:
            if enemyBullet.live:
                enemyBullet.displayBullet()
                enemyBullet.move()
                # 调用敌方子弹与我方坦克碰撞的方法
                enemyBullet.enemyBullet_hit_myTank()
            else:
                MainGame.enemyBulletList.remove(enemyBullet)

    # 循环展示爆炸效果
    def blitExplode(self):
        for explode in MainGame.explodeList:
            # 判断是否活着
            if explode.live:
                # 展示
                explode.displayExplode()
            else:
                # 在爆炸列表中移除
                MainGame.explodeList.remove(explode)

    # 循环展示墙壁
    def blitWall(self):
        for wall in MainGame.wallList:
            # 调用display方法
            wall.displayWall()

    # 结束游戏
    def endGame(self):

        print('Cheers')
        exit()

    # 左上角文字的绘制
    def getTextSurface(self, text):
        # 初始化字体模块
        pygame.font.init()
        # 查看所有字体
        # print(pygame.font.get_fonts())
        # 获取字体Font对象
        font = pygame.font.SysFont('kaiti', 18)
        # 绘制文本信息
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface

    # 获取事件
    def getEvent(self):
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                self.endGame()
            # 获取所有键盘事件
            k_p = pygame.key.get_pressed()
            # 根据当前方向重新设置图片的朝向

            # 如果键盘按下
            if event.type == pygame.KEYDOWN:
                # 当坦克不存在时
                if not MainGame.my_tank:
                    # 按下esc复活
                    if k_p[pygame.K_ESCAPE]:
                        # 调用创建我方坦克的方法
                        MainGame().createMyTank()
                if MainGame.my_tank and MainGame.my_tank.live:
                    if k_p[pygame.K_a]:
                        print('左')
                        # 切换方向
                        MainGame.my_tank.stop = False
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.move()
                    if k_p[pygame.K_d]:
                        print('右')
                        MainGame.my_tank.stop = False
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.move()
                    if k_p[pygame.K_w]:
                        print('上')
                        MainGame.my_tank.stop = False
                        MainGame.my_tank.direction = 'U'
                        MainGame.my_tank.move()
                    if k_p[pygame.K_s]:
                        print('下')
                        MainGame.my_tank.stop = False
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.move()
                    if k_p[pygame.K_SPACE]:
                        print('发射子弹')
                        # 创建我方坦克发射的子弹, 最多可以创建三颗
                        if len(MainGame.myBulletList) < 3:
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)

            # 松开方向键时停止
            if event.type == pygame.KEYUP:
                # 判断松开的键是方向键时才停止
                if MainGame.my_tank and MainGame.my_tank.live:
                    MainGame.my_tank.stop = True


class Tank(BaseItem):
    # 添加距离左边，距离上边
    def __init__(self, left, top):
        # 保存加载的图片
        self.images = {'U': pygame.image.load(r'D:\Python_files\images\p1tankU.gif'), \
                       'D': pygame.image.load(r'D:\Python_files\images\p1tankD.gif'), \
                       'L': pygame.image.load(r'D:\Python_files\images\p1tankL.gif'), \
                       'R': pygame.image.load(r'D:\Python_files\images\p1tankR.gif')}
        # 默认方向
        self.direction = 'U'
        # 根据当前图片的方向获取图片
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        # 设置区域left top
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = 3
        # 坦克移动开关
        self.stop = True
        # 是否活着
        self.live = True

    # 移动
    def move(self):
        # 判断坦克的方向
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if SCREEN_WIDTH - self.rect.width > self.rect.left:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if SCREEN_HEIGHT - self.rect.height > self.rect.top:
                self.rect.top += self.speed

    # 射击
    def shot(self):
        return Bullet(self)

    # 展示坦克的方法
    def displayTank(self):
        # 获取展示的对象
        self.image = self.images[self.direction]
        # 调用blit方法
        MainGame.window.blit(self.image, self.rect)

    def myTank_hit_enemyTank(self):
        # 循环遍历敌方坦克列表
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemyTank):
                self.stay()


# 我方坦克
class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)

    # 检测我方坦克与敌方坦克发生碰撞
    def myTank_hit_enemyTank(self):
        # 循环遍历敌方坦克列表
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemyTank):
                self.stay()

# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # 调用父类的初始化方法
        super().__init__(left, top)
        # 加载图片集
        self.images = {
            'U': pygame.image.load(r'D:\Python_files\images\enemy1U.gif'), \
            'D': pygame.image.load(r'D:\Python_files\images\enemy1D.gif'), \
            'L': pygame.image.load(r'D:\Python_files\images\enemy1L.gif'), \
            'R': pygame.image.load(r'D:\Python_files\images\enemy1R.gif')
        }
        # 方向, 随机生成敌方坦克的方向
        self.direction = self.randDirection()
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left和top赋值
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = speed
        # 新增一个步数变量step
        self.step = 20

    # 随机生成坦克方向
    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'R'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'D'

    # 敌方坦克随即移动的方法
    def randMove(self):
        if self.step <= 0:
            # 修改方向
            self.direction = self.randDirection()
            self.step = 120
        else:
            self.move()
            self.step -= 1

    # 重写shot()方法
    def shot(self):
        # 随机生成100以内的数
        num = random.randint(1, 100)
        if num < 10:
            return Bullet(self)


# 子弹类
class Bullet(BaseItem):

    def __init__(self, tank):
        # 加载图片
        self.image = pygame.image.load(r'D:\Python_files\images\enemymissile.gif')
        # 坦克方向决定子弹方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 子弹的left和top也方向有关
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2

        # 子弹的速度
        self.speed = 10

        # 子弹状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live = True

    # 移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 修改子弹状态
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                # 修改子弹状态
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                # 修改子弹状态
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改子弹状态
                self.live = False

    # 展示子弹的方法
    def displayBullet(self):
        # 将图片surface加载到窗口
        MainGame.window.blit(self.image, self.rect)

    # 我方子弹与敌方坦克的碰撞
    def myBullet_hit_enemyTank(self):
        # 循环遍历敌方坦克列表，判断是否发生碰撞
        for enemy in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemy):
                # 修改敌方坦克和我方子弹的状态
                enemy.live = False
                self.live = False
                # 创建爆炸对象， 将爆炸对象添加到爆炸列表中
                explode = Explode(enemy)
                MainGame.explodeList.append(explode)

    # 敌方子弹与我方坦克碰撞
    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(self, MainGame.my_tank):
                # 产生爆炸对象
                # 修改我方坦克和敌方子弹的状态
                MainGame.my_tank.live = False
                self.live = False
                # 创建爆炸对象， 将爆炸对象添加到爆炸列表中
                explode = Explode(MainGame.my_tank)
                MainGame.explodeList.append(explode)


# 墙壁类
class Wall():
    def __init__(self, left, top):
        # 加载图片
        self.image = pygame.image.load(r'D:\Python_files\images\walls.gif')
        # 获取墙壁区域
        self.rect = self.image.get_rect()
        # 设置位置left和 top
        self.rect.left = left
        self.rect.top = top
        # 是否活着
        self.live = True
        # 设置生命值
        self.hp = 3

    # 展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)


# 爆炸类
class Explode():
    def __init__(self, tank):
        # 由当前子弹打中的坦克位置决定爆炸位置
        self.rect = tank.rect
        self.images = [pygame.image.load(r'D:\Python_files\images\blast0.gif'),
                       pygame.image.load(r'D:\Python_files\images\blast1.gif'),
                       pygame.image.load(r'D:\Python_files\images\blast2.gif'),
                       pygame.image.load(r'D:\Python_files\images\blast3.gif'),
                       pygame.image.load(r'D:\Python_files\images\blast4.gif'),
                       pygame.image.load(r'D:\Python_files\images\blast5.gif'),
                       pygame.image.load(r'D:\Python_files\images\blast6.gif')]
        self.step = 0
        self.image = self.images[self.step]
        # 是否活着
        self.live = True

    # 展示爆炸的方法
    def displayExplode(self):
        if self.step < len(self.images):
            # 根据索引获取爆炸对象
            self.image = self.images[self.step]
            self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, self.rect)
        else:
            # 修改状态
            self.live = False
            self.step = 0


# 音效类
class Music():
    def __init__(self):
        pass

    # 播放音乐的方法
    def play(self):
        pass


if __name__ == '__main__':
    MainGame().startGame()
