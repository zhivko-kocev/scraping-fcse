import os
import re
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

def get_data(data):
    req = requests.get(
        "https://www.finki.ukim.mk/mk/content/%D1%81%D0%BE%D1%84%D1%82%D0%B2%D0%B5%D1%80%D1%81%D0%BA%D0%BE-%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D1%81%D1%82%D0%B2%D0%BE-%D0%B8-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%81%D0%BA%D0%B8-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B8")
    bs1 = BeautifulSoup(req.text, "html.parser")

    anchors = bs1.select_one("#node-25348").find_all('a')[:-1]
    links = ["https://www.finki.ukim.mk" + anchor['href'] for anchor in anchors]

    for link in links:
        req = requests.get(link)
        bs2 = BeautifulSoup(req.text, "html.parser")
        tag = bs2.select_one(".file")
        if tag is None:
            continue
        pdf = tag.find_next('a')["href"]
        pdf_content = requests.get(pdf)
        with open("../pdfs_tmp/" + tag.text.strip(), "wb") as file:
            file.write(pdf_content.content)
        print("Wrote contents for: " + tag.text.strip())

    files = os.listdir("../pdfs_tmp")

    for file in files:
        if not file.endswith(".pdf"):
            continue

        reader = PdfReader("../pdfs_tmp/" + file)
        first_page_text = reader.pages[0].extract_text().strip()
        second_page_text = reader.pages[1].extract_text().strip()

        title_index = first_page_text.find("1.")
        code_index = first_page_text.find("F18")
        tests_index = second_page_text.find("17.1")
        project_index = second_page_text.find("17.2")
        activities_index = second_page_text.find("17.3")
        final_exam_index = second_page_text.find("17.4")

        title = first_page_text[title_index + 34:code_index].split("\n")[0].strip() + " - 2018 program"
        code = first_page_text[code_index:code_index + 10]

        tests = re.search(r'\b\d+\b', second_page_text[tests_index+4:project_index]).group() if re.search(r'\b\d+\b', second_page_text[tests_index+4:project_index]) else "N/A"
        project = re.search(r'\b\d+\b', second_page_text[project_index+4:activities_index]).group() if re.search(r'\b\d+\b', second_page_text[project_index+4:activities_index]) else "N/A"
        activities = re.search(r'\b\d+\b', second_page_text[activities_index+4:final_exam_index]).group() if re.search(r'\b\d+\b', second_page_text[activities_index+4:final_exam_index]) else "N/A"
        final_exam = re.search(r'\b\d+\b', second_page_text[final_exam_index+4:final_exam_index + 30]).group() if re.search(r'\b\d+\b', second_page_text[final_exam_index+4:final_exam_index + 30]) else "N/A"

        print("Title:", title)
        print("Code:", code)
        print("Tests:", tests)
        print("Project:", project)
        print("Activities:", activities)
        print("Final Exam:", final_exam)
        data.append([title, code, tests, project, activities, final_exam])

