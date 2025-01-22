import sys
sys.dont_write_bytecode = True  # do not make '__cache__'
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmsg
import os
pwdcwd=os.getcwd()
import my_icon  # アイコン
# import mahjong
#計算#麻雀牌
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
import time
import mido 
from mido import Message, MidiFile, MidiTrack, MetaMessage
# from mido import Message
import threading
import ctypes
import datetime
# import functools
import glob
# import re
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

ipausesec = 0
f_name="dummy"

def dummy():
    pass
def eummy(event):
    pass
def getTime():
    return datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
def printTime(string):
    print(f"{getTime()}: {string}")
def killThemAll():
    for thread in threading.enumerate():
        if thread != threading.main_thread():
            printTime(f"kill: {thread.name}")
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.native_id, ctypes.py_object(SystemExit))
def play_sound():
    global ipausesec, f_name
    msg = Message('note_on', note=60)
    # print(msg)
    # print(dir(msg))
    # print(f"start={datetime.datetime.today()}")
    ports = mido.get_output_names()
    with mido.open_output(ports[0]) as outport:
        # f_name = os.path.dirname(__file__) + "\\data\\" + 'ff3lstbt.mid'
        f_name = combobox1.get()
        # f_name = r'C:\Users\19NECK011\pyworks\chinitsu\data\ff3lstbt.mid'
        
        end = 0
        if ipausesec>0:
            end=ipausesec
            ipausesec=0
        for msg in mido.MidiFile(f_name):
            if ipausesec >= end:
                time.sleep(msg.time) # sound output(normal)
            if not msg.is_meta:
                outport.send(msg) # sound output
                # print(outport, msg)
                # print(f"ip={ipausesec} end={end}")
                ipausesec += 1

class NeoButton_START(tk.Button): # START
    global thread , lis_thread
    def __init__(self):
        super().__init__(master=None,text="音楽再生\n▶ ",command=self.Button_click)
    def Button_click(self):
        text_message.set("演奏中です。")
        thread = threading.Thread(target=music_play,daemon=True)
        lis_thread.append(thread)
        thread.start()
        print(thread)
        # tkmsg.showwarning('メッセージ', f"デバッグつまらないよ。。。")

    def place_forget(self):
        return super().place_forget()
    def place_configure(self,width = ..., height = ..., x = ..., y = ...):
        return super().place_configure(width=width, height=height, x=x, y=y)

class NeoButton_WAIT(tk.Button): # WAIT # 未実装
    def __init__(self):
        super().__init__(master=None,text="一時停止\n⏸︎",command=self.Button_click)
    def Button_click(self):
        killThemAll()
        pass
    def place_forget(self):
        return super().place_forget()
    def place_configure(self,width = ..., height = ..., x = ..., y = ...):
        return super().place_configure(width=width, height=height, x=x, y=y)

class NeoButton_STOP(tk.Button): # STOP
    def __init__(self):
        super().__init__(master=None,text="音楽停止\n■",command=self.Button_click)
    def Button_click(self):
        killThemAll()
        clear_play()
    def place_forget(self):
        return super().place_forget()
    def place_configure(self,width = ..., height = ..., x = ..., y = ...):
        return super().place_configure(width=width, height=height, x=x, y=y)

def music_play():
    Button_act1["state"] = tk.DISABLED
    try:
        # time.sleep(20) # 重い処理
        play_sound()
    except Exception as Exc:
        str1 = f"音楽再生ワーニングです({Exc})"
        print(str1)
        # tkmsg.showwarning("warning", str1)
        pass
    else:
        # tkmsg.showinfo("message", "正常終了です")
        print("音楽再生  正常終了です")
        pass
    finally:
        text_message.set("待機中\n(midﾌｧｲﾙのみ対応)")
        Button_act1["state"] = tk.NORMAL

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
        canvas.create_image(0,0,image=lis2[i_temp],anchor=tk.NW)
        canvas.place(x=0+95*i, y=5)
        lis_can.append(canvas)
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
            btn.place(x=94*i+5,y=150,width=88,height=128)
            lis_btn.append(btn)

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

def c_draw_new(event,gamen,lis2,lis3,num1,text1,text_d):
    game()
    
    draw_new(gamen,lis2,lis3,num1)
    text1.delete( 0. , tk.END )
    strtxt = "アガリ牌をクリックして緑にした後、決定を押して下さい。\n※アガリが存在しない場合は、何も選択しないこと"
    text1.insert(tk.END, strtxt )

    text_d.delete( 0. , tk.END )
    strtxt = "みんなには  ナイショだよ"
    text_d.insert(tk.END, strtxt )

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

def c_agari(event,text1,text_d):
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
        strtxt  = "間違いです\n\n"
        strtxt += "↓ 答えは下に隠れてます"
        text1.insert(tk.END, strtxt )

    text_d.delete( 0. , tk.END )
    strtxt  = f"正解は、、、、\n"
    strtxt += f"            1  2  3  4  5  6  7  8  9\n"
    strtxt += f" AGARI_HAI={agari_tiles}"
    strtxt += f" <- '1' だけをクリックして緑にすれば正解です\n"
    strtxt += f" SELECTED ={count}"
    text_d.insert(tk.END, strtxt )

    # frame2.place(x=645,y=307,width=400,height=85)
    # Label1.place(x=750,y=300,width=130,height=16)
    # button4.place(x=650,y=320,width=88,height=64)
    # button5.place(x=750,y=320,width=88,height=64)
    # button6.place(x=850,y=320,width=88,height=64)
    # button7.place(x=950,y=320,width=88,height=64)
    button_menu.place(x=1050,y=150,width=176,height=128)

def forget_item():
    for val in lis_btn:
        val.place_forget()
    for val in lis_can:
        val.place_forget()

def menu():
    text_d.delete( 0. , tk.END )
    strtxt = "みんなには  ナイショだよ"
    text_d.insert(tk.END, strtxt )

    text1.delete( 0. , tk.END )
    strtxt = "アガリ牌の数字をクリックして緑にした後、決定を押して下さい。\n※アガリが存在しない場合は、何も選択しないこと"
    text1.insert(tk.END, strtxt )

    forget_item()
    # frame2.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    # Label1.place_forget()
    # button4.place_forget()
    # button5.place_forget()
    # button6.place_forget()
    # button7.place_forget()
    text1.place_forget()
    # button_game.place(x=10,y=160,width=400,height=100)
    button_menu.place_forget()
    Label_doc1.place(x=10,y=10,width=1000,height=50)
    Label_doc2.place(x=10,y=65,width=600,height=300)
    Label_doc3.place(x=1050,y=50,width=200,height=100)
    label_info.place(x=1075,y=300,width=160,height=50)
    root.mainloop()

def c_menu(event):
    menu()

def game():
    # button_game.place_forget()
    Label_doc1.place_forget()
    Label_doc2.place_forget()
    Label_doc3.place_forget()
    button_menu.place_forget()

    draw(mylist, 13)
    print(newlist)

    hai_order(root,images)
    make_btn(root)

    button1.place(x=855,y=150,width=88,height=128)
    button2.place(x=950,y=150,width=88,height=60)
    button3.place(x=950,y=220,width=88,height=60)
    text1.place(x=10,y=300,width=450,height=60)
    Label_d.place(x=10,y=500,width=200,height=16)
    text_d.place(x=10,y=520,width=800,height=80)

    # root.mainloop() # menu?

def c_game(event):
    game()

def print_list(event):
    print(f"can={lis_can}")
    print(f"btn={lis_btn}")

def dprint(event):
    x = threading.current_thread().name
    y = threading.active_count()
    z = threading.Event()
    print("-"*30)
    str1=f"p_dir={p_dir}"
    print(str1)
    str2=f"{x}\n{y}\n{z}\n{ipausesec}"
    print(str2)
    text_d.delete( 0. , tk.END )
    strtxt = f"p_dir={p_dir}\n{str2}"
    text_d.insert(tk.END, strtxt )
    pass

def clear_play():
    global ipausesec, f_name
    ipausesec = 0
    f_name = combobox1.get()

def update_values():
    global options , ipausesec, p_dir, f_name
    ipausesec = 0
    options = glob.glob(p_dir+"\\*.mid")
    combobox1['values'] = options
    if len(options)==0:
        Button_act1["state"] = tk.DISABLED
    else:
        combobox1.set(options[0])
        Button_act1["state"] = tk.NORMAL
        f_name = combobox1.get()

def on_select():
    global options , ipausesec , f_name
    ipausesec = 0
    f_name = combobox1.get()

global p_dir
# print(__file__)
# print('basename:    ', os.path.basename(__file__) )
# print('dirname:     ', os.path.dirname(__file__) )
# print('cwdname:     ', os.getcwd() )

p_dir  = 'chinitsu\\data\\'
p_file = 'chinitsu\\data\\souzu1.png'
if os.path.isdir(p_dir) and os.path.isfile(p_file):
    print("DIR_FILE_OK1_DEBUG")
    pass
else:
    p_dir  = os.path.dirname(__file__) + '\\data\\'
    p_file = os.path.dirname(__file__) + '\\data\\souzu1.png'
    if os.path.isdir(p_dir) and os.path.isfile(p_file):
        print("DIR_FILE_OK2")
        pass
    else:
        p_dir  = pwdcwd + '\\data\\'
        p_file = pwdcwd + '\\data\\souzu1.png'
        if os.path.isdir(p_dir) and os.path.isfile(p_file):
            print("DIR_FILE_OK3")
            pass
        else:
            p_dir  = '\\data\\'
            p_file = '\\data\\souzu1.png'
            if os.path.isdir(p_dir) and os.path.isfile(p_file):
                print("DIR_FILE_OK3")
                pass
            else:
                tkmsg.showwarning('メッセージ', f"{p_dir}が見つかりません。。。")    #「警告」のメッセージボックス
                sys.exit()

root=tk.Tk()
photo = my_icon.get_photo_image4icon()  # PhotoImageオブジェクトの作成
root.iconphoto(False, photo)           # アイコンの設定
version = tk.Tcl().eval('info patchlevel')
root.configure(bg="lightgray")
ttext = "麻雀 清一色 練習"
root.title(ttext)
gx,gy=1250,400
root.minsize(gx,gy)

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

lis_can=[]
lis_btn=[]
lis_thread=[]

Label_doc1=tk.Label(root,font=("MSゴシック", "40", "bold"),text='麻雀 清一色 練習',bg="lightgray")
Label_doc1.place(x=10,y=10,width=1000,height=50)

Label_doc2=tk.Label(root,justify=tk.LEFT,font=("MSゴシック", "15" ),bg="lightgray",text='''
・麻雀における清一色（染手）を練習するためのソフトです。
・難易度のボタンを選択するとゲーム開始です。
  アガリ牌だと思う数字をすべての選択肢し、
  パネルを緑にした後に『決定』を押して下さい。
・以下のボタンは必要に応じて押して下さい。
    『理牌』：牌を種類・数字順に整列させる。（難易度ダウン）
    『洗牌』：牌をランダムに整列させる。（難易度アップ）

・音楽ファイル(mid)を再生可能です。
  ファイルを『data』フォルダに格納し、
  コンボボックスから選択後に
  再生ボタンを押して下さい。
''')
Label_doc2.place(x=10,y=65,width=600,height=400)

Label_doc3=tk.Label(root,justify=tk.LEFT,font=("MSゴシック", "10" ),bg="lightgray",text='''
●素材の利用
・MIDI音楽データ
「龍的交響楽」様
URL：http://d-symphony.com/
''')
Label_doc3.place(x=1050,y=50,width=200,height=100)

button1=tk.Button(root,text="決定!!",bg="orange")
button1.bind("<1>", lambda event:c_agari(event,text1,text_d) )
# button1.place(x=850,y=150,width=88,height=128)

button2=tk.Button(root,text="理牌\n\n(整列する)",bg="lightcyan")
button2.bind("<1>", lambda event:c_hai_order(event,root,images) )
# button2.place(x=950,y=150,width=88,height=60)

button3=tk.Button(root,text="洗牌\n\n(ｼｬｯﾌﾙする)",bg="pink")
button3.bind("<1>", lambda event:c_hai_shuffle(event,root,images) )
# button3.place(x=950,y=220,width=88,height=60)

frame2 = tk.Frame(root, bg="lightgray", bd=1, relief='solid' )
frame2.place(x=495,y=295,width=400,height=100)

Label1=tk.Label(root,text="レベル選択(NewGame)",bg="lightgray")
Label1.place(x=550,y=300,width=130,height=16)

button4=tk.Button(root,text="超簡単\n\n大四喜確定",bg="lightgreen")
button4.bind("<1>", lambda event:c_draw_new(event,root,images,s_mylist,0,text1,text_d) )
button4.place(x=500,y=320,width=88,height=64)

button5=tk.Button(root,text="簡単\n\n大三元確定",bg="lightgreen")
button5.bind("<1>", lambda event:c_draw_new(event,root,images,s_easy_mylist,1,text1,text_d) )
button5.place(x=600,y=320,width=88,height=64)

button6=tk.Button(root,text="普通\n\n理牌済",bg="lightyellow")
button6.bind("<1>", lambda event:c_draw_new(event,root,images,s_mylist,2,text1,text_d) )
button6.place(x=700,y=320,width=88,height=64)

button7=tk.Button(root,text="困難\n\n理牌なし",bg="red",foreground="white")
button7.bind("<1>", lambda event:c_draw_new(event,root,images,s_mylist,3,text1,text_d) )
button7.place(x=800,y=320,width=88,height=64)

text1=tk.Text(root,bg="white")
text1.delete( 0. , tk.END )
strtxt = "アガリ牌の数字をクリックして緑にした後、決定を押して下さい。\n※アガリが存在しない場合は、何も選択しないこと"
text1.insert(tk.END, strtxt )
# text1.place(x=10,y=300,width=450,height=60)

Label_d=tk.Label(root,text="デバッグ表示",bg="yellow")
Label_d.bind("<1>",dprint)
Label_d.place(x=10,y=500,width=200,height=16)

text_d=tk.Text(root,bg="white")
text_d.delete( 0. , tk.END )
strtxt = "みんなには　ナイショだよ"
text_d.insert(tk.END, strtxt )
text_d.place(x=10,y=520,width=800,height=80)

frame1 = tk.Frame(root, bg="lightgray", bd=1, relief='solid' )
# frame1 = ttk.Frame(root, borderwidth=1, width=200, height=100, relief='solid' )
# frame1.place(x=1055,y=155,width=190,height=150)
frame1.place(x=900,y=295,width=340,height=100)

Button_act1 = NeoButton_START()
Button_act1.place(x=905,y=300,width=50,height=50)
# Button_act1.place_configure(x=1100,y=200,width=100,height=100)

Button_act2 = NeoButton_WAIT()
Button_act2.place(x=960,y=300,width=50,height=50)
# # Button_act2.place_configure(x=1100,y=200,width=100,height=100)

Button_act3 = NeoButton_STOP()
Button_act3.place(x=1020,y=300,width=50,height=50)
# Button_act3.place_configure(x=1100,y=200,width=100,height=100)

# button_game=tk.Button(root,text="ゲーム開始",bg="orange")
# button_game.bind("<1>", c_game )
# button_game.place(x=10,y=210,width=400,height=100)

button_menu=tk.Button(root,text="メニューへ戻る",bg="orange")
button_menu.bind("<1>", c_menu )
# button_menu.bind("<1>", print_list )
# button_menu.place(x=1100,y=320,width=88,height=64)

options = glob.glob(p_dir+"\\*.mid")
combobox1 = ttk.Combobox(root, values=options, state="readonly", postcommand=update_values)
if len(options)==0:
    Button_act1["state"] = tk.DISABLED
else:
    combobox1.set(options[0])
    Button_act1["state"] = tk.NORMAL
combobox1.bind("<<ComboboxSelected>>", on_select)

combobox1.place(x=905,y=360,width=330,height=30)

text_message = tk.StringVar()
text_message.set("待機中\n(midﾌｧｲﾙのみ対応)")
label_info = tk.Label(textvariable = text_message, font = ("", 10,"bold"), justify = "left")
label_info.bind("<3>",dprint)

if __name__ == "__main__":
    # game()
    menu()
