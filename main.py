"""
Phase 1: Extract the relevant data from the selected product page, capturing the following details:
product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax,
number_available, product_description, category, review_rating, image_url
After retrieving the data, save it to a CSV file using the above fields as column headers.
"""

import pandas
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
page = urlopen(url)  # open the url
html = page.read().decode("utf-8")  # read html as a string
soup = BeautifulSoup(html, "html.parser")  # create beautifulsoup object

# Extract Data

def find_the_tag_string(search_text, search_tag, search_next):
    search_field = soup.find(search_tag, string=search_text)
    search_field_value = search_field.find_next(search_next)
    search_field_value = search_field_value.string
    return search_field_value


# print(soup.get_text()) # get the whole page
product_page_url = page.geturl()

title = soup.title.string  # retrieve the string between the title tags
title = title.split("|")[0].strip()  # strips what's after the pipe
img_tag = soup.find("img", alt=title)  # Find the <img> tag with alt title
src_value = img_tag["src"]

# Locate the tags that match the specified search string and tag type
universal_product_code = find_the_tag_string("UPC", "th", "td")
price_excluding_tax = find_the_tag_string("Price (excl. tax)", "th", "td")
price_including_tax = find_the_tag_string("Price (incl. tax)", "th", "td")
number_available = find_the_tag_string("Availability", "th", "td")
product_description = find_the_tag_string("Product Description", "h2", "p")
category = find_the_tag_string("Books", "a", "a")

# Find the <p> tag with a class that starts with "star-rating"
star_rating_p = soup.find("p", class_="star-rating")
classes = star_rating_p["class"]
for class_name in classes:
    if class_name != "star-rating":
        review_rating = class_name + " stars"

# Transform Data

# Define headers
headers = [
    "Title",
    "Product page url",
    "Image url",
    "UPC",
    "Category",
    "Price (excl. tax)",
    "Price (incl. tax)",
    "Availability",
    "Product Description",
    "Rating",
]
df = pandas.DataFrame(
    [
        [
            title,
            product_page_url,
            src_value,
            universal_product_code,
            category,
            price_excluding_tax,
            price_including_tax,
            number_available,
            product_description,
            review_rating,
        ],
    ],
    columns=headers,
)

# Write the DataFrame to a CSV file
df.to_csv("product_page_data.csv", index=False)
print("CSV file has been created with the specified headers.")


# Load Data
