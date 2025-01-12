
import json
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class AccountBook:
    def __init__(self, filename='C:/Users/Admin/PycharmProjects/Python_Basic/account_book.json'):
        self.filename = filename
        self.data = defaultdict(list)
        self.load_data()

    def load_data(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4, sort_keys=True)

    def add_transaction(self, date, inex, price, detail):
        transaction = {
            'date': date,
            'inex': inex,
            'price': price,
            'detail': detail
        }
        try:
            self.data[date].append(transaction)
        except:
            self.data[date] = []
            self.data[date].append(transaction)
        self.save_data()

    def input_transaction(self):
        txt_input = input("Enter your transaction (YY-MM-DD, income or expense, Price, Detail) : ")
        txt_split = txt_input.split(', ')
        date = txt_split[0]
        inex = txt_split[1]
        price = int(txt_split[2])
        detail = txt_split[3]
        self.add_transaction(date, inex, price, detail)

    #현재 잔액 계산 함수
    def calculate_balance(self):
        balance = 0
        for date, transactions in self.data.items():
            for transaction in transactions:
                if transaction['inex'] == "income":
                    balance += transaction['price']
                if transaction['inex'] == 'expense':
                    balance -= transaction['price']
        return balance

    #최대 지출 / 최대 수익 날짜 구하는 함수
    def max_inex(self):
        max_income = 0
        max_expense = 0
        max_income_date = []
        max_expense_date = []
        for date, transactions in self.data.items():
            max_date = date
            for transaction in transactions:
                if transaction['inex'] == "income" and transaction['price'] >= max_income:
                    max_income = transaction['price']
                    max_income_date.append(datetime.strptime(max_date,"%y-%m-%d"))
                if transaction['inex'] == "expense"  and transaction['price'] >= max_expense:
                    max_expense = transaction['price']
                    max_expense_date.append(datetime.strptime(max_date,"%y-%m-%d"))
        max_income_date = set(max_income_date)
        max_expense_date = set(max_expense_date)
        print(f'최대 수익 : {max_income}')
        for i in max_income_date:
            print('최대 수익일 :',i)
        print(f'최대 지출 : {max_expense}')
        for i in max_expense_date:
            print('최대 지출일 :',i)
        return max_income_date, max_income, max_expense_date, max_expense

    # 월별 지출 / 수익 합계 계산 함수
    def calculate_monthly_sum(self):
        monthly_stats = defaultdict(lambda: {'sum_income': 0, 'sum_expense': 0})
        for date, transactions in self.data.items():
            month = datetime.strptime(date, '%y-%m-%d').month
            for transaction in transactions:
                if transaction['inex'] == 'income':
                    income = transaction['price']
                    monthly_stats[month]['sum_income'] += income
                if transaction['inex'] == 'expense':
                    expense = transaction['price']
                    monthly_stats[month]['sum_expense'] += expense
        return monthly_stats

    # 잔액 변동량 구하기
    def balance_variance_plot(self):
        x = []
        y = []
        daily_balance = 0
        for date, transactions in self.data.items():
            x.append(datetime.strptime(date, '%y-%m-%d'))
            for transaction in transactions:
                if transaction['inex'] == 'income':
                    daily_balance += transaction['price']
                if transaction['inex'] == 'expense':
                    daily_balance -= transaction['price']
                y.append(daily_balance)
        plt.figure(figsize=(10,6))
        plt.plot(x, y, marker='o', linestyle = '-', label = 'Balance')
        plt.xlabel('Date')
        plt.ylabel('Balance')
        plt.title('Balance Changes Over Time')
        plt.xticks(rotation=25)
        plt.legend()
        plt.show()

# 예시 데이터 자동 생성 및 테스트
book = AccountBook()
# book.input_transaction()
# book.balance_variance_plot()

# 잔액 계산 및 출력
balance = book.calculate_balance()
print(f"현재 잔액: {balance}")

# 월별 지출 및 수익의 합계 계산 및 출력
monthly_stats = book.calculate_monthly_sum()
for month, stats in monthly_stats.items():
    print(f"{month}월 수익 합계 : {stats['sum_income']}, {month}월 지출 합계: {stats['sum_expense']}")

# 최대 지출 - 수익 날짜 출력
max_val = book.max_inex()
print(max_val)

# 잔액변동량 출력
book.balance_variance_plot()
