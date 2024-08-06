"""
Phase 1: Extract the relevant data from the selected product page, capturing the following details:
product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax,
number_available, product_description, category, review_rating, image_url
After retrieving the data, save it to a CSV file using the above fields as column headers.
"""

import pandas
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url_img = "https://books.toscrape.com/"
product_page_url = "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"


page = requests.get(product_page_url)
soup = BeautifulSoup(page.content, "html.parser")

# Extract Data


def get_title(soup):
    """Extract and clean the title from the page."""
    # retrieve the string between the title tags and strips what's after the pipe
    title = soup.title.string.split("|")[0].strip()
    return title


def get_image_src(soup, title):
    """Find the image src based on the title's alt text."""
    img_tag = soup.find("img", alt=title)
    src_value = img_tag["src"]
    src_value = urljoin(base_url_img, src_value)
    return src_value


def find_the_tag_string(search_text, search_tag, search_next_tag):
    """Locate the sibling tag that matches the specified search text."""
    search_field = soup.find(search_tag, string=search_text)
    search_field_value = search_field.find_next(search_next_tag)
    search_field_value = search_field_value.string
    return search_field_value


def extract_star_rating(soup):
    """
    Extract the star rating from a <p> tag with a class that starts with "star-rating".
    """
    star_rating_p = soup.find("p", class_="star-rating")
    classes = star_rating_p["class"]
    for class_name in classes:
        if class_name != "star-rating":
            review_rating = class_name + " stars"
    return review_rating


def extract_product_info(soup):
    """Extract product information from the soup object."""
    title = get_title(soup)
    image_url = get_image_src(soup, title)
    universal_product_code = find_the_tag_string("UPC", "th", "td")
    price_excluding_tax = find_the_tag_string("Price (excl. tax)", "th", "td")
    price_including_tax = find_the_tag_string("Price (incl. tax)", "th", "td")
    number_available = find_the_tag_string("Availability", "th", "td")
    product_description = find_the_tag_string("Product Description", "h2", "p")
    category = find_the_tag_string("Books", "a", "a")
    star_rating = extract_star_rating(soup)

    return {
        "title": title,
        "product_page_url": product_page_url,
        "image_url": image_url,
        "universal_product_code": universal_product_code,
        "price_excluding_tax": price_excluding_tax,
        "price_including_tax": price_including_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "rating": star_rating,
    }


# Transform Data
products_data = []
# Extract product info and add to the list
product_info = extract_product_info(soup)
products_data.append(product_info)
# Convert the list of dictionaries into a pandas DataFrame
df = pandas.DataFrame(products_data)
# Write the DataFrame to a CSV file
df.to_csv("product_page_data.csv", index=False)
print("CSV file has been created.")

"""
Phase 2: Extract the relevant data from the selected category page, capturing the following details for each product:
product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax,
number_available, product_description, category, review_rating, image_url
After retrieving the data, save it to a CSV file using the above fields as column headers.
"""
# Phase 2 extract datqa for a category
# https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html
# https://books.toscrape.com/catalogue/category/books/fantasy_19/page-2.html
# https://books.toscrape.com/catalogue/category/books/fantasy_19/page-3.html
base_url_book = "https://books.toscrape.com/catalogue/"
category_books = (
    "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
)
category_page = requests.get(category_books)
soup = BeautifulSoup(category_page.content, "html.parser")
books = soup.find_all("div", class_="image_container")

# Extract all links within these containers
books_links = []
for book in books:
    link = book.find("a")
    if link and link.has_attr("href"):
        link = (link["href"])[9:]
        link = urljoin(base_url_book, link)  # tranform into urls
        books_links.append(link)


category_books_data = []

for link in books_links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    product_info = extract_product_info(soup)
    category_books_data.append(product_info)

df = pandas.DataFrame(category_books_data)
df.to_csv("category_pages_data.csv", index=False)
print("CSV file with Fantasy books info has been created.")
