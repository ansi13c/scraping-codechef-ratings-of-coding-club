import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from set_tings import *
from urllib.parse import quote_plus

def search_api(query, pages=int(RESULT_COUNT/10)):
    results = []
    for i in range(0, pages):
        start = i*10+1
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            query=quote_plus(query),
            start=start
        )
        response = requests.get(url)
        data = response.json()
        results += data["items"]

    res_df = pd.DataFrame.from_dict(results)

    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    res_df = res_df[["link", "rank", "snippet", "title"]]

    return list(l for l in res_df["link"])


print(search_api("anshuman jayaprakash", 1)[0])

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("coding_club").sheet1

url = search_api("anshuman jayaprakash", 1)[0]
# user_name = "ansi13c"
# url = "https://www.codechef.com/users/" + user_name
res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")

rating_number = soup.select_one(".rating-number")
print(type(rating_number.getText()))
line = ["anshuman jayaprakash" , rating_number.getText()]
sheet.delete_row(2)
sheet.insert_row(line, 2)
