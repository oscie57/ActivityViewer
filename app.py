from flask import Flask, render_template, send_file
import json, requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)

def get_title_info(tid, type):

    match type:
        case "name":
            #return "Super Mario"
        
            url = f"https://ninja.wup.shop.nintendo.net/ninja/ws/titles/id_pair?title_id[]={tid}"
            data = requests.get(url, verify=False, cert="static/WIIU_WOOD_1_CERT.pem").text

            bs = BeautifulSoup(data, 'lxml')
            ns_uid = bs.find("ns_uid")
            
            if ns_uid is not None:
                url = f"https://samurai.wup.shop.nintendo.net/samurai/ws/GB/title/{ns_uid.text}/?shop_id=2"
                data = requests.get(url, verify=False, cert="static/WIIU_WOOD_1_CERT.pem").text

                bs = BeautifulSoup(data, 'lxml')

                name = bs.find("name")

                if name is not None:
                    return name.text
                else:
                    return "Unknown"
            else:
                return "Unknown"
        case "icon":
            return f"https://caramelkat.github.io/Nintendo-eShop-Title-DB/titles/{tid}/icon.jpg"
        case "code":
            #return "Super Mario"
        
            url = f"https://ninja.wup.shop.nintendo.net/ninja/ws/titles/id_pair?title_id[]={tid}"
            data = requests.get(url, verify=False, cert="static/WIIU_WOOD_1_CERT.pem").text

            bs = BeautifulSoup(data, 'lxml')
            ns_uid = bs.find("ns_uid")

            if ns_uid is not None:
                url = f"https://samurai.wup.shop.nintendo.net/samurai/ws/GB/title/{ns_uid.text}/?shop_id=2"
                data = requests.get(url, verify=False, cert="static/WIIU_WOOD_1_CERT.pem").text

                bs = BeautifulSoup(data, 'lxml')

                product_code = bs.find("product_code")

                if product_code is not None:
                    return product_code.text
                else:
                    return "Unknown"
            else:
                return "Unknown"
        case "rating":
            return f"https://caramelkat.github.io/Nintendo-eShop-Title-DB/titles/{tid}/rating.jpg"

    # https://caramelkat.github.io/Nintendo-eShop-Title-DB/

def convert_minutes(minutes):
    return f"{minutes // 60} hours, {minutes % 60} minutes"

def get_date(days):
    wiiu_day = datetime(2000, 1, 1)
    correct_day = wiiu_day + timedelta(days=days)
    formatted = correct_day.strftime("%A, %d %B %Y")

    return formatted

@app.route('/')
def main():
    with open('PlayStats.json', 'r') as f:
        PlayStats = json.load(f)

    entry_count = PlayStats['entry_count']
    entries = PlayStats['entries']

    return render_template('stats.html', get_title_name=get_title_info, convert_minutes=convert_minutes, getdate=get_date, count=entry_count, statslist=entries)

@app.route('/<cssfile>.css')
def css(cssfile):
    return send_file(f'static/style/{cssfile}.css')

@app.route('/fonts/<font>')
def font(font):
    return send_file(f'static/fonts/{font}')

@app.route('/icons/<icon>')
def icons(icon):
    return send_file(f'static/img/{icon}')

if __name__ == '__main__':
    app.run('127.0.0.1', 8080, debug=False)