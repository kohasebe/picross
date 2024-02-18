import config

def main_logic(df, logic):
    line_types = ["column", "row"]
    for line_type in line_types:
        setting = config.picross[line_type]["setting"]
        for i in range((len(setting))):
            if (line_type == "column"):
                df[i] = globals()[logic](df[i], setting[i])
            elif (line_type == "row"):
                df.iloc[i] = globals()[logic](df.iloc[i], setting[i])


def get_status(dfi):
    status = []
    for i in range(len(dfi)):
        s = dfi[i]
        if(i == 0):
            status.append(s + ":1")
        else:
            last_status = status[-1].split(":")
            if (last_status[0] == s):
                last_status[1] = int(last_status[1]) + 1
                status[-1] = s + ":" + str(last_status[1])
            else:
                status.append(s + ":1")

    return status

def create_line(status):
    line = []
    for s in status:
        s_a = s.split(":")
        for i in range(int(s_a[1])):
            line.append(s_a[0])
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
# 例
# 5 [e,e,e,e,e]のとき[o,o,o,o,o]にする
def open1(dfi, settingi):
    length = config.picross["length"]
    if (length == settingi[0]):
        return [config.open] * length
    else:
        return dfi

# openとblankの数を足すと全長と一致するときopenとblankを確定させる
# 例
# 1 1 1 [e,e,e,e,e]のとき[o,x,o,x,o]にする
def open2(dfi, settingi):
    length = config.picross["length"]
    count = sum(settingi) + len(settingi) - 1
    if (len(settingi) >= 2 and length == count):
        status = []
        for i, s in enumerate(settingi):
            status.append(config.open + ":" + str(s))
            # 最後の要素じゃなかったらblankを追加する
            if (i != (len(settingi) - 1)):
                status.append(config.blank + ":1")

        return create_line(status)
    else:
        return dfi

# 2 1 [x,e,e,e,e]のとき[x,o,o,x,o]にする
def open3(dfi, settingi):
    return

def fill_blank(dfi, settingi):
    return

