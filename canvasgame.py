from tkinter import *
from tkinter import messagebox
import threading
import random
from tkinter import ttk
GAME_WIDTH = 500
GAME_HEIGHT = 580
BOARD_X = 230
BOARD_Y = 500
BOARD_WIDTH = 80
BALL_RADIUS = 9
THREAD_ID = 0
class canvasgame:
    def __init__(self, master):
        self.master = master
        # 记录小球动画的第几帧
        self.ball_index = 0
        # 记录游戏是否失败的旗标
        self.is_lose = False
        # 初始化记录小球位置的变量
        self.curx = 260
        self.cury = 30
        self.boardx = BOARD_X
        self.init_widgets()
        self.vx = random.randint(3, 6)  # x方向的速度
        self.vy = random.randint(5, 10)  # y方向的速度

        #3次机会
        self.lives = 3
        self.lives_text = None
        # 初始化生命值
        self.update_lives_text()

        self.text = None
        self.update_text('')

    # 创建界面组件
    def init_widgets(self):
        self.cv = Canvas(self.master, background='white',
            width=GAME_WIDTH, height=GAME_HEIGHT)
        self.cv.pack()
        # 让画布得到焦点，从而可以响应按键事件
        self.cv.focus_set()
        self.cv.bms = []
        # 初始化小球的动画帧
        for i in range(3):
            self.cv.bms.append(PhotoImage(file='images/ball_' + str(i+1) + '.png'))
        # 绘制小球
        self.ball = self.cv.create_image(self.curx, self.cury,
            image=self.cv.bms[self.ball_index])
        self.board = self.cv.create_rectangle(BOARD_X, BOARD_Y,
            BOARD_X + BOARD_WIDTH, BOARD_Y + 20, width=0, fill='lightblue')
        # 为向左箭头按键绑定事件，挡板左移
        self.cv.bind('<KeyPress-Left>', self.move_left)
        # 为向右箭头按键绑定事件，挡板右移
        self.cv.bind('<KeyPress-Right>', self.move_right)

        ttk.Button(self.master, text='开始游戏', command=self.start_game).pack()

    def move_left(self, event):
        if self.boardx <= 0:
            return
        self.boardx -= 5
        self.cv.coords(self.board, self.boardx, BOARD_Y,
            self.boardx + BOARD_WIDTH, BOARD_Y + 20)
        print("move_left:"+str(self.boardx))
    def move_right(self, event):
        if self.boardx + BOARD_WIDTH >= GAME_WIDTH:
            return
        self.boardx += 5
        self.cv.coords(self.board, self.boardx, BOARD_Y,
            self.boardx + BOARD_WIDTH, BOARD_Y + 20)
        print("move_right:" + str(self.boardx))
    def moveball(self):
        if not doTick:
            return
        self.curx += self.vx
        self.cury += self.vy
        # 小球到了右边墙壁，转向
        if self.curx + BALL_RADIUS >= GAME_WIDTH:
            self.vx = -self.vx
        # 小球到了左边墙壁，转向
        if self.curx - BALL_RADIUS <= 0:
            self.vx = -self.vx
        # 小球到了上边墙壁，转向
        if self.cury - BALL_RADIUS <= 0:
            self.vy = -self.vy
        # 小球到了挡板处
        if self.cury + BALL_RADIUS >= BOARD_Y:
            # 如果在挡板范围内
            if self.boardx <= self.curx <= (self.boardx + BOARD_WIDTH):
                self.vy = -self.vy
            else:
                # 如果在挡板范围，则将 lives 减 1，否则绘制弹球，再次进行游戏循环
                self.lives -= 1
                # 如果 lives 小于 1，游戏结束，否则调整 scores，重新预置游戏
                if self.lives < 1:
                    self.update_lives_text();
                    self.update_text('游戏结束');
                    self.is_lose = True
                    return
                else:
                    self.reset_ball()
                    return

        self.cv.coords(self.ball, self.curx, self.cury)
        self.ball_index += 1
        self.cv.itemconfig(self.ball, image=self.cv.bms[self.ball_index % 3])
        # 如果游戏还未失败，让定时器继续执行
        if not self.is_lose:
            # 通过定时器指定0.1秒之后执行moveball函数
            self.t = threading.Timer(0.1, self.moveball)
            self.t.start()

    # 开始游戏
    def start_game(self):
        '''
        # 依次解除绑定、重设得分、删除提示文本、开始游戏循环
        self.canvas.unbind('<Button-1>')
        self.reset_score()
        self.canvas.delete(self.text)
        self.game_loop()
        '''
        # 记录游戏是否失败的旗标
        self.is_lose = False

        self.lives = 3
        self.update_lives_text()
        self.update_text('')

        #重置定时器
        global doTick
        doTick = False

        # 通过定时器指定0.2秒之后执行moveball函数
        self.t = threading.Timer(0.2, self.reset_ball)
        self.t.start()

        # 将键盘焦点转移到画布组件上
        self.cv.focus_set()

    #重置ball
    def reset_ball(self):
        # 初始化记录小球位置的变量
        self.curx = 260
        self.cury = 30

        self.update_lives_text()
        global doTick
        doTick = True
        self.moveball()


    # 更新生命的数字
    def update_lives_text(self):
        text = '生命: %s' % self.lives
        if self.lives_text is None:
            self.lives_text = self.cv.create_text(60, 30, text=text, font=('Helvetica', 16), fill='green')
        else:
            self.cv.itemconfig(self.lives_text, text=text)

    # 更新提示信息
    def update_text(self,text):
        if self.text is None:
            self.text = self.cv.create_text(220, 200, text=text, font=('Helvetica', 36), fill='red')
        else:
            self.cv.itemconfig(self.text, text=text)