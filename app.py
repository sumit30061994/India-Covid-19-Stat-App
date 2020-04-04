from bs4 import BeautifulSoup
import requests
import csv
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)  # initialising the flask app with the name 'app'
@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content']
            covid_url = "https://www.grainmart.in/news/coronavirus-covd-19-live-cases-tracker-john-hopkins/"
            html_content = requests.get(covid_url).text
            soup = BeautifulSoup(html_content, "lxml")
            table_rows = soup.find_all("tr")
            df = pd.DataFrame(columns=['State', 'Total Cases', 'Active Cases', 'Total Deaths', 'Cured'])
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text.strip() for i in td]
                s = pd.Series(row, index=df.columns)
                df = df.append(s, ignore_index=True)
            df = df.drop([0, 1])
            df.set_index('State', inplace=True)
            data = df.loc[searchString]
            dict = {"Total Cases": data["Total Cases"],
                    "Active Cases": data["Active Cases"],
                    "Total Deaths": data["Total Deaths"],
                    "Cured": data["Cured"]}

            return render_template('res.html', data=dict)

        except Exception as e:
            #print('The Exception message is: ',e)
            return ("something is wrong")

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000