import os
import copy
from time import sleep
from pandas import read_csv
from tkinter import Label, Frame, Button, Checkbutton, Tk, IntVar, HORIZONTAL, Scale
import tkinter.font as tkFont
from tkinter import ttk, scrolledtext
from VideoGame import VideoGame

loaded = False
NORECORD = 'NORECORD'
# 关联九种不同rating的intVar列表，为1时表示被选中
intVar = []
# 当前显示第n条记录，通过按钮进行切换
selection = 0
game_list = []
# 满足用户搜索条件的游戏
properties = []
rating_list =  ['E10+', 'T', 'K-A', 'RP', 'E', 'EC', 'AO', 'M']

# 启动应用时加载指定目录下的csv文件进行游戏对象创建
def load_csv():
    global game_list
    csv_filepath = './video-game-sales-with-ratings/Video_Games_Sales.csv'
    dataFrame = read_csv(csv_filepath)
    # 在这里对nan数据进行处理
    dataFrame.fillna(NORECORD,inplace=True)
    for _, row in dataFrame.iterrows():
        VideoGame(row)
    game_list = VideoGame.games
    return len(game_list)>0

# 以指定格式更改推荐游戏的内容
def change_display():
    global properties, selection
    display_message = '\n为您找到 {} 款游戏，当前显示第 {} 项\n\n游戏名称：{}\n游戏类型：{}\n发售时间：{}\n发售平台：{}\n开发者：{}\n媒体评分：{}\n大众评分：{}\n游戏销量（百万）：{}\n游戏评级：{}\n'.format(
                            len(properties), selection+1,
                            properties[selection].name, properties[selection].genre,properties[selection].year_of_release, properties[selection].platform,
                            properties[selection].developer, properties[selection].critic_score,properties[selection].user_score, properties[selection].global_sales,
                            properties[selection].rating)
    return display_message

# 根据用户的检索条件从游戏对象队列中遍历查找符合条件的对象
# 将符合条件的对象存储在properties中
def properties_filter():
    global properties, selection
    properties.clear()
    # 从各个组件中得到界面中用户选择的查询条件 
    platform = platform_select.get()
    genre = genre_select.get()
    l_bound = int(from_year_select.get())
    r_bound = int(to_year_select.get())
    critical_score_l = int(critical_score_scale.get())
    user_score_l = round((user_score_scale.get()),1)
    # 多项可选评级审查
    allowed_rating = []
    for idx in range(len(intVar)):
        if intVar[idx].get():
            allowed_rating.append(rating_list[idx])
    # 终端打印出用户的选取规则
    print('【RULE】',platform, genre, l_bound, r_bound, critical_score_l, user_score_l)
    for game in game_list:
        if game.platform == platform and game.genre == genre \
            and (game.year_of_release == NORECORD or game.year_of_release >= l_bound and game.year_of_release <= r_bound)\
                and (game.critic_score == NORECORD or game.critic_score >= critical_score_l) \
                    and(game.user_score == NORECORD or game.user_score >= user_score_l)\
                        and(game.rating == NORECORD or game.rating in allowed_rating):
            properties.append(game)
    # 终端符合用户要求的选区结果
    print('【RESULT】', len(properties))
    print()
    # 对搜索结果按照年份逆序排列
    properties = sorted(properties, key=lambda game: game.year_of_release if type(game.year_of_release) == int else -1, reverse=True)
    # 在窗口中显示符合用户要求的首条记录
    # 检测结果条数是否 > 0
    if len(properties):
        selection = 0
        result_message['text'] = change_display()
    else:
        result_message['text'] = '数据库中没有符合要求的游戏'

        
def next_message():
    global properties, selection
    if selection < len(properties)-1:
        selection += 1
        result_message['text'] = change_display()


def prev_message():
    global properties, selection
    if selection > 0:
        selection -= 1
        result_message['text'] = change_display()

if __name__ == '__main__':

    window = Tk()
    window.title("Play-Smart.expertsystem")
    window.geometry('1024x640')
    window.resizable(width=False, height=False)

    # 第0行与第一行放置给用户的推荐游戏信息
    message = Label(window, text='[EXPERT SYSTEM]', font=('Microsoft YaHei', 18))
    result_window = Frame(window, width=1024, height=180)
    # 保证窗口大小不变
    result_window.propagate(0)
    message.grid(row=0, columnspan=5)
    result_message = Label(result_window, text='还没有推荐内容')
    result_message.pack()
    result_window.grid(row=1, columnspan=5)

    if not loaded:
        loaded = load_csv()
        if not loaded:
            print('ERROR: CANT LOAD CSV FILE')
            sleep(3)
            exit()
    # 用于早期输出表中的特定属性种类以及具体内容
    VideoGame.show_genre()
    VideoGame.show_platform()

    # 第二行设置按钮，有多条推荐信息时用按钮进行切换
    prev_btn = Button(window, text='上一条', command=prev_message)
    next_btn = Button(window, text='下一条', command=next_message)
    prev_btn.grid(row=2, column=3, sticky='e', ipadx=20, pady=30)
    next_btn.grid(row=2, column=4, ipadx=20)

    # 第三行用于选择游戏所在平台以及游戏类型
    platform_label = Label(window, text='主机平台', font=('tMicrosoft YaHei',12,'bold'))
    genre_label = Label(window, text='游戏类型', font=('tMicrosoft YaHei',12,'bold'))
    platform_select = ttk.Combobox(window, value=sorted(list(VideoGame.Platform)))
    platform_select.current(0)
    genre_select = ttk.Combobox(window, value=sorted(list(VideoGame.Genre)))
    genre_select.current(0)
    platform_label.grid(row=3, column=0)
    platform_select.grid(row=3, column=1)
    genre_label.grid(row=3, column=2)
    genre_select.grid(row=3, column=3)

    # 第四行，选择游戏发售时间段
    time_range_labelA = Label(window, text='发售时间自', font=('tMicrosoft YaHei',12,'bold'))
    time_range_labelB = Label(window, text='年起至', font=('tMicrosoft YaHei',12,'bold'))
    from_year_select = ttk.Combobox(window, value=list(VideoGame.YearOfRelease))
    from_year_select.current(0)
    to_year_select = ttk.Combobox(window, value=list(VideoGame.YearOfRelease))
    to_year_select.current(len(VideoGame.YearOfRelease)-1)
    time_range_labelA.grid(row=4, column=0)
    time_range_labelB.grid(row=4, column=2)
    from_year_select.grid(row=4, column=1)
    to_year_select.grid(row=4, column=3)

    # 第五行，对游戏评分做出要求
    critical_score_scale = Scale(window, label='媒体评分高于', from_=0, to=100, orient=HORIZONTAL,
             length=400, showvalue=1, tickinterval=10, resolution=1)
    critical_score_scale.grid(row=5, column=0, columnspan=2)
    user_score_scale = Scale(window, label='大众评分高于', from_=0, to=10, orient=HORIZONTAL,
             length=400, showvalue=1, tickinterval=1, resolution=0.1)
    user_score_scale.grid(row=5, column=2, columnspan=2)

    # 第六行，确认提交所选游戏指标要求
    submit_btn = Button(window, text='提交', font=('Microsoft YaHei', 15), command=properties_filter)
    submit_btn.grid(row=6, column=2, ipadx=70, ipady=10, pady=10)

    # 最右列放置一个用于选择游戏分级的listGroup
    rating_frame = Frame(window)
    rating_frame.grid(row=3, column=4, rowspan=3)
    rating_note_label = Label(rating_frame, text='游戏评级选择', font=('tMicrosoft YaHei',12,'bold'))
    rating_note_label.pack()
    for idx in range(len(rating_list)):
        intVar.append(IntVar(value=1))
        check = Checkbutton(rating_frame, text=rating_list[idx], variable=intVar[idx], onvalue=1, offvalue=0)
        check.pack(side='top', expand='yes', fill='both')

    window.mainloop()