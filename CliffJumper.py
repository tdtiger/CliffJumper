import pyxel
import PyxelUniversalFont as puf
import random

# プレイヤーの定義部分
# ゲーム画面において左右，または上矢印の入力を受け付け，それぞれに対応した位置に移動する．
class Player:
    def __init__(self):
        self.pos = 0
        self.prepos = 0
        self.keyIn = None
        self.offsetX = 0
        self.offsetY = 0

    def Move(self, keyIn):
        if keyIn == "left":
            self.prepos = self.pos
            self.pos = max(-2, self.pos - 1)
        elif keyIn == "up":
            self.prepos = self.pos
        elif self.keyIn == "right":
            self.prepos = self.pos
            self.pos = min(self.pos + 1, 2)

    def Scroll(self):
        if self.offsetY > -38:
            self.offsetX += 1
            self.offsetY -= 2
        else:
            self.offsetX = 0
            self.offsetY = 0

    def draw(self):
        if self.pos == self.prepos:
            pyxel.blt(200 + self.pos * 40, 241 + self.offsetY, 0, 0, 0, 8, 8, 0)
        elif self.pos > self.prepos:
            pyxel.blt(200 + self.pos * 40 + self.offsetX, 241 + self.offsetY, 0, 8, 0, 8, 8, 0)
        elif self.pos < self.prepos:
            pyxel.blt(200 + self.pos * 40 - self.offsetX, 241 + self.offsetY, 0, 0, 8, 8, 8, 0)

        # if self.offsetY == 0:
        #     pyxel.blt(200 + self.pos * 40, 276, 0, 0, 0, 8, 8, 0)

# 足場の定義部分．
# 生成されるたびにランダムに位置が変化する．
# 現時点では生成される数は2つで固定にしているが，難易度ごとに変化するように変数を与える仕様にしても良いのかもしれない．
class Scaffold:
    def __init__(self):
        self.exs = random.sample([0, 1, 2, 3, 4], 3)

# アプリ本体の定義部分
# 基本的にはscreenという変数に現在のモードを格納し，それに応じた画面を描画する．
class App():
    def __init__(self):
        pyxel.init(400, 300, title = "Cliff Jumper")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.writer = puf.Writer("IPA_PGothic.ttf")
        self.screen = "title"
        self.volume = 50
        self.isScroll = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.screen == "title":
            self.UpdateTitle()
        elif self.screen == "game":
            self.UpdateGame()
        elif self.screen == "option":
            self.UpdateOption()

    def draw(self):
        pyxel.cls(1)
        # 各モード画面の描画
        if self.screen == "title":
            self.DrawTitle()
        elif self.screen == "game":
            self.DrawGame()
        elif self.screen == "option":
            self.DrawOption()

    def ResetGame(self):
        self.player = None
        self.scaffold = []
        self.player = Player()
        self.scaffold.append(Scaffold())


    # タイトル画面の描画
    def DrawTitle(self):
        self.writer.draw(120, 80, "Cliff Jumper", 30, 2)
        pyxel.rect(120, 145, 150, 30, 11)
        self.writer.draw(133, 150, "ゲームスタート", 20, 2)
        pyxel.rect(120, 185, 150, 30, 11)
        self.writer.draw(150, 190, "オプション", 20, 2)
        pyxel.rect(120, 225, 150, 30, 11)
        self.writer.draw(145, 230, "ゲーム終了", 20, 2)

    def UpdateTitle(self):
        if pyxel.btnp(pyxel.KEY_1) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 120 < pyxel.mouse_x < 270 and 145 < pyxel.mouse_y < 175):
            self.screen = "game"
            self.ResetGame()
            pyxel.mouse(False)
        elif pyxel.btnp(pyxel.KEY_2) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 120 < pyxel.mouse_x < 270 and 185 < pyxel.mouse_y < 215):
            self.screen = "option"
        elif pyxel.btnp(pyxel.KEY_Q) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 120 < pyxel.mouse_x < 270 and 225 < pyxel.mouse_y < 255):
            pyxel.quit()

    def UpdateOption(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.screen = "title"

        if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 210 < pyxel.mouse_x < 230 and 95 < pyxel.mouse_y <105) or pyxel.btnp(pyxel.KEY_LEFT):
            self.volume = max(0, self.volume - 1)
        elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 300 < pyxel.mouse_x < 320 and 95 < pyxel.mouse_y <105) or pyxel.btnp(pyxel.KEY_RIGHT):
            self.volume = min(self.volume + 1, 100)

    def DrawOption(self):
        self.writer.draw(70, 90, "音量", 20, 2)
        pyxel.tri(210, 100, 230, 95, 230, 105, 2)
        self.writer.draw(250, 90, str(self.volume), 20, 2)
        pyxel.tri(320, 100, 300, 95, 300, 105, 2)

        self.writer.draw(130, 130, "Q : タイトルに戻る", 20, 2)

    def UpdateGame(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.screen = "title"
            pyxel.mouse(True)
        elif not self.isScroll:
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.player.keyIn = "left"
                self.isScroll = True
            elif pyxel.btnp(pyxel.KEY_UP):
                self.player.keyIn = "up"
                self.isScroll = True
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.keyIn = "right"
                self.isScroll = True

        if self.isScroll:
            self.player.Scroll()
            if self.player.offsetY == 0:
                self.isScroll = False
                self.player.Move(self.player.keyIn)
                self.player.keyIn = None

    def DrawGame(self):
        for i in range(10):
            for j in range(7):
                pyxel.blt(92 + 32 * j, 0 + 32 * i, 0, 16 * (j % 2 + 1), 0, 32, 32)

        pyxel.blt(189, 235, 0, 80, 0, 32, 32)
        for i in self.scaffold[0].exs:
            pyxel.blt(109 + i * 40, 200, 0, 80, 0, 32, 32)

        self.player.draw()
        pyxel.text(5, 5, "score", 7)


App()