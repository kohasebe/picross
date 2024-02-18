import sys

empty = 'empty'
blank = 'blank'
open = 'open'

# empty = '□'
# blank = 'x'
# open = '■'

# expected = {
#     0: [o, o, o, o, o],
#     1: [o, o, e, e, e],
#     2: [o, x, o, x, o],
#     3: [o, o, e, e, e],
#     4: [o, o, e, e, e]
# }

picross = {
    "length": 5,
    "row": {
        "setting": [
            [5],
            [2],
            [1,1,1],
            [2],
            [2]
        ]
    },
    "column": {
        "setting": [
            [5], [2,2], [1,1], [1], [1,1]
        ]
    }
}
