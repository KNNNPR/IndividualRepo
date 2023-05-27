import requests
from bs4 import BeautifulSoup

url = "https://www.mirea.ru/schedule/"
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

result = soup.find("div", class_="schedule"). \
    find(string="Институт информационных технологий"). \
    find_parent("div"). \
    find_parent("div"). \
    findAll("a", class_="uk-link-toggle")  # получить ссылки
links = []
for link in result:
    links.append(link['href'])
# print(links)
# for x in links:
#     if result == links:  # среди всех ссылок найти нужную
#         f = open("file.xlsx", "wb")  # открываем файл для записи, в режиме wb
#         resp = requests.get(x)  # запрос по ссылке
#         f.write(resp.content)

