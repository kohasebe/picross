import config

# とりあえず全部開ける
def open_all(x):
    return config.open

# 全長と一致するラインを開ける
def open1(df, i, line_name):
    length = config.picross[line_name]["length"]
    if (length == config.picross[line_name]["setting"][i][0]):
        df[i] = [config.open] * length

    return df