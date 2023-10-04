import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Stock"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "143P6EZSCWLKFEH0"
NEWS_API_KEY = "e06f754c8e8449449c9fe23b2c089d28"
TWILIO_SID = "AC0dcc2dbb26a478e123a8d2edef64a755"

TWILIO_AUTH_TOKEN = "536217d22744f901aed7e190494108d1"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,

}

response = requests.get(STOCK_ENDPOINT, params=stock_params)

data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]

yesterday_data_closing_price = data_list[0]["4. close"]

print(yesterday_data_closing_price)

day_before_yesterday_closing_price = data_list[1]["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_data_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_data_closing_price)) * 100)
print(diff_percent, "percent diff")

if abs(diff_percent) > .1:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)

    printed_articles = articles[:25]
    print(printed_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent} %\n Headline: {article['title']}. \nBrief: {article['description']}" for article in
                          printed_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18662612919",
            to="+15123580349"
        )
