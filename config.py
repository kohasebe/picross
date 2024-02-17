import sys

empty = 'empty'
fill = 'fill'
open = 'open'

picross = {
    "row": {
        "length": 5,
        "setting": [
            [1,1],
            [1,1],
            [1],
            [1,1],
            [1,1]
        ]
    },
    "column": {
        "length": 5,
        "setting": [
            [0],
            [2,2],
            [0],
            [0],
            [5]
        ]
    }
}

# 行の設定
if len(picross["row"]["setting"]) != picross["row"]["length"]:
    sys.exit("[ERROR]行の長さと設定が異なります")

# 列の設定
if len(picross["column"]["setting"]) != picross["column"]["length"]:
    sys.exit("[ERROR]列の長さと設定が異なります")
