# for i in range(3):
#     print("Outer loop:", i)
#     for j in range(3):
#         print("Inner loop:", j)
#         if j == 1:
#             break  # 内側のループのみを中断する


for i in range(3):
    print("Outer loop:", i)
    for j in range(3):
        print("Inner loop:", j)
        if j == 1:
            break  # 内側のループから一気に抜ける
    else:
        continue
    break