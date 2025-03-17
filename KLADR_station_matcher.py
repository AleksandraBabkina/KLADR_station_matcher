from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import pandas as pd
import sys
import oracledb
import re
from fuzzywuzzy import fuzz, process

# Display all rows when printing pandas DataFrame
pd.set_option('display.max_rows', None)

# Oracle DB version compatibility setting
oracledb.version = "8.3.0"
# Replace cx_Oracle with oracledb
sys.modules["cx_Oracle"] = oracledb

# Database connection configuration - DO NOT EDIT
username = 'username'
password = 'password'
dsn = 'dsn'

# Creating the connection string for SQLAlchemy
connection_string = f'oracle+cx_oracle://{username}:{password}@{dsn}'
engine = create_engine(connection_string)  # Creating SQLAlchemy engine

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()

# SQL query to get the list of distinct city names from KLADR table (latest actual date)
query = """
SELECT DISTINCT NAME FROM diasoft_test.kladr
WHERE ACTUALDATE = (SELECT MAX(ACTUALDATE) FROM diasoft_test.kladr)
"""

# Execute query and load results into DataFrame
all_city_RF = pd.read_sql_query(query, engine)
all_city_RF.head()  # Display the first few rows

# SQL query to get station IDs and names where name is NULL
query = """
SELECT DISTINCT a.id_station, a.station FROM al_babkina_meteostanse_5 a WHERE name IS NULL
"""

# Execute query and load results into DataFrame
station = pd.read_sql_query(query, engine)

# Close the database connection
engine.dispose()
station.head()  # Display first few rows

# Transliteration rules: Latin letters to Cyrillic equivalents
translit_rules = {
    'yaj': 'яй', 'ju': 'ю', 'kh': 'х', 'ij': 'ий', 'aja': 'ая', 'ja': 'я',
    'ts': 'ц', 'ch': 'ч', 'shch': 'щ', 'sh': 'ш', 'zh': 'ж', 'yu': 'ю',
    'ya': 'я', 'y': 'ы', 'e': 'э', "'": 'ь', 'a': 'а', 'b': 'б', 'v': 'в',
    'g': 'г', 'd': 'д', 'e': 'е', 'z': 'з', 'i': 'и', 'k': 'к', 'l': 'л',
    'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т',
    'u': 'у', 'f': 'ф', 'h': 'х', 'j': 'й'
}

# Function to transliterate station name from Latin to Cyrillic
def transliterate_station_name(station_name):
    station_name = station_name.lower()
    for latin, russian in translit_rules.items():
        station_name = re.sub(latin, russian, station_name)
    return station_name.title()

# Apply transliteration to station names
station['STATION_RU'] = station['station'].apply(transliterate_station_name)

# Check if transliterated station name matches a city in KLADR, else empty
station['reestr'] = station['STATION_RU'].apply(lambda x: x if x in all_city_RF['name'].values else '')

# Generate SQL UPDATE statements for matching stations
for index, row in station.iterrows():
    if row['reestr'] != '':
        print(f"UPDATE al_babkina_meteostanse_5 SET NAME = '{row['reestr']}' WHERE ID_STATION = {row['id_station']};")

# Fuzzy matching section: try to match station names to city names using fuzzy logic
station = station.assign(reestr='')  # Reset 'reestr' column

# Fuzzy match using default scorer
for index, row in station.iterrows():
    city_ru = row['STATION_RU']
    if isinstance(city_ru, str):
        match = process.extractOne(city_ru, all_city_RF['name'])
        if match:
            station.loc[index, 'reestr'] = match[0]

# Fuzzy match using token_sort_ratio
station = station.assign(reestr='')
for index, row in station.iterrows():
    city_ru = row['STATION_RU']
    if isinstance(city_ru, str):
        match = process.extractOne(city_ru, all_city_RF['name'], scorer=fuzz.token_sort_ratio)
        if match:
            station.loc[index, 'reestr'] = match[0]

# Fuzzy match using ratio
station = station.assign(reestr='')
for index, row in station.iterrows():
    city_ru = row['STATION_RU']
    if isinstance(city_ru, str):
        match = process.extractOne(city_ru, all_city_RF['name'], scorer=fuzz.ratio)
        if match:
            station.loc[index, 'reestr'] = match[0]

# Fuzzy match using token_set_ratio
station = station.assign(reestr='')
for index, row in station.iterrows():
    city_ru = row['STATION_RU']
    if isinstance(city_ru, str):
        match = process.extractOne(city_ru, all_city_RF['name'], scorer=fuzz.token_set_ratio)
        if match:
            station.loc[index, 'reestr'] = match[0]

# Save the processed station DataFrame to a new table
with session.begin():
    station.to_sql('al_babkina_meteostanse_111', engine, if_exists='append', index=False)
    session.commit()

# Close session
session.close()

# Export station data to CSV
station.to_csv(r'C:\Users\aleksandra.babkina\Desktop\station.csv', index=False)