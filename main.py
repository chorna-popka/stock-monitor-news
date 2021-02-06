from api_connector import Connector
from mail_engine import MailEngine
from api_keys import api_keys


STOCK = "GME"
COMPANY_NAME = "Game Stop"
compare_by = "4. close"

params_alpha = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": api_keys["a"],
}

params_news = {
    "q": COMPANY_NAME,
    "apikey": api_keys["b"],
}


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_change_pct(values):
    pct_change = float(values[0]) / float(values[1]) - 1
    return pct_change


def get_stock_change():
    conn = Connector(url="https://www.alphavantage.co/query", params=params_alpha)
    api_data = conn.get_json()

    # get only data for two dates that tuple contains into a list of dictionaries
    to_compare = [value for (key, value) in api_data["Time Series (Daily)"].items()]

    yesterday = to_compare[0][compare_by]
    day_before = to_compare[1][compare_by]
    return get_change_pct([yesterday, day_before])


def create_news_text():
    conn = Connector(url="http://newsapi.org/v2/top-headlines", params=params_news)
    api_data = conn.get_json()

    news = api_data["articles"][:3]
    news_text = ""
    for n in news:
        date_string = f"" \
                      f"{n['publishedAt'].split('T')[0][8:10]}." \
                      f"{n['publishedAt'].split('T')[0][5:7]}." \
                      f"{n['publishedAt'].split('T')[0][0:4]} " \
                      f"{n['publishedAt'].split('T')[1][0:8]}"
        news_text += f"{n['source']['name']}: {n['title']}\n{n['description']}\n{n['url']}\n{date_string}\n\n"

    return news_text


delta = get_stock_change()
if delta > 0.05:
    header = "🟢{:.2%}".format(delta)
elif delta < -0.05:
    header = "🔻{:.2%}".format(delta)
else:
    print("No major fluctuations today")
    exit(0)

subject = f"{STOCK}: {header}"
mail = MailEngine()
mail.send_email(to="kalbust@gmail.com", subject=subject, body=create_news_text())



