import pandas as pd

# import datetime


class account_book:
    def __init__(self):
    def append_data(self):
        # today_data = {}
        date_input = input("Enter date(ex. 08/02) : ").split('/')
        io_input = input("Enter whether it's Income or Outcome : ")
        price_input = int(input("Enter its price : "))
        total_data = {
            "month": [],
            "day": [],
            "io": [],
            "price": []
        }
        self._month = date_input[0]
        self._day = date_input[1]
        self._io = io_input
        self._price = int(price_input)

        total_data["month"].append(self._month)
        total_data["day"].append(self._day)
        total_data["io"].append(self._io)
        total_data["price"].append(self._price)

        total_df = pd.DataFrame()
        total_df["month"] = total_data["month"]
        total_data["day"] = total_data["day"]
        total_data["io"] = total_data["io"]
        total_data["price"] = total_data["price"]
    def file_export(self):
        
    def cal_return(self):

