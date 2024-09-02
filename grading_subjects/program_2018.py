import requests
from bs4 import BeautifulSoup

req = requests.get(
    "https://www.finki.ukim.mk/mk/content/%D1%81%D0%BE%D1%84%D1%82%D0%B2%D0%B5%D1%80%D1%81%D0%BA%D0%BE-%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D1%81%D1%82%D0%B2%D0%BE-%D0%B8-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%81%D0%BA%D0%B8-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B8")

bs1 = BeautifulSoup(req.text, "html.parser")

anchors = bs1.select_one("#node-25348").find_all('a')[:-1]

links = []

for anchor in anchors:
    links.append(anchor['href'])

for link in links:
    req = requests.get("https://www.finki.ukim.mk"+link)
    bs2 = BeautifulSoup(req.text, "html.parser")
    tag = bs2.select_one(".file")
    pdf = tag.find_next('a')["href"]
    pdf_content = requests.get(pdf)
    with open("../pdfs_tmp/"+tag.text.strip(),"wb") as file:
        file.write(pdf_content.content)


