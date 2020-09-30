import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get('https://br.investing.com/currencies/usd-brl')
    ele = driver.find_element(By.ID, 'last_last').text

print(ele)

now = datetime.now()

text = f"Hoje, {now.strftime('%d/%m/%Y')} às {now.strftime('%H:%M')}, o valor do dólar está em R${ele} reais.\n"
print(text)

desktop_dir = os.path.join(os.environ.get('PATH_TO_ONEDRIVE'), 'Área de Trabalho')
os.chdir(desktop_dir)

with open('dolar_real.txt', 'a+') as f:
    f.write(text)
