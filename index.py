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
logics = ["open1"]

# 最後のmainの形を想像する
while (func.check_continue(df)):
    before = df.copy()
    for logic in logics:
        func.main_logic(df, logic)

    # print(before)
    # print(df)
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

print(pd.__version__)
