
import json
import os.path
from io import BytesIO
import base64
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
from flask import Flask, request, render_template, jsonify


# app = Flask(__name__)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

class AccountBook_App:
    def __init__(self, filename='C:/Users/Admin/PycharmProjects/Python_Basic/account_book.json'):
        self.app = Flask(__name__)
        self.data = defaultdict(list)
        self.filename = filename
        self.configure_routes()

    def configure_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index_home.html')

        @self.app.route('/accbook', methods=['GET','POST'])
        def save_data():
            if request.method == 'POST':
                date = str(request.form['input_date'])
                inex = request.form['input_inex']
                price = int(request.form['input_price'])
                detail = request.form['input_detail']

                transaction = {
                    'date': date,
                    'inex': inex,
                    'price': price,
                    'detail': detail
                }
                if os.path.exists(self.filename):
                    with open(self.filename, 'r', encoding='utf-8') as f:
                        self.data = json.load(f)
                else:
                    self.data = defaultdict(list)

                try:
                    self.data[date].append(transaction)
                except:
                    self.data[date] = []
                    self.data[date].append(transaction)

                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4, sort_keys=True)
            return render_template('index_result.html', context=self.data)

        @self.app.route('/accbook', methods=['GET'])
        def load_data():
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                # return render_template('index_home.html')

        #최대 지출 / 최대 수익 날짜 구하는 함수
        @self.app.route('/max_inex', methods=['GET', 'POST'])
        def max_inex():
            load_data()
            max_income = 0
            max_expense = 0
            max_income_date = []
            max_expense_date = []
            for date, transactions in self.data.items():
                max_date = date
                for transaction in transactions:
                    if transaction['inex'] == "1" and transaction['price'] >= max_income:
                        max_income = transaction['price']
                        max_income_date.append(datetime.strptime(max_date,"%Y-%m-%d"))
                    if transaction['inex'] == "2" and transaction['price'] >= max_expense:
                        max_expense = transaction['price']
                        max_expense_date.append(datetime.strptime(max_date,"%Y-%m-%d"))
            max_income_date = sorted(max_income_date)
            max_expense_date = sorted(max_expense_date)

            max_list = [max_income, max_income_date, max_expense, max_expense_date]
            return render_template('index_max_inex_result.html',
                               context=max_list)


        # 월별 지출 / 수익 합계 계산 함수
        @self.app.route('/monthly_sum', methods=['GET', 'POST'])
        def calculate_monthly_sum():
            monthly_stats = defaultdict(lambda: {'sum_income': 0, 'sum_expense': 0,
                                                 'income_count':0, 'expense_count':0})
            for date, transactions in self.data.items():
                month = datetime.strptime(date, '%Y-%m-%d').month
                for transaction in transactions:
                    if transaction['inex'] == '1':
                        income = transaction['price']
                        monthly_stats[month]['sum_income'] += income
                        monthly_stats[month]['income_count'] += 1
                    if transaction['inex'] == '2':
                        expense = transaction['price']
                        monthly_stats[month]['sum_expense'] += expense
                        monthly_stats[month]['expense_count'] += 1

            return render_template("index_monthly_sum.html",
                                   context=monthly_stats)

        @self.app.template_filter('strftime')
        def format_datetime(date, fmt=None):
            if fmt is None:
                fmt = '%월 %일'
            return date.strftime(fmt)

        @self.app.template_filter('format_number')  # 추가된 부분
        def format_number(value):  # 추가된 부분
            return f"{value:,.0f}"


        # 잔액 변동량 구하기
        @self.app.route('/view_balance', methods=['GET', 'POST'])
        def balance_variance_plot():
            load_data()
            x = []
            y = []
            daily_balance = 0
            for date, transactions in self.data.items():
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                for transaction in transactions:
                    if transaction['inex'] == '1':
                        daily_balance += transaction['price']
                    if transaction['inex'] == '2':
                        daily_balance -= transaction['price']
                    x.append(date_obj)
                    y.append(daily_balance)
            sorted_pairs = sorted(zip(x, y))
            x, y = zip(*sorted_pairs)

            plt.figure(figsize=(10,6))
            plt.plot(x, y, marker='o', linestyle='-', label = 'Balance')
            plt.xlabel('날짜')
            plt.ylabel('잔액')
            # plt.title('잔액 변동량 그래프')
            plt.xticks(rotation=25)
            plt.legend()

            img = BytesIO()
            plt.savefig(img, format='png', dpi=200)
            img.seek(0)
            img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
            return render_template("index_balance_result.html",
                                   context=[x,y], img_data=img_base64)

    def show_result(self):
        return render_template('index_result.html')

    def run(self, port=5000):
        self.app.run(port=port)

# 예시 데이터 자동 생성 및 테스트

if __name__ == '__main__':
    book = AccountBook_App()
    book.run()
