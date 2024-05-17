import argparse
import csv
import json
import logging
import re
import os
from datetime import datetime

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, time
from bs4 import BeautifulSoup as BSoup
from urllib.parse import urljoin

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from json
with open("config.json") as f:
    config = json.load(f)


def validate_url(url):
    """ Validate the LinkedIn post URL using regex to ensure it matches expected format """
    pattern = re.compile("https://www.linkedin.com/posts/.+")
    return pattern.match(url)


def validate_config(config):
    """ Ensure all necessary configuration options are set """
    required_keys = ["name_class", "position_class", "linkedin_url_class", "comment_class",
                     "show_comments_class", "show_replies_class", "filename"]
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(f"Missing configuration for keys: {', '.join(missing_keys)}")
    logging.info("Configuration validated successfully")


# Login
def login(driver):
    """ Attempt to log in to LinkedIn using the provided email and password"""
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    if not email or not password:
        raise ValueError("LinkedIn credentials not set in environment variables")

    try:
        logging.info("Attempting to log in...")
        driver.get("https://www.linkedin.com/login")
        sleep(1)
        eml = driver.find_element(by=By.ID, value="username")
        eml.send_keys(email)
        passwd = driver.find_element(by=By.ID, value="password")
        passwd.send_keys(password)
        loginbutton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
        loginbutton.click()
        logging.info("Logged in successfully.")
        sleep(3)
    except Exception as e:
        logging.error(f"Failed to log in: {e}")
        raise


def show_more(target, target_class, driver):
    """ Click on the 'Show 10 more comments' or the "Load previous replies" buttons to load more comments or replies
    as specified"""
    logging.info(f"Attempting to load more {target}")
    try:
        load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, target_class)))
        action = ActionChains(driver)
        while True:
            action.move_to_element(load_more_button).click().perform()
            sleep(2)
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, target_class)))
            logging.info(f"Loading more {target}...")
    except Exception as e:
        logging.info(f"All {target} are loaded ")


def write2csv(file_path, names, positions, linkedin_urls, comments):
    """ Write scraped data to CSV """
    with open(file_path, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Current Position", "LinkedIn URL", "Comment"])
        for name, position, linkedin_url, comment in zip(names, positions, linkedin_urls, comments):
            writer.writerow([name, position, linkedin_url, comment])
        logging.info(f"Data written to {file_path} successfully.")


def extract_data(bs_obj):
    """
    Extract relevant data from a comment.

    Args:
    bs_obj (BeautifulSoup): The BeautifulSoup object containing the HTML of the page.

    Returns:
    tuple: A tuple containing lists of names, positions, LinkedIn URLs, and comments.
    """
    # Extract names: Finds all elements with the class specified in config for names.
    # It checks if there's a nested span with `aria-hidden="true"` which contains the actual name text.
    names = [
        name.find("span", {"aria-hidden": "true"}).get_text(strip=True)
        for name in bs_obj.find_all("span", {"class": config["name_class"]})
        if name.find("span", {"aria-hidden": "true"})
    ]

    # Extract positions: Finds all spans with a specific class and extracts their clean text content.
    positions = [
        position.get_text(strip=True) for position in
        bs_obj.find_all("span", {"class": config["position_class"]})
    ]

    # Extract LinkedIn URLs: Finds all anchor tags with a specific class, joins their href attribute
    # with the base LinkedIn URL to form absolute URLs.
    linkedin_urls = [
        urljoin("https://www.linkedin.com/", link['href']) for link in
        bs_obj.find_all("a", {"class": config["linkedin_url_class"]})
    ]

    # Extract comments: Finds all spans with a specific class and extracts their clean text content.
    comments = [
        comment.get_text(strip=True) for comment in
        bs_obj.find_all("span", {"class": config["comment_class"]})
    ]
    logging.info("Data extraction completed successfully.")
    return names, positions, linkedin_urls, comments


def scrape_comments(url):
    """
    Main function to initiate scraping process based on the given LinkedIn post URL, and writes scraped data to a CSV file.

    Args:
    url (str): The URL of the LinkedIn post to scrape.
    """

    # Initialize a new Chrome WebDriver session
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Validate the given URL with regex to ensure it is a LinkedIn post URL
    if validate_url(url):
        logging.info(f"URL validated successfully: {url}")
        start = time()  # Start timer to calculate execution time
        try:
            driver.maximize_window()  # Maximize browser window for consistent behavior

            # Login using credentials from environment variables
            login(driver)

            # Navigate to the specified post URL
            driver.get(url)

            # Expand all comments available
            show_more("comments", config["show_comments_class"], driver)

            # Expand all hidden replies available if the user has specified the -r flag
            if args.show_replies:
                show_more("hidden replies", config["show_replies_class"], driver)

            # Parse the current page source with BeautifulSoup
            bs_obj = BSoup(driver.page_source, "html.parser")

            # Extract relevant data using BeautifulSoup
            names, positions, linkedin_urls, comments = extract_data(bs_obj)

            # Write the scraped data to a csv file using the provided output filename
            if args.output:  # user specified output filename
                filename = args.output + ".csv"
            else:  # default output filename
                curr_time = datetime.now().strftime("-%m-%d-%Y--%H-%M")
                filename = config["filename"] + curr_time + ".csv"
            write2csv(filename, names, positions, linkedin_urls, comments)
        except WebDriverException as e:
            logging.error(f"WebDriver error occurred: {e}")
        finally:
            # Log the time taken to scrape
            end = time()
            logging.info(f"Script completed.  {len(comments)} comments scraped in: {int(end - start)} seconds")
    else:
        # Log an error if the URL does not validate
        logging.error("Invalid URL. Please enter a valid LinkedIn post URL.")

    # Ensure the driver is quit properly, closing the browser session
    driver.quit()


if __name__ == "__main__":
    logging.info("Starting LinkedIn scraping tool...")
    validate_config(config)

    parser = argparse.ArgumentParser(description="Linkedin Scraping.")
    parser.add_argument("-r", "--show-replies", dest="show_replies", action="store_true",
                        help="Load all replies to comments")
    parser.add_argument("-o", "--output", type=str, help="Output CSV file name")
    args = parser.parse_args()

    url = input("Enter LinkedIn post URL: ")
    scrape_comments(url)
