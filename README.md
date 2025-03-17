# KLADR_station_matcher
## Description
This program is designed to address the issue of matching meteorological station names written in Latin script to the official Russian city registry (KLADR). Initially, station names were written in Latin, but due to the peculiarities of transliteration, they did not match their Russian equivalents properly. This led to the need for a solution that could transliterate these names to Cyrillic and, through fuzzy string matching, identify the closest city names from the KLADR registry.

The script employs Levenshtein distance (edit distance) to compare transliterated station names with unique city names from the KLADR database. Once a match is found, the program links the station names to the corresponding cities and retrieves the KLADR codes for those cities. This allows for an accurate update and association between the meteorological stations and their respective cities.

## Functional Description
The program performs the following steps:
1. Retrieves a list of distinct cities from the KLADR database that have the most recent actual date.
2. Retrieves a list of meteorological stations from the `al_babkina_meteostanse_5` table where the station names are missing.
3. Applies transliteration rules to convert station names from Latin to Cyrillic.
4. Uses fuzzy string matching to compare transliterated station names with the list of cities in the KLADR database.
5. Identifies the best matches for each station and updates the station's name field in the database.
6. Saves the results back to the database and optionally exports the data to a CSV file.

## How It Works
1. **Retrieving City Names:** The program queries the KLADR database to retrieve a list of all cities that have the latest actual date, ensuring only valid and up-to-date data is used.
2. **Transliterating Station Names:** The station names are first transliterated from Latin to Cyrillic using predefined transliteration rules, ensuring better matching with the city names.
3. **Fuzzy Matching:** The transliterated station names are then compared to the list of cities from the KLADR database using fuzzy matching techniques (Levenshtein distance, fuzzy string matching algorithms such as `fuzz.ratio`, `fuzz.token_sort_ratio`, and `fuzz.token_set_ratio`).
4. **Matching and Updating:** Once the best matches are found, the program updates the station names with the corresponding city names and retrieves the KLADR code for further reference.
5. **Saving Results:** The updated station data is saved back into the database, and the results are optionally exported to a CSV file for review.

## Input Structure
To run the program, the following parameters need to be provided:
1. Database credentials: Username, Password, Database DSN (Data Source Name).
2. Tables: `diasoft_test.kladr` for city data and `al_babkina_meteostanse_5` for meteorological station data.

## Technical Requirements
To run the program, the following are required:
1. Python 3.x
2. Installed libraries: `sqlalchemy`, `pandas`, `fuzzywuzzy`, `oracledb`, `re`, and `sys`.
3. Oracle Database with the following tables: `diasoft_test.kladr` (containing city names) and `al_babkina_meteostanse_5` (containing meteorological station names).

## Usage
1. Modify the database credentials (`username`, `password`, and `dsn`) to connect to your Oracle database.
2. Run the script, and it will:
   - Retrieve a list of city names from the KLADR database.
   - Transliterates station names from Latin to Cyrillic.
   - Perform fuzzy matching to find the closest matches between station names and cities.
   - Update the station names in the database with the matched city names.
   - Optionally export the data to a CSV file.

## Example Output
After running the script, the following output can be expected:
- A list of SQL `UPDATE` statements for the stations that were successfully matched to city names.
- The updated stations table, now with correct city names, optionally saved as a CSV file.
- The exported CSV will contain columns like `id_station`, `station`, `STATION_RU`, and `reestr` (matched city names).

## Conclusion
This tool efficiently matches meteorological station names, initially written in Latin, to their corresponding cities in the KLADR registry. It ensures the accurate linking of station data, improving the quality of the database by using transliteration and fuzzy matching techniques. The program helps automate the process of updating station names in the database and supports further data analysis and usage.
