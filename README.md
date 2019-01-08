# autoMoodle

A Python script for automatically downloading all uploaded resources from Moodle, built for IIT Bombay students.

# Requirements

The script requires bs4, chrome webdriver and selenium, along with Python 3. Please ensure that the packages are correctly installed.

# Usage

The 'config.json' file should be updated as follows:
1. LDAP ID and password
2. Course codes should be inserted in the following format: ["AA 101", "BB 101", ...]
3. Base path should contain the path to the base folder
4. Set reset to True in case you want to wipe the directory and start afresh.
PLEASE NOTE THAT IT WILL DELETE THE ENTIRE FOLDER AND BUILD THE DIRECTORY FROM SCRATCH
