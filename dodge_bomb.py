import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT:(+5,0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def game_over(screen: pg.Surface) -> None:

    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表
    示し，泣いているこうかとん画像を貼り付ける関数
    """
    back_screen = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(back_screen,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    back_screen.set_alpha(128)

    fonto = pg.font.Font(None,80)
    txt = fonto.render("Game Over",True,(255,255,255))
    screen.blit(txt,[400,300])
    kk8_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,1)
    kk8_rct1 = kk8_img.get_rect(center = (WIDTH//2-200,HEIGHT//2))
    kk8_rct2 = kk8_img.get_rect(center = (WIDTH//2+200,HEIGHT//2))
    screen.blit(back_screen,[0,0])
    screen.blit(kk8_img,kk8_rct1)
    screen.blit(kk8_img,kk8_rct2)
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) # 爆弾用空のSurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) # 爆弾円を描く
    bb_img.set_colorkey((0,0,0)) # 四隅の黒を透過させる
    bb_rct = bb_img.get_rect() # 爆弾Rectの抽出
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = +5,+5 # 爆弾の速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            game_over(screen)
            return # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        #　こうかとんが画面外なら元の場所に戻す
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy) # 爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 横にはみ出てる
            vx *= -1
        if not tate: #　縦にはみ出てる
            vy *= -1 
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
