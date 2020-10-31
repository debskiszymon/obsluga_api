import json
import requests
import csv
from flask import Flask, render_template, request

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0]["rates"]

def write_to_csv():
    with open('rates.csv', mode='w', encoding='utf-8') as csv_file:
        header = [key for key in rates[0].keys()]
        writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
        writer.writeheader()
        writer.writerows(rates)

def codes():
    codes = [code['code'] for code in rates]
    return codes


app = Flask(__name__)

@app.route("/currency/", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        data = request.form
        currency = data.get('currency')
        amount = int(data.get('amount'))
        for i in rates:
            if currency == i['code']:
                ask = amount * i['ask']
        return f"{str(ask)} PLN"
      
    return render_template("main.html", codes=codes())


if __name__ == "__main__":
    app.run(debug=True)


