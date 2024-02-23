import pandas as pd
import numpy as np
import config
import func

# 行列の設定をする
row_length = len(config.picross["row"]["setting"])
column_length = len(config.picross["column"]["setting"])

# 盤面を作る
df = pd.DataFrame(np.full((row_length, column_length), config.empty))

# print("初期盤面はこちら")
# print(df)

# line_types = ["column", "row"]
logics = {
    "open1": 0,
    "open2": 0,
    "open3": 0,
    "open4": 0,
    "open5": 0,
    "open6": 0,
    "open7": 0,
    "open8": 0,
}

# 最後のmainの形を想像する
while (func.check_continue(df)):
    before = df.copy()
    for logic in logics:
        if (func.main_logic(df, logic)):
            # ロジックが有効に働いた場合、カウントアップする
            logics[logic] += 1

    if (before.equals(df)):
        print("前回と差分がなくなりました")
        if (func.check_continue(df)):
            print("現存のロジックがたりないようです")
            break
        else:
            print("現存のロジックで全てのマスを開けることができました")
    else:
        if (func.check_continue(df)):
            print("差分があるので継続します")
        else:
            print("現存のロジックで全てのマスを開けることができました")
            break

print("結果はこちら")
print(df)

print("ロジックが有効に働いた回数は以下")
print(logics)


print(pd.__version__)
