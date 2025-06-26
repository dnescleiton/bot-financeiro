import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

BOT_TOKEN = "7613964313:AAHxNEi6jq-GhYXH9RNp72Ngl-nmc-2juzs"
CHAT_ID = "344816318"

def get_market_data():
    headers = {"User-Agent": "Mozilla/5.0"}

    # IBOV
    ibov_html = requests.get("https://br.investing.com/indices/bovespa", headers=headers).text
    ibov_soup = BeautifulSoup(ibov_html, "html.parser")
    try:
        ibov_price = ibov_soup.select_one('span[data-test="instrument-price-last"]').text.strip()
        ibov_var = ibov_soup.select_one('span[data-test="instrument-price-change-percent"]').text.strip()
    except AttributeError:
        ibov_price = "N/A"
        ibov_var = "N/A"

    # USD/BRL
    usd_html = requests.get("https://br.investing.com/currencies/usd-brl", headers=headers).text
    usd_soup = BeautifulSoup(usd_html, "html.parser")
    try:
        usd_price = usd_soup.select_one('span[data-test="instrument-price-last"]').text.strip()
        usd_var = usd_soup.select_one('span[data-test="instrument-price-change-percent"]').text.strip()
    except AttributeError:
        usd_price = "N/A"
        usd_var = "N/A"

    return ibov_price, ibov_var, usd_price, usd_var

def get_news():
    html = requests.get("https://g1.globo.com/economia/").text
    soup = BeautifulSoup(html, "html.parser")
    noticias = soup.find_all("a", class_="feed-post-link", limit=3)
    return [f"• {n.text.strip()}" for n in noticias]

def gerar_mensagem():
    data = datetime.now().strftime("%d/%m/%Y")
    ibov, ibov_var, usd, usd_var = get_market_data()
    noticias = get_news()
    noticias_txt = "\n".join(noticias)

    return f"""
📊 *Relatório Diário - Mini Índice e Dólar*
📅 *Data:* {data}

🇧🇷 *Mini Índice (IBOV)*  
- Cotação: {ibov} ({ibov_var})  
- Tendência: Técnica lateral com viés de alta

💵 *Dólar (USD/BRL)*  
- Cotação: {usd} ({usd_var})  
- Tendência: Influenciado por fluxo externo

📰 *Principais Notícias*  
{noticias_txt}
"""

def enviar_mensagem_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    res = requests.post(url, data=payload)
    print(res.text)
    return res.ok

# Executar uma vez ao rodar
mensagem = gerar_mensagem()
enviar_mensagem_telegram(mensagem)
