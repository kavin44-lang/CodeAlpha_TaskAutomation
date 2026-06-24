import os
import shutil
import re
import urllib.request
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

def move_jpg_files():
    source_folder = input("Enter source folder path: ")
    destination_folder = input("Enter destination folder path: ")

    os.makedirs(destination_folder, exist_ok=True)

    count = 0
    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith(".jpg"):
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(destination_folder, file_name)

            shutil.move(source_path, destination_path)
            count += 1

    print(f"{count} JPG file(s) moved successfully!")

def extract_emails():
    input_file = input("Enter input text file name: ")
    output_file = input("Enter output file name: ")

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    emails = re.findall(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        text
    )

    with open(output_file, "w", encoding="utf-8") as file:
        for email in emails:
            file.write(email + "\n")

    print(f"{len(emails)} email(s) extracted and saved to {output_file}")

def scrape_webpage_title():
    url = input("Enter webpage URL: ")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No Title Found"

        with open("webpage_title.txt", "w", encoding="utf-8") as file:
            file.write(title)

        print("Title saved to webpage_title.txt")
        print("Title:", title)

    except Exception as e:
        print("Error:", e)

while True:
    print("\n===== TASK AUTOMATION MENU =====")
    print("1. Move JPG Files")
    print("2. Extract Email Addresses")
    print("3. Scrape Webpage Title")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        move_jpg_files()
    elif choice == "2":
        extract_emails()
    elif choice == "3":
        scrape_webpage_title()
    elif choice == "4":
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Please try again.")