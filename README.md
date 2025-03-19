# KLADR_station_matcher
## Description
This program is designed to address the issue of matching meteorological station names written in Latin script to the official Russian city registry (KLADR). Initially, station names were written in Latin, but due to the peculiarities of transliteration, they did not match their Russian equivalents properly. This led to the need for a solution that could transliterate these names to Cyrillic and, through fuzzy string matching, identify the closest city names from the KLADR registry.

The script employs Levenshtein distance (edit distance) to compare transliterated station names with unique city names from the KLADR database. Once a match is found, the program links the station names to the corresponding cities and retrieves the KLADR codes for those cities. This allows for an accurate update and association between the meteorological stations and their respective cities.

## Functional Description

The script follows these main steps:
1. **Database Connection**: Connects to an Oracle database using SQLAlchemy and Oracle's `oracledb` driver.
2. **Query Execution**: Executes SQL queries to retrieve city names from the `kladr` table and station names with `NULL` values in the `name` field from the `al_babkina_meteostanse_5` table.
3. **Transliteration**: Converts station names from Latin characters to Cyrillic using predefined transliteration rules.
4. **Exact Matching**: Matches transliterated station names to city names from the `kladr` table, and generates `UPDATE` statements for exact matches.
5. **Fuzzy Matching**: Uses fuzzy string matching to find the best possible matches for station names that were not exactly matched.
6. **Data Insertion**: Saves the processed station data with updated names into a new table `al_babkina_meteostanse_111`.
7. **CSV Export**: Exports the station data to a CSV file for further analysis or use.

## Input Structure

1. **Database Connection**:
   - `username`: Username for the Oracle database connection.
   - `password`: Password for the Oracle database connection.
   - `dsn`: Data Source Name (DSN) for connecting to the Oracle database.

2. **Predefined Transliteration Rules**: 
   - A dictionary that maps Latin letter combinations to their Cyrillic equivalents for transliterating station names.

3. **Tables**:
   - `kladr`: Contains the list of city names (and their actual dates).
   - `al_babkina_meteostanse_5`: Contains the station names (with some missing values for `name`).

## Technical Requirements

1. **Libraries**:
   - `SQLAlchemy`: For connecting to the Oracle database and executing SQL queries.
   - `pandas`: For data manipulation and handling SQL query results.
   - `oracledb`: Oracle database driver used by SQLAlchemy.
   - `fuzzywuzzy`: For performing fuzzy matching of station names to city names.
   - `re`: Regular expressions used for transliteration.

2. **Oracle Database**: The script connects to an Oracle database containing the `kladr` table (with city names) and the `al_babkina_meteostanse_5` table (with station names that need updating).

## Usage

1. Modify the `username`, `password`, and `dsn` values in the script to connect to your Oracle database.
2. Ensure that the database contains the `kladr` table (with city names) and the `al_babkina_meteostanse_5` table (with station names to be updated).
3. Run the script, which will:
   - Transliterating station names from Latin to Cyrillic.
   - Match station names to city names in the `kladr` table using both exact and fuzzy matching.
   - Generate SQL `UPDATE` statements to update the station names.
   - Insert the updated data into a new table `al_babkina_meteostanse_111`.
   - Export the processed data to a CSV file.

## Example Output

The script will print SQL `UPDATE` statements for stations with exact name matches. Additionally, it will apply fuzzy matching for stations where no exact match was found, using the `fuzzywuzzy` library. It will also export the processed station data into a CSV file, such as `station.csv`.

## Conclusion

This script helps automate the process of updating station names based on transliteration and matching with city names in the `kladr` table. The use of fuzzy matching allows for a more flexible and accurate update process, ensuring that even imperfectly matched station names are updated correctly. The processed data is saved back to the database and exported to a CSV file for further use.
