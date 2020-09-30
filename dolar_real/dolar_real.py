"""
This short script makes use of the Selenium library to scrape a website and retrieve the
value of american Dollars in brazillian Reais.
Then, it appends a line to a file specifying the value and thedate and time that the value
was retrieved, with the help of the datetime standard library.
"""

import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

# Creates a driver for navigation
with webdriver.Chrome() as driver:
    # Goes to the desired website
    driver.get('https://br.investing.com/currencies/usd-brl')

    # Retrieves the text of the element with the id = 'last_last'
    ele = driver.find_element(By.ID, 'last_last').text

print(ele)

now = datetime.now()

# Builds text to be appended to file
text = f"Hoje, {now.strftime('%d/%m/%Y')} às {now.strftime('%H:%M')}, o valor do dólar está em R${ele} reais.\n"
print(text)

# Builds path to desktop
desktop_dir = os.path.join(os.environ.get('PATH_TO_ONEDRIVE'), 'Área de Trabalho')

# Changes working directory to Desktop
os.chdir(desktop_dir)

# Opens/creates a file to write the text in
with open('dolar_real.txt', 'a+') as f:
    f.write(text)
