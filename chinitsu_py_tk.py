import sys
sys.dont_write_bytecode = True  # do not make '__cache__'
import random
import tkinter as tk
from tkinter import messagebox as msg
import os
import my_icon  # アイコン
# import mahjong
#計算
from mahjong.hand_calculating.hand import HandCalculator
#麻雀牌
from mahjong.tile import TilesConverter
#役, オプションルール
# from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.hand_config import HandConfig
# #鳴き
# from mahjong.meld import Meld
# #風(場&自)
# from mahjong.constants import EAST, SOUTH, WEST, NORTH


# m_mylist=tuple(i for i in range(0,36,1))
# m_agari_kouho=tuple(i for i in range(3,36,4))

# p_mylist=tuple(i for i in range(36,72,1))
# p_agari_kouho=tuple(i for i in range(39,72,4))

s_mylist=tuple(i for i in range(72,108,1))
s_easy_mylist=tuple(i for i in range(72,88,1))
s_agari_kouho=tuple(i for i in range(75,108,4))
count =[0,0,0,0,0,0,0,0,0]

mylist=s_mylist
agari_kouho=s_agari_kouho
agari_tiles=[0,0,0,0,0,0,0,0,0]

newlist=[]

def draw(mylist,n):
    global newlist
    newlist = random.sample(mylist, n)
    # return newlist

def b_click(btn,x):
    count[x] ^= 1
    if count[x] == 0:
        btn.config(bg="lightyellow")
    else:
        btn.config(bg="#00c000")

def reprint(gamen,lis2):
    global newlist
    # print(f"Reprint={len(newlist)}")
    for i in range(13):
        i_temp = int((newlist[i]-72)/4)
        # print(i_temp+1,end=" ")
        canvas = tk.Canvas(gamen,width=88,height=128)
        canvas.place(x=0+95*i, y=5)
        canvas.create_image(0,0,image=lis2[i_temp],anchor=tk.NW)
    # print("")

def hai_order(gamen,lis2):
    global newlist
    print("-"*20)
    print(newlist)
    newlist.sort()
    print(newlist)
    reprint(gamen,lis2)

def c_hai_order(event,gamen,lis2):
    global newlist
    hai_order(gamen,lis2)

def hai_shuffle(gamen,lis2):
    global newlist
    print("-"*20)
    print(newlist)
    random.shuffle(newlist)
    print(newlist)
    reprint(gamen,lis2)

def c_hai_shuffle(event,gamen,lis2):
    global newlist
    hai_shuffle(gamen,lis2)

def make_btn(gamen):
    column = -1
    row = 0
    for i in range(0,9):
        if i >= 0:
            if i%9 == 1:
                row += 1 
                column = -1
            column += 1
            text=f'{i+1}'
            btn = tk.Button(gamen,text=text,font=32,bg="lightyellow")
            btn.grid(column=column, row=row)
            # btn.config(command=collback(btn))
            btn.config(command=lambda a=btn,b=i: b_click(a,b))
            btn.place(x=90*i,y=150,width=88,height=128)


def draw_new(gamen,lis2,lis3,num1):
    global newlist , count
    count=[0,0,0,0,0,0,0,0,0]
    make_btn(gamen)
    print("-"*20)
    if num1==0:
        draw(lis3,1)
        lis_tnsp = [ 121,122,123,  125,126,127, 129,130,131, 133,134,135 ] # ton,nan,sha,pei
        newlist = newlist + lis_tnsp
    elif num1==1:
        draw(lis3,4)
        lis_hhc = [ 109,110,111,  113,114,115, 117,118,119 ] # haku,hatsu,chun
        newlist = newlist + lis_hhc
    else:
        draw(lis3,13)
    if num1<=2:
        print(newlist)
        newlist.sort()
    print(newlist)
    make_btn(gamen)
    reprint(gamen,lis2)

def c_draw_new(event,gamen,lis2,lis3,num1,text1):
    draw_new(gamen,lis2,lis3,num1)
    text1.delete( 0. , tk.END )
    strtxt = "アガリ牌をクリックして緑にした後、決定を押して下さい。\n※アガリが存在しない場合は、何も選択しないこと"
    text1.insert(tk.END, strtxt )

def agari():
    global agari_tiles
    #HandCalculator(計算用クラス)のインスタンスを生成
    calculator = HandCalculator()
    melds = None
    dora_indicators = [TilesConverter.string_to_136_array(man='1')[0],]
    config = HandConfig(is_tsumo=True,is_riichi=None,is_daburu_riichi=None,is_ippatsu=None,)
    tiles=[]
    agari_tiles=[0,0,0,0,0,0,0,0,0]
    yakitori=0
    for x in range(72,108,4):  # ALL souzu check  1s=72,(73,74,75)  2s=76,(77,78....
        for y in range(0,4,1): #
            win_tile=x+y
            tumohai = [win_tile]
            if ( win_tile not in newlist ):
                tiles = newlist + tumohai
            result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
            if  ( win_tile not in newlist ) & (type(result.han)==int) & (type(result.fu)==int ):
                print("win_tile=",win_tile," RON!")
                yakitori=1
                temp=int((win_tile-72)/4)
                agari_tiles[temp]=1
                # print(h_list[temp])
                break
    # print("            1  2  3  4  5  6  7  8  9")
    # print("agari_tiles=",agari_tiles)
    if(yakitori==0):
        print("No_AGARI_HAI")
    return(agari_tiles)

def c_agari(event,text1):
    agari()
    print(f"AGARI_HAI={agari_tiles}")
    print(f"Hands_HAI={count}")
    if agari_tiles==count:
        print(f"Correct")
        text1.delete( 0. , tk.END )
        strtxt = "正解です！"
        text1.insert(tk.END, strtxt )

    else:
        print(f"Wrong")
        text1.delete( 0. , tk.END )
        strtxt = "間違いです"
        text1.insert(tk.END, strtxt )

def main(p_dir):
    pwdcwd=os.getcwd()

    root=tk.Tk()
    photo = my_icon.get_photo_image4icon()  # PhotoImageオブジェクトの作成
    root.iconphoto(False, photo)           # アイコンの設定
    version = tk.Tcl().eval('info patchlevel')
    root.configure(bg="lightgray")
    ttext = "MJ" + "_" + version + pwdcwd
    root.title(ttext)
    gx,gy=1250,400
    root.minsize(gx,gy)

    # tiles=[]
    # agari_tiles   = [0,0,0,0,0, 0,0,0,0]

    draw(mylist, 13)
    print(newlist)

    img_s1    = tk.PhotoImage(file=f"{p_dir}/souzu1.png",width=88,height=128)
    img_s2    = tk.PhotoImage(file=f"{p_dir}/souzu2.png",width=88,height=128)
    img_s3    = tk.PhotoImage(file=f"{p_dir}/souzu3.png",width=88,height=128)
    img_s4    = tk.PhotoImage(file=f"{p_dir}/souzu4.png",width=88,height=128)
    img_s5    = tk.PhotoImage(file=f"{p_dir}/souzu5.png",width=88,height=128)
    img_s6    = tk.PhotoImage(file=f"{p_dir}/souzu6.png",width=88,height=128)
    img_s7    = tk.PhotoImage(file=f"{p_dir}/souzu7.png",width=88,height=128)
    img_s8    = tk.PhotoImage(file=f"{p_dir}/souzu8.png",width=88,height=128)
    img_s9    = tk.PhotoImage(file=f"{p_dir}/souzu9.png",width=88,height=128)
    img_haku  = tk.PhotoImage(file=f"{p_dir}/haku.png",width=88,height=128)
    img_hatsu = tk.PhotoImage(file=f"{p_dir}/hatsu.png",width=88,height=128)
    img_chun  = tk.PhotoImage(file=f"{p_dir}/chun.png",width=88,height=128)
    img_ton   = tk.PhotoImage(file=f"{p_dir}/ton.png",width=88,height=128)
    img_nan   = tk.PhotoImage(file=f"{p_dir}/nan.png",width=88,height=128)
    img_sha   = tk.PhotoImage(file=f"{p_dir}/sha.png",width=88,height=128)
    img_pei   = tk.PhotoImage(file=f"{p_dir}/pei.png",width=88,height=128)
    images=(img_s1,img_s2,img_s3,img_s4,img_s5,img_s6,img_s7,img_s8,img_s9,img_haku,img_hatsu,img_chun,img_ton,img_nan,img_sha,img_pei)

    hai_order(root,images)
    make_btn(root)

    button1=tk.Button(root,text="決定!!",bg="orange")
    button1.bind("<1>", lambda event:c_agari(event,text1) )
    button1.place(x=850,y=150,width=88,height=128)

    button2=tk.Button(root,text="理牌\n\n(整列する)",bg="lightcyan")
    button2.bind("<1>", lambda event:c_hai_order(event,root,images) )
    button2.place(x=950,y=150,width=88,height=60)

    button3=tk.Button(root,text="洗牌\n\n(ｼｬｯﾌﾙする)",bg="pink")
    button3.bind("<1>", lambda event:c_hai_shuffle(event,root,images) )
    button3.place(x=950,y=220,width=88,height=60)

    Label1=tk.Label(root,text="レベル選択(NewGame)",bg="lightgray")
    Label1.place(x=750,y=300,width=200,height=16)

    button4=tk.Button(root,text="超簡単\n\n大四喜確定",bg="lightgreen")
    button4.bind("<1>", lambda event:c_draw_new(event,root,images,s_mylist,0,text1) )
    button4.place(x=750,y=320,width=88,height=64)

    button4=tk.Button(root,text="簡単\n\n大三元確定",bg="lightgreen")
    button4.bind("<1>", lambda event:c_draw_new(event,root,images,s_easy_mylist,1,text1) )
    button4.place(x=850,y=320,width=88,height=64)

    button5=tk.Button(root,text="普通\n\n理牌済",bg="lightyellow")
    button5.bind("<1>", lambda event:c_draw_new(event,root,images,s_mylist,2,text1) )
    button5.place(x=950,y=320,width=88,height=64)

    button6=tk.Button(root,text="困難\n\n",bg="pink")
    button6.bind("<1>", lambda event:c_draw_new(event,root,images,s_mylist,3,text1) )
    button6.place(x=1050,y=320,width=88,height=64)

    text1=tk.Text(root,bg="white")
    text1.delete( 0. , tk.END )
    strtxt = "アガリ牌をクリックして緑にした後、決定を押して下さい。\n※アガリが存在しない場合は、何も選択しないこと"
    text1.insert(tk.END, strtxt )
    text1.place(x=10,y=300,width=600,height=60)

    root.mainloop()

if __name__ == "__main__":
    # print(__file__)
    print('basename:    ', os.path.basename(__file__) )
    print('dirname:     ', os.path.dirname(__file__) )
    print('cwdname:     ', os.getcwd() )

    p_file = 'chinitsu/image/souzu1.png'
    p_dir  = 'chinitsu/image/'

    if os.path.isdir(p_dir):
        pass
    else:
        print(f"{p_dir}が見つかりません。")
        p_file = 'image/souzu1.png'
        p_dir  = 'image/'
        if os.path.isdir(p_dir):
            pass
        else:
            print(f"{p_dir}が見つかりません。")
            msg.showwarning('メッセージ', f"{p_dir}が見つかりません。")    #「警告」のメッセージボックス
            sys.exit()

    if os.path.isfile(p_file):
        pass
    else:
        print(f"{p_file}が見つかりません。")
        p_file = 'image/souzu1.png'
        if os.path.isdir(p_file):
            pass
        else:
            print(f"{p_file}が見つかりません。")
            msg.showwarning('メッセージ', f"{p_file}が見つかりません。")    #「警告」のメッセージボックス
            sys.exit()

    main(p_dir)