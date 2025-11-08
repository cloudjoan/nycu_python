msg = """=== 歡迎使用 ATM 系統 ===
1. 查詢餘額
2. 存款
3. 提款
4. 離開
"""

print(msg)

money = 1000
command = input('請選擇功能：')

while command != '4':

    if command == '1':
        print(f'目前餘額:{money}')
        command = input('請選擇功能：')
    elif command == '2':
        deposit = int(input('請輸入存款金額：'))
        if deposit <= 0:
            print('金額請請大於0')
        else:
            money += deposit
            print(f'存款成功，目前餘額:{money}')
        command = input('請選擇功能：')
    elif command == '3':
        withdraw = int(input('請輸入提款金額：'))
        if withdraw > money:
            print('餘額不足，提款失敗！')
            command = input('請選擇功能：')
        else:
            money = money - withdraw
            print(f'提款成功！目前餘額:{money}')
            command = input('請選擇功能：')

if command == '4':
    print('感謝使用，程式結束！')