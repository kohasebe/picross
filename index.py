import pandas as pd
import numpy as np
import config
import func

# 行列の設定をする
row_length = config.picross["row"]["length"]
column_length = config.picross["column"]["length"]

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
    df = func_name(df, i, "column")
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

print("結果はこちら")
print(df)


print(pd.__version__)
