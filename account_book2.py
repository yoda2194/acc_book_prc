
import json
import os.path
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from flask import Flask, request, render_template

app = Flask(__name__)
class AccountBook:
    def __init__(self, filename='C:/Users/Admin/PycharmProjects/Python_Basic/account_book.json'):
        self.filename = filename
        self.data = defaultdict(list)
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
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

    # @app.route('/', methods = ['POST','GET'])
    # def user_input(self):
    #     if request.method == 'GET':
    #         return render_template('index.html')
    #     else:
    #         date = request.form['input_date']
    #         inex = request.form['input_inex']
    #         price = request.form['input_price']
    #         detail = request.form['input_detail']
    #         self.add_transaction(date, inex, price, detail)
    #         return render_template('index_result.html',
    #                                context=self.data)

    #현재 잔액 계산 함수
    def calculate_balance(self):
        balance = 0
        for date, transactions in self.data.items():
            for transaction in transactions:
                if transaction['inex'] == "income":
                    balance += transaction['price']
                if transaction['inex'] == 'expense':
                    balance -= transaction['price']
        print(f"현재 잔액: {balance}")
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
                if transaction['inex'] == "expense" and transaction['price'] >= max_expense:
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
        for month, stats in monthly_stats.items():
            print(f"{month}월 수익 합계 : {stats['sum_income']}, {month}월 지출 합계: {stats['sum_expense']}")
        return monthly_stats

    # 잔액 변동량 구하기
    def balance_variance_plot(self):
        x = []
        y = []
        daily_balance = 0
        for date, transactions in self.data.items():
            for transaction in transactions:
                if transaction['inex'] == 'income':
                    daily_balance += transaction['price']
                    # x.append(datetime.strptime(transaction['date'], '%y-%m-%d'))
                    x.append(transaction['date'])
                if transaction['inex'] == 'expense':
                    daily_balance -= transaction['price']
                    # x.append(datetime.strptime(transaction['date'], '%y-%m-%d'))
                    x.append(transaction['date'])
                y.append(daily_balance)
        x.sort()
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

if __name__ == '__main__':

    # app.run()
    while True:
        print("-----가계부 메뉴-----")
        print("1. 입력")
        print("2. 잔액 조회")
        print("3. 월별 합계")
        print("4. 최대 수익 / 지출일 조회")
        print("5. 잔액 변동량 조회")
        print("6. 종료\n")
        print("-"*20,"\n")
        menu_num = int(input())
        if menu_num == 1:
            book.input_transaction()
        elif menu_num == 2:
            book.calculate_balance()
        elif menu_num == 3:
            book.calculate_monthly_sum()
        elif menu_num == 4:
            book.max_inex()
        elif menu_num == 5:
            book.balance_variance_plot()
        elif menu_num == 6:
            break