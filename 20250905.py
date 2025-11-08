long_text = 'this is a long text'

a = 'aaa'
b = 'bbb'
c = 11

print(a, c, b) 

#讓使用者輸入資訊
# name = input("請輸入姓名:") 
# print(name)

# age = input("請輸入年齡：")
# print(age)


complex_number = 5 + 3j  # 複數 complex, 代表複數數字
print(complex_number)

# 建立一個複數：實部為 3，虛部為 5
z = 3 + 5j

print(f"複數 z 是：{z}")
print(f"z 的型別是：{type(z)}")

# 可以分別取得實部和虛部
print(f"z 的實部是：{z.real}")
print(f"z 的虛部是：{z.imag}")

# 進行複數運算
z1 = 2 + 3
z2 = 1 - 4j

print(f"z1 + z2 = {z1 + z2}")
print(f"z1 - z2 = {z1 - z2}")
print(f"z1 * z2 = {z1 * z2}")
print(f"z1 / z2 = {z1 / z2}")

n1, n2 = map(int, input().split())
print(n1 + n2)