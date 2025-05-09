from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time,os
import random

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).text

    except AttributeError:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available



# Function to build Amazon search URL dynamically
def build_amazon_search_url(search_term, page=1):
    search_term = search_term.replace(' ', '+')
    return f"https://www.amazon.in/s?k={search_term}&page={page}"

if __name__ == '__main__':

    # Set headers
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    })

    # 🔥 Input from user
    search_keyword = input("Enter product to search on Amazon: ").strip()
    total_pages = int(input("Enter number of pages to scrape: "))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    for page in range(1, total_pages + 1):
        print(f"Scraping Page {page}...")
        URL = build_amazon_search_url(search_keyword, page)
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", attrs={'class':'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})
        links_list = [link.get('href') for link in links]

        for link in links_list:
            product_url = "https://www.amazon.in" + link
            new_webpage = requests.get(product_url, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))

            time.sleep(random.uniform(1, 3))  # Random sleep

    # Save results
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])

    # Save file with dynamic name
    filename = f"./data/scrapped/amazon_{search_keyword}_data.xlsx"
    os.makedirs('./data/scrapped', exist_ok=True)
    amazon_df.to_excel(filename, index=False)

    print(f"\n✅ Scraping Completed. Saved {len(amazon_df)} products to {filename}")
