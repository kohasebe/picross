import pandas as pd
import numpy as np
import config
import func

# 行列の設定をする
row_length = len(config.picross["row"]["setting"])
column_length = len(config.picross["column"]["setting"])

# 盤面を作る
df = pd.DataFrame(np.full((row_length, column_length), config.empty))

print("初期盤面はこちら")
print(df)

func_name = func.open1

# df.iloc[0]= df.iloc[0].apply(func.open_all)
# print(df)
# print("------ 初期操作完了 ------")

# 列操作
# 1列の操作
# df= df.assign(A=df["A"].apply(func_name))

# 全列の操作
for i in range(column_length):
    # df[i] = df[i].apply(func_name, args=(i, "column",))
    df = func_name(df[i], i, "column", config.picross)
    # for i in range(config.row_num):
    #     print(df[i][0])

# for column in df.columns:
#     print(df[column])
    # df[column] = df[column].apply(func_name(config.column_setting[column],))
    # df[column] = df[column].apply(func_name, args=(config.column_setting[column],))

# df = df.apply(lambda column: func_name(column, config.column_setting[column]), axis=0)

# 行操作
# 1行の操作
# df.iloc[func.get_line_num(1)]= df.iloc[func.get_line_num(1)].apply(func_name)

# 全行の操作
# for i in range(len(df.index)):
#     df.iloc[i] = df.iloc[i].apply(func_name)


line_types = ["column", "row"]
logics = ["open1", "open2"]
# 最後のmainの形を想像する
while (func.check_end()):
    before = df
    for line_type in line_types:
        setting = config.picross[line_type]["setting"]
        for i in range(len(setting)):
            for logic in logics:
                if (line_type == "column"):
                    df[i] = func.logic(df[i], setting[i])
                elif (line_type == "row"):
                    df.iloc[i] = func.logic(df[i], setting[i])

    if (func.check_diff(before, df)):
        print("差分があるので継続します")
    else:
        print("前回と差分がなくなりました")
        if (func.check_end()):
            print("現存のロジックで全てのマスを開けることができました")
        else:
            print("現存のロジックがたりないようです")
            break





print("結果はこちら")
print(df)


print(pd.__version__)
