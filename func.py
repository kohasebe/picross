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
            elif (line_type == "row"):
                df.iloc[i] = globals()[logic](df.iloc[i], setting[i])

    if (before.equals(df)):
        return False
    else:
        return True

def create_line_serialize(status, num):
    return status + ":" + str(num)

def update_line_serialize(line_serialize, i, serialize):
    # ほんとはこう書いてたけどforループの中でline_serializeを更新する動きができなくなるのでしかたなく変えた
    # line_serialize[i] = ",".join(serialize)
    del line_serialize[i]
    for s in serialize:
        line_serialize.insert(i, s)
        i += 1

    return get_line_serialize(create_line(line_serialize))

def split_line_serialize(serialize):
    status, num = serialize.split(":")
    return status, int(num)

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

# 2 [e,e,e,e,e]のとき何もしない
# 2 [e,e,x,e,e]のとき何もしない
# 3 [x,e,e,e,e]のとき[x,e,o,o,e]にする
# 1,2 [o,x,e,e,e]のとき[o,x,e,o,e]にする
# 1,3,3 [o,x,e,e,e,e,e,e,e,e]のとき何もしない
def open6(dfi, settingi):
    line_serialize = get_line_serialize(dfi)

    for s in settingi:
        # 候補チェック
        check = 0 # s以上のemptyが複数回出てきたら無視する
        flg = False
        for ls in line_serialize:
            status, num = split_line_serialize(ls)
            if (status == config.empty):
                # 2 [e,e,e,e,e]のとき何もしない
                if (num/2 > s):
                    flg = True
                    continue

                # 2 [e,e,x,e,e]のとき何もしない
                if (num >= s):
                    check += 1
                    if (check > 1):
                        flg = True

        if (flg):
            continue

        # 一回しか出てこなかったので次のロジックに行く
        # 3 [x,e,e,e,e]のとき[x,e,o,o,e]にする
        # 1,2 [o,x,e,e,e]のとき[o,x,e,o,e]にする
        for i, ls in enumerate(line_serialize):
            status, num = split_line_serialize(ls)
            if (status == config.empty and num > s): # == のパターンはopen3で吸収してる
                # 例えばnum=4, s=3のときは有効, 例えばnum=6, s=3のときは無効
                diff = num - s
                if (diff > 0 and s > diff):
                    line_serialize = update_line_serialize(line_serialize, i, [
                        create_line_serialize(config.empty, diff),
                        create_line_serialize(config.open, s - diff),
                        create_line_serialize(config.empty, diff)
                    ])
                    continue

    return create_line(line_serialize)

# 確定した箇所の両端をblankで埋める
# 1,1 [o,e,e,e,e]のとき[o,x,e,e,e]にする
# 1,1 [e,e,e,e,o]のとき[e,e,e,x,o]にする
# 1,1 [o,e,x,e,e]のとき[o,x,x,e,e]にする
def open7(dfi, settingi):
    line_serialize = get_line_serialize(dfi)
    for se_i, se in enumerate(settingi):
        for ls_i, ls in enumerate(line_serialize):
            status, num = split_line_serialize(ls)
            if (status == config.open and num == se):
                # ネクストがあるかをチェック
                if (len(line_serialize) > ls_i + 1):
                    next_ls = line_serialize[ls_i + 1]
                    # 始端を考える
                    # 1,1 [o,e,e,e,e]のとき[o,x,e,e,e]にする
                    if (se_i == 0):
                        next_status, nextnum = split_line_serialize(next_ls)
                        if (next_status == config.empty):
                            line_serialize = update_line_serialize(line_serialize, ls_i + 1, [
                                create_line_serialize(config.blank, 1),
                                create_line_serialize(next_status, nextnum - 1),
                            ])
                    else:
                        # 間にある場合
                        # 1,1 [e,e,o,e,e]のとき[e,x,o,x,e]にする
                        # 1,2 [e,e,o,e,e,e]のとき何もしない
                        print
                else:
                    # 終端を考える
                    # 1,1 [e,e,e,e,o]のとき[e,e,e,x,o]にする
                    if (len(settingi) == se_i + 1):
                        previous_status, previous_num = split_line_serialize(line_serialize[ls_i-1])
                        if (previous_status == config.empty):
                            line_serialize = update_line_serialize(line_serialize, ls_i - 1, [
                                create_line_serialize(previous_status, previous_num - 1),
                                create_line_serialize(config.blank, 1),
                            ])

    return create_line(line_serialize)


# 1,1 [e,e,o,e,e]のとき[e,x,o,x,e]にする
# 1,2 [e,e,o,e,e,e]のとき何もしない
# 1,2 [e,x,o,e,e,e]のとき何もしない
# def open5(dfi, settingi):

# 3,3 [e,e,e,e,e,e,e,e]のとき[e,o,o,e,e,o,o,e]にする
# 3 [x,e,o,e,e]のとき[x,e,o,o,e]にする
# 3 [x,e,e,o,e]のとき[x,e,o,o,e]にする
# 1,4 [e,x,o,e,e,e,e,e]のとき何もしない
# def open5(dfi, settingi):



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

