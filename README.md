# BuffScaner
Compares prices of buff.163.com with market.csgo.com .

## Introduction
This project was made to automate the price comparison of buff.163 with market.csgo.

## Usage
BuffScaner can:
- Compare price by item hash name.
- Automatically compare prices of a list of hash items.
- Automatically parse buff.163 market pages.
- Save and load analyzed items to .csv files.

## Setup
Install required packages:
```
$ python -m pip install urllib3
```
Fill config.txt:
- Set your market.csgo api key.
- Set buff.163 session cookie.

You can add .txt files of hashes to scan items of interest automatically. 
Item hashes you can get from https://raw.githubusercontent.com/ModestSerhat/buff163-ids/main/buffids.txt
Hash list .txt files should be saved in ```Scan lists``` folder.

Storage saves and loads .csv files from ```Storage saves``` folder.

## Work in progress
In the future, I plan to expand the functionality and provide a more user-friendly experience.
