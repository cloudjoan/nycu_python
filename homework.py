import time
import sys
# 算圓周面積、圓周長
# r = float(input())
# print('圓面積:', round(3.14 * r ** 2, 2))
# print('圓周長:', round(2 * 3.14 * r, 2))

#nycu python class HA output NYCU Python Class haha
# w1, w2, w3, w4 = map(str, input().split())

# print(w1.upper(), w2.capitalize(), w3.capitalize(), (w4*2).lower())



#菜鳥的工作
# x = list(map(int, input().split(',')))
# print(f"最菜鳥的工作年資是{min(x)}年")

#迴文
# s = input()
# s = s.lower().replace(' ', '')
# if s == s[::-1]:
#     print(True)
# else:
#     print(False)

#數字位數加總
# sum = 0
# for i in list(input()):
#     sum += int(i)
# print(sum)

#Merry X'mas
# i = int(input())
# if i > 1 :
#     for j in range(i):
#         print((' '*(i-j-1)) + "*" * (2*j+1))
#     for k in range(i-1):
#         print(' '* (i-1) + '|')
# else:
#     print("*")



#1854 . 簡易字串運算
# s = list(map(str, input().split()))
# print(s[0].capitalize() + '_' + s[1].capitalize())
# s = input().split()
# print(s[0].capitalize() + '_' + s[1].capitalize())

# 1855 . 匯率轉換
# ex = float(input())
# us = input().split()
# for i in us:
#     print(f"us_price:{i}, tw_price:{round(float(i)*ex)}")

# 1856 . 簡易型開票統計
# r = input().split()
# outcome = {}
# for ri in r:
#     if ri in outcome:
#         outcome[ri] += 1
#     else:
#         outcome[ri] = 1

# for o in outcome:
#     print(f"{o} {outcome[o]}")

#1857 .最遠的距離
# import math
# list = [(1, 1), (3, 4), (5, 3)]
# tg = (2.5, 2.5)
# rs = {}
# #計算距離
# for i in list:
#     result = round(math.sqrt(abs(i[0]-tg[0])**2 + abs(i[1]-tg[1])**2), 2)
#     rs[result] = i
# #找key值最大值
# print(f"{rs[max(rs)]} 距離為{max(rs)}")

#1858 . 多層金剛鑽
# n = int(input())
# rs = []
# for i in range(n//2):
#     if(i == 1) : print('$')
#     #同時塞前後？

# print(f'Hello {input()} !')

#1869 . 變數交換
# a = input()
# b = input()
# b, a = a, b
# print(f'a={a} and b={b}')

#1875 . 串列元素改位子
# s = list(map(int, input().split()))
# s.insert(0, s.pop())
# print(s)


# import math 

# math.sq

# #1876 . 移除重複元素並排序
# s = list(map(int, input().replace(' ', '').split(',')))
# s = set(s)
# print(s)

# print(str(sorted(set(s))).replace('[', '').replace(']', ''))
# str.join()


# 1878 . 生日快樂
# s = input().lower().replace(',', '').split()
# outcome = {}
# for si in s:
#     if si in outcome:
#         outcome[si] += 1
#     else:
#         outcome[si] = 1

# for o in outcome:
#     print(f"{o} {outcome[o]}")


#1879 . 分數判斷
# s = list(map(int, (input().split())))
# for i in s:
#     if i < 0 or i > 100 : print('Error')
#     elif i > 60 : print('Pass')
#     else : print('Fail')


# 1880 . 找20內的質數 
# for i in range(2, 20):
#     for j in range(2, i): #由比自身數字小的，如果無餘數就表示不是質數
#         if i % j == 0:
#             break
#     else:
#         print(f'{i} is Prime')

#1881 . n!
# import math

# n = int(input())
# print(math.factorial(n))


#1882 . 判斷等比數列
# def is_geometric(arr):
#     if len(arr) < 2:
#         return True
    
#     ratio = arr[1] / arr[0]
#     for i in range(2, len(arr)):
#         if arr[i] / arr[i-1] != ratio:
#             return False
#     return True

# arr = list(map(int, input().split()))

# if is_geometric(arr):
#     print('Yes')
# else:
#     print('No')

#1884 生命靈數
# birthdayNum = list(map(int, (input().replace(' ', ''))))

# life_num = 999

# while len(str(life_num)) > 1:
#     life_num = 0
#     for i in birthdayNum:
#         life_num += i

#     birthdayNum = list(map(int, str(life_num)))

# print(life_num)


# print(_num)

# 1981 . 派派村
# n = int(input())
# #10進位轉2進位，並計算2進位含有1的數量
# sum_buck = bin(n).count('1')
# bucks = list(str(bin(n)).replace('0b', ''))
# #foreach從後面開始
# buckList = []
# for i in range(len(bucks)):
#     if bucks[len(bucks)-1-i] == '1':
#         buckList.append(2**i)

# print(sum_buck)
# print(str(buckList).replace('[', '').replace(']', '').replace(',', ''))

#1980 . 出國換錢
# r = float(input())
# usds = input().split()
# for i in usds:
#     print(round(float(i)*r))

#1886 . 完全平方和
# i = 0
# sum = 0
# while i**2 <= 30:
#     sum += i**2
#     i += 1

# print(sum)

#1982 . 直角三角形
# nums = list(map(int, input().split()))
# nums.sort(reverse=True)

# if(nums[0]**2 == nums[1]**2 + nums[2]**2):
#     print('Y')
# else:
#     print('N')

#1882 . 判斷等比數列
# tn = int(input())
# nums = list(map(int, input().split()))
# r = nums[0] / nums[1]
# result = True
# if(tn == len(nums)):
#     for i in range(len(nums)-1):
#         if r != nums[i] / nums[i+1]:
#             result = False
#             break
#     print(result)
# else:
#     print(False)

#1885 . 四則運算
# nums = input().split()
# result = 0
# if(nums[1] == '+'):
#     result = int(nums[0]) + int(nums[2])
# elif(nums[1] == '-'):
#    result = int(nums[0]) - int(nums[2])
# elif(nums[1] == '*'):
#     result = int(nums[0]) * int(nums[2])
# elif(nums[1] == '/'):
#     result = int(nums[0]) / int(nums[2])

# print(f'{nums[0]} {nums[1]} {nums[2]} = {result}')

#1895 . 月月是好月
#依輸入數字，轉換成英文3字縮寫月份
# i = int(input())
# mom_dic = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
# print(mom_dic[i])

#1975 . 最小公倍數(LCM)
#找2個數的最小公倍數

#1986 . 左左右右
# s = list(input())
# if s[0] == '(' and s[-1] == ')':
#     print(True)
# else:
#     print(False)

# 14:00 to datetime

#1979 . 找因數
# n = int(input())
# result = []
# for i in range(1, n+1):
#     if n % i == 0 :
#         result.append(i)

# print(str(result).replace('[', '').replace(']', '').replace(',', ''))

#1975 . 最小公倍數(LCM)
# nums = list(map(int, input().split()))

# min_num = min(nums)
# max_num = max(nums)

# if max_num % min_num == 0:
#     print('LCM:', max_num)
# else:
#     times = 1
#     while True:
#         if min_num * times % max_num == 0:
#             print('LCM:', min_num * times)
#             break
#         else:
#             times += 1

#1983 . Two Sum
# nums = list(map(int, input().split()))
# target = int(input())

# for i in range(len(nums)):
#     for j in range(i+1, len(nums)):
#         if nums[i] + nums[j] == target:
#             print(nums[i], nums[j])

#1883 . 信用卡號驗證
# card_nums = [input(), input(), input()]
# result = []

# for card_num in card_nums:
#     odd_sum = 0 
#     even_sum = 0
#     check_sum = 0
#     card_num = card_num.replace('-', '')
#     for i in range(len(card_num)-1):
#         if int(i+1) % 2 == 1:
#             i_odd = int(card_num[i]) * 2
#             if i_odd >= 10:
#                 i_odd = i_odd - 9
#             odd_sum += i_odd
#         else:
#             even_sum += int(card_num[i])
#     check_sum = odd_sum + even_sum
#     check_sum = 10 - (check_sum % 10)

#     if check_sum == int(card_num[-1]):
#         if(card_num[0]=='5'):
#             result.append('MASTER_CARD')
#         elif(card_num[0]=='4'):
#             result.append('VISA_CARD')
#     else:
#         result.append('INVALID')

# for r in result:
#     print(r)

#1976 . Tic-Tac-Toe 判斷勝負
# nums = [input(), input(), input()]
# outcome = '和局'

# #判斷row
# for num in nums:
#     if num == 'OOO':
#         outcome = 'O勝'
#         break
#     elif num == 'XXX':
#         outcome = 'X勝'
#         break

# #判斷column
# for i in range(3):
#     if nums[0][i] and (nums[0][i] == nums[1][i] == nums[2][i]):
#         outcome = f'{nums[0][i]}勝'
#         break

# #判斷交叉
# if nums[0][0] and (nums[0][0] == nums[1][1] == nums[2][2]):
#     outcome = f'{nums[0][0]}勝'
    
# elif nums[0][2] and (nums[0][2] == nums[1][1] == nums[2][0]):
#     outcome = f'{nums[0][2]}勝'
    

# print(outcome)


#1974 . 凱撒密碼
# move_index = int(input())
# content = input()
# encrypt_content = ''
# alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# for c in content:
#    if c in alphabets:
#       encrypt_content += alphabets[(alphabets.index(c) + move_index) % 26]
#    else:
#       encrypt_content += c

# print(encrypt_content)

#1978 . 停車收費
# from datetime import time

# time_in = time.fromisoformat(input())
# time_out = time.fromisoformat(input())

# #計算總分鐘數
# total_minutes = (time_out.hour * 60 + time_out.minute) - (time_in.hour * 60 + time_in.minute)

# if(total_minutes < 15):
#     print(0)
# elif( 15 <= total_minutes <= 60):
#     print(40)
# else:
#     half_h, re_minutes = divmod((total_minutes - 60), 30)
#     fee = 40 + half_h * 20 + (20 if re_minutes > 0 else 0)
#     print(fee)


# #提款機
# msg = """
# 1. 查詢餘額
# 2. 存款
# 3. 提款
# 4. 離開
# """

# print(f'=== 歡迎使用 ATM 系統 ===')

# money = 1000

# while True:
#     print(msg)
#     command = input('請選擇功能：')

#     if command == '1':
#         print(f'目前餘額:{money}')
#         continue
        
#     elif command == '2':
#         deposit = int(input('請輸入存款金額：'))
#         if deposit <= 0:
#             print('金額請請大於0')
#             continue
#         else:
#             money += deposit
#             print(f'存款成功，目前餘額:{money}')
#             continue
#     elif command == '3':
#         withdraw = int(input('請輸入提款金額：'))
#         if withdraw > money:
#             print('餘額不足，提款失敗！')
#             continue
#         else:
#             money = money - withdraw
#             print(f'提款成功！目前餘額:{money}')
#             continue
#     elif command == '4':
#         print('感謝使用，程式結束！')
#         break


