import config

def status(df, i, line_type):
    if (line_type == "column"):
        target = df[i]
    elif (line_type == "row"):
        target = df.iloc[i]

    status = []
    for i in range(len(target)):
        s = target[i]
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

# テスト用: とりあえず全部開ける
def open_all(x):
    return config.open

# 全長と一致するラインを開ける
def open1(dfi, settingi):
    length = config.picross["length"]
    if (length == settingi[0]):
        return [config.open] * length
    else:
        return dfi

def fill_blank(df, i, line_type, picross):
    return

def check_end(df):
    return False

def check_diff(before, after):
    return True