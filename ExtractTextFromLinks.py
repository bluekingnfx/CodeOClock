import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class MITREExtractor:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def extract_text_data(self):
        body_element = self.driver.find_element(By.TAG_NAME, 'body')
        return body_element.text

    def extract_and_save(self, urls_file, output_file):
        with open(urls_file, 'r') as file:
            urls = [line.strip().split(': ')[1] for line in file if line.strip()]

        for url in urls:
            self.driver.get(url)
            time.sleep(2)  # Wait for the page to load
            page_text_data = self.extract_text_data()
            
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(f"URL: {url}\n")
                file.write(f"{page_text_data}\n\n")

        self.driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text data from a list of URLs.")
    parser.add_argument("urls_file", help="The file containing the list of URLs.")
    parser.add_argument("--output", default="extracted_text_data.txt", help="The output file to save the extracted data.")
    
    args = parser.parse_args()
    
    extractor = MITREExtractor()
    extractor.extract_and_save(args.urls_file, args.output)