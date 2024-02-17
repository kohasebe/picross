import pandas as pd

# サンプルのデータフレーム
data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
df = pd.DataFrame(data)

# データフレームの行にapply
result = df.apply(lambda row: row.sum(), axis=1)

# 結果の表示
print(result)