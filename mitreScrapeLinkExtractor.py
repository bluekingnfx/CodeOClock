
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse

class MITREExtractor:
    def __init__(self, url, max_pages=1000):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)
        self.max_pages = max_pages
        self.page_count = 0
        self.base_domain = urlparse(url).netloc

    def extract_links(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        links = self.driver.find_elements(By.TAG_NAME, 'a')
        extracted_links = []
        for link in links:
            href = link.get_attribute('href')
            text = link.text
            if href and text and urlparse(href).netloc == self.base_domain:
                extracted_links.append(f"{text}: {href}")
        return extracted_links

    def extract_and_save(self, output_file):
        all_links = set()
        while self.page_count < self.max_pages:
            extracted_links = self.extract_links()
            new_links = set(extracted_links) - all_links
            all_links.update(new_links)
            
            with open(output_file, 'a', encoding='utf-8') as file:
                for link in new_links:
                    file.write(f"{link}\n")
            
            self.page_count += 1
            print(f"Processed page {self.page_count}, found {len(new_links)} new links")
            
            if self.page_count < self.max_pages:
                next_link = next((link for link in extracted_links if "next" in link.lower()), None)
                if next_link:
                    self.driver.get(next_link.split(": ")[1])
                    time.sleep(2)
                else:
                    print("No 'next' link found. Stopping extraction.")
                    break
        
        self.driver.quit()
        print(f"Extracted {len(all_links)} unique links from {self.page_count} pages.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract links from a website domain.")
    parser.add_argument("url", help="The URL of the website to extract links from.")
    parser.add_argument("--output", default="extracted_links.txt", help="The output file to save the extracted links.")
    parser.add_argument("--max_pages", type=int, default=20, help="The maximum number of pages to extract.")
    
    args = parser.parse_args()
    
    extractor = MITREExtractor(args.url, args.max_pages)
    extractor.extract_and_save(args.output)