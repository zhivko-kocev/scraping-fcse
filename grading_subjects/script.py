import sqlite3

import pandas as pd

from .program_2023 import get_data_new

data = []

get_data_new(data)

df = pd.DataFrame(data, columns=['title', 'code', 'tests', 'project', 'activities', 'final_exam'])

df[['tests', 'code', 'activities', 'final_exam']] = df[['tests', 'project', 'activities', 'final_exam']].apply(
    pd.to_numeric, errors='coerce').fillna(0)

conn = sqlite3.connect('../data/grading_subjects.db')
df.to_sql('subjects', conn, if_exists='replace', index=False)
conn.close()

print("Data has been successfully saved to the database.")
