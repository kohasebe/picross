import config

# dfは参照渡しで更新される
def main_logic(df, logic):
    before = df.copy()
    line_types = ["column", "row"]
    for line_type in line_types:
        setting = config.picross[line_type]["setting"]
        for i in range((len(setting))):
            if (line_type == "column"):
                df[i] = globals()[logic](df[i], setting[i])
                print
            elif (line_type == "row"):
                df.iloc[i] = globals()[logic](df.iloc[i], setting[i])

    if (before.equals(df)):
        return False
    else:
        return True

def create_line_serialize(status, num):
    return status + ":" + str(num)

def split_line_serialize(serialize):
    return serialize.split(":")

def get_line_serialize(dfi):
    status = []
    for i in range(len(dfi)):
        s = dfi[i]
        if(i == 0):
            status.append(create_line_serialize(s, 1))
        else:
            last_status, num = split_line_serialize(status[-1])
            if (last_status == s):
                num = int(num) + 1
                status[-1] = create_line_serialize(s, num)
            else:
                status.append(create_line_serialize(s, 1))

    return status

def create_line(line_serialize):
    line = []
    for ls in line_serialize:
        for l in ls.split(","):
            if isinstance(l, list):
                for v in l:
                    status, num = split_line_serialize(v)
                    for i in range(int(num)):
                        line.append(status)
            else:
                status, num = split_line_serialize(l)
                for i in range(int(num)):
                    line.append(status)
    return line

def check_continue(df):
    open_count = 0
    empty_count = 0
    for index, row in df.iterrows():
        for value in row:
            if (value == config.open):
                open_count += 1
            elif (value == config.empty):
                empty_count += 1

    expected_count = 0
    for setting in config.picross["row"]["setting"]:
        for num in setting:
            expected_count += num

    if (empty_count == pow(config.picross["length"], 2)):
        return True
    elif (open_count == expected_count):
        return False
    else:
        return True

# 全長と一致するラインを開ける
# 5 [e,e,e,e,e]のとき[o,o,o,o,o]にする
def open1(dfi, settingi):
    length = config.picross["length"]
    if (length == settingi[0]):
        return [config.open] * length
    else:
        return dfi

# openとblankの数を足すと全長と一致するときopenとblankを確定させる
# 1 1 1 [e,e,e,e,e]のとき[o,x,o,x,o]にする
def open2(dfi, settingi):
    length = config.picross["length"]
    count = sum(settingi) + len(settingi) - 1
    if (len(settingi) >= 2 and length == count):
        line_serialize = []
        for i, s in enumerate(settingi):
            line_serialize.append(create_line_serialize(config.open , str(s)))
            # 最後の要素じゃなかったらblankを追加する
            if (i != (len(settingi) - 1)):
                line_serialize.append(create_line_serialize(config.blank, 1))

        return create_line(line_serialize)
    else:
        return dfi

# blankの数から確定させる
# 2 1 [x,e,e,x,e]のとき[x,o,o,x,o]にする
# 2 1 [x,o,e,x,e]のとき[x,o,o,x,o]にする
def open3(dfi, settingi):
    # 全体からblankの数を引いた数が設定値の合計と同じなら全部埋める
    if ((config.picross["length"] - dfi.value_counts().get(config.blank, 0)) == sum(settingi)):
        for i, v in enumerate(dfi):
            if (v == config.empty):
                dfi[i] = config.open
    return dfi

# openの数から確定させる
# 2 [o,o,x,e,e]のとき[o,o,x,x,x]にする
# 2 1[o,o,x,o,e]のとき[o,o,x,o,x]にする
def open4(dfi, settingi):
    # openの数が設定値の合計と同じなら残りを全部blankにする
    if ((dfi.value_counts().get(config.open, 0)) == sum(settingi)):
        for i, v in enumerate(dfi):
            if (v != config.open):
                dfi[i] = config.blank
    return dfi

# 盤面の過半数より大きい数字の時はいい感じにopenする
# 4 [e,e,e,e,e]のとき[e,o,o,o,e]にする
def open5(dfi, settingi):
    length = config.picross["length"]
    line_serialize = get_line_serialize(dfi)
    max_empty_size = 0
    # 強烈に上書きをするのでemptyのサイズをチェックして一回しか実施しないようにする
    for ls in line_serialize:
        status, num = split_line_serialize(ls)
        if (status == config.empty):
            if (max_empty_size == 0 or num > max_empty_size):
                max_empty_size = int(num)

    line_serialize = []
    if (settingi[0] > length/2 and max_empty_size >= settingi[0]):
        diff = length - settingi[0]
        line_serialize = [
            create_line_serialize(config.empty, diff),
            create_line_serialize(config.open, settingi[0] - diff),
            create_line_serialize(config.empty, diff)
        ]
        return create_line(line_serialize)
    else:
        return dfi

# 3 [x,e,e,e,x,e,e,e]のとき何もしない
# 3 [x,e,e,e]のとき[x,o,o,o]にする

# 3 [x,e,e,e,e]のとき[x,e,o,o,e]にする
# 3 [x,e,o,e,e]のとき[x,e,o,o,e]にする
# 3 [x,e,e,o,e]のとき[x,e,o,o,e]にする
# 1,4 [e,x,o,e,e,e,e,e]のとき何もしない
# 1,4 [o,x,e,e,e,e,e]のとき[o,x,e,o,o,o,e]にする
def open6(dfi, settingi):
    line_serialize = get_line_serialize(dfi) # x:1,e:3
    before = line_serialize.copy()

    # 候補チェック
    for s in settingi:
        # 3 [x,e,e,e,x,e,e,e]のとき何もしない
        check1 = 0 # sより大きいemptyが複数回出てきたら無視する
        for ls in line_serialize:
            status, num = split_line_serialize(ls)
            if (status == config.empty):
                if (num >= s):
                    check1 += 1
        if (check1 > 1):
            continue

        # 一回しか出てこなかったので次のロジックに行く
        # 3 [x,e,e,e,e]のとき[x,e,o,o,e]にする
        for i, ls in enumerate(line_serialize):
            status, num = split_line_serialize(ls)
            if (status == config.empty and num > s): # == のパターンはopen3で吸収してる
                line_serialize[i] = create_line_serialize(config.open, s)
                continue


    if (before.equals(line_serialize)):
        return dfi
    else:
        return create_line(line_serialize)

# 3 [x,e,e,e,x,e,e,e]のとき何もしない
def open6_1(dfi, settingi):

    return False

# 2 [e,e,x,e,e]のときなにもしない
# 2 1 [e,e,x,e,e]のとき[o,o,x,e,e]にする
# 2 [e,x,x,e,e]のとき[x,x,x,o,o]にする
# def open5(dfi, settingi):
#     line_serialize = get_line_serialize(dfi)
#     for i, se in enumerate(settingi):
#         count = 0
#         for ls in line_serialize:
#             # 全部空いてたらスルーする(#a)
#             if (ls == (config.open + str(se))):
#                 # それが最後の要素だったら他のとこはblankで埋める(#a)
#                 if (i == (len(settingi) - 1)):
#                     c_flg = True
#                 break
#             elif (ls == (config.empty + str(se))):
#                 count += 1

#         if (count == 1):
#             print

#         else:
#             continue
#         break


# 2 [e,o,e,x,e]のとき[e,o,e,x,x]にする
# 2 [e,o,e,x,e,e]のとき[e,o,e,x,x,x]にする
# def open4(dfi, settingi):
#     status = get_status(dfi)
#     return

# 2 1 [x,e,e,e,e]のとき[x,o,o,x,o]にする
# 2 1 [x,e,e,e,e,x,e,e,e,e]のときはなにもしない
# def open5(dfi, settingi):
#     return

# 2 [x,e,e,e,x,e]のとき[x,e,o,e,x,e]にする
# 2 [x,e,e,e,x,e,e]のときなにもしない
# def open6(dfi, settingi):
#     status = get_status(dfi)
#     return

# 2 1 [x,e,e,e,x,e,e]のとき[x,e,o,e,x,e,e]にする
# 2 1 [x,e,e,e,x,e,e,e,e]のときなにもしない
# def open7(dfi, settingi):
#     status = get_status(dfi)
#     return

# 端っこが確定した時の処理
# 2 1 [x,o,e,e,e]のとき[x,o,o,e,e]にする
# 2 1 [e,x,o,e,e,e]のとき[e,x,o,o,x,o]にする(openの数が設定と一致するので次のループでeはxになる)
# def open7(dfi, settingi):
#     return



def fill_blank(dfi, settingi):
    return

