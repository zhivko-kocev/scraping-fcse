import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

data = []

for i in range(1, 201):
    for j in ["W", "S"]:
        for k in [1, 2, 3]:
            res = requests.get(f'https://www.finki.ukim.mk/subject/F23L{k}{j}{i:03}')

            bs = BeautifulSoup(res.text, "html.parser")

            table = bs.find_all("table")[0] if bs.find_all("table") else None

            if not table:
                continue

            rows = table.find_all_next("tr")

            title = tuple(rows[0].children)[5].find_next("b").text
            code = tuple(rows[1].children)[5].find_next("span").text

            tests = tuple(rows[19].children)[5].find_next("span").text[:3].strip()
            project = tuple(rows[20].children)[5].find_next("span").text[:3].strip()
            activities = tuple(rows[21].children)[5].find_next("span").text[:3].strip()
            final_exam = tuple(rows[22].children)[5].find_next("span").text[:3].strip()

            data.append([title, code, tests, project, activities, final_exam])
            print(f'Got the data for {title}')

print(len(data))

df = pd.DataFrame(data, columns=['Title', 'Code', 'Tests', 'Project', 'Activities', 'Final_Exam'])

df[['Tests', 'Project', 'Activities', 'Final_Exam']] = df[['Tests', 'Project', 'Activities', 'Final_Exam']].apply(
    pd.to_numeric, errors='coerce').fillna(0)

conn = sqlite3.connect('subjects.db')
df.to_sql('subjects', conn, if_exists='replace', index=False)
conn.close()

print("Data has been successfully saved to the database.")
