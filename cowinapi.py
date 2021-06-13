import requests
from datetime import datetime
import time

api_url_telegram = 'https://api.telegram.org/bot(write token no. of your bot here)/sendMessage?chat_id=@__groupid__&text='
base_cowin_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict'
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
group_id = 'vaccine_slots_dausa'


def fetch_data_from_cowin(district_id):
    flag=0
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    final_url = base_cowin_url+query_params
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)
    #print(response.text)

def extract_availability_data(response):
    response_json = response.json()
    for center in response_json["sessions"]:
        if center["available_capacity_dose1"] > 0 and center["min_age_limit"] == 45:
            message = "Pincode: {}\nPlace:{}\nSlots: {}\nMinimum age: {}\nVaccine: {}".format(
            center["pincode"], center["name"], center["available_capacity_dose1"]
            , center["min_age_limit"], center["vaccine"])
            flag=1
            send_message_telegram(message)
            #print(message)

def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace('__groupid__',group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)


if __name__ == "__main__":
    fetch_data_from_cowin(511)

while flag == 0:
    time.sleep(30)
    fetch_data_from_cowin(511)
