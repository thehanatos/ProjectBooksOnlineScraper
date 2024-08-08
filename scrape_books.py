"""
Phase 1: Extract the relevant data from the selected product page, capturing the following details:
product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax,
number_available, product_description, category, review_rating, image_url
After retrieving the data, save it to a CSV file using the above fields as column headers.
"""
import os
import pandas
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse


# Extract Data

base_url_site = "https://books.toscrape.com/"
product_page_url = "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
base_url_book = "https://books.toscrape.com/catalogue/"
# Directory to save files
image_dir = "book_images"
csv_files_dir = "data"
# Create directory if it doesn't exist


def create_directories(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


create_directories(image_dir)
create_directories(csv_files_dir)


def save_csv_to_data_folder(df, filename):
    """
    Save the DataFrame to a CSV file in the 'data' folder.
    """
    file_path = os.path.join(csv_files_dir, filename)
    df.to_csv(file_path, index=False)
    print(f"CSV file has been created as '{file_path}'.")


def get_soup(url):
    """
    Fetch the content of the given URL and parse it into a BeautifulSoup object.
    """
    page = requests.get(url)
    page.raise_for_status()  # Raises an error if the request was unsuccessful
    soup = BeautifulSoup(page.content, "html.parser")
    soup.current_url = url  # Attach the URL to the soup object for later retrieval
    return soup


def get_url(url):
    """Returns the URL of the page being scraped from the soup object."""
    # In this case, the URL is already known, but we can simply return it
    return soup.current_url


soup = get_soup(product_page_url)


def get_title(soup):
    """Extract and clean the title from the page."""
    # retrieve the string between the title tags and strips what's after the pipe
    title = soup.title.string.split("|")[0].strip()
    return title


def get_image_src(soup, title):
    """Find the image src based on the title's alt text."""
    img_tag = soup.find("img", alt=title)
    src_value = img_tag["src"]
    src_value = urljoin(base_url_site, src_value)
    return src_value


def find_the_tag_string(soup, search_text, search_tag, search_next_tag):
    """Locate the sibling tag that matches the specified search text."""
    search_field = soup.find(search_tag, string=search_text)
    if search_field:
        search_field_value = search_field.find_next(search_next_tag)
        search_field_value = search_field_value.string
        return search_field_value
    else:
        return "Not found"


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
    product_page_url = get_url(soup)
    universal_product_code = find_the_tag_string(soup, "UPC", "th", "td")
    price_excluding_tax = find_the_tag_string(
        soup, "Price (excl. tax)", "th", "td")
    price_including_tax = find_the_tag_string(
        soup, "Price (incl. tax)", "th", "td")
    number_available = find_the_tag_string(soup, "Availability", "th", "td")
    product_description = find_the_tag_string(
        soup, "Product Description", "h2", "p")
    category = find_the_tag_string(soup, "Books", "a", "a")
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

book_data = []
# Extract product info and add to the list
product_info = extract_product_info(soup)
book_data.append(product_info)
# Convert the list of dictionaries into a pandas DataFrame
df = pandas.DataFrame(book_data)
# Write the DataFrame to a CSV file
filename = (str(get_title(soup)) + "_data.csv")
save_csv_to_data_folder(df, filename)

"""
Phase 2: Extract the relevant data from all the pages of the category.
"""

category_books = (
    "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
)


def clean_filename(filename):
    """
    Replace or remove special characters from filenames that are not allowed in file paths.
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)


def download_image(image_url, save_dir, image_name):
    """
    Download an image from a URL and save it to a specified directory.
    """
    # Clean the image name to avoid invalid characters
    cleaned_image_name = clean_filename(image_name)
    image_path = os.path.join(save_dir, cleaned_image_name)
    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        # Combines the directory path (save_dir) with the image filename to create a full file path.
        # Clean the image name to avoid invalid characters
        cleaned_image_name = clean_filename(image_name)
        image_path = os.path.join(save_dir, cleaned_image_name)
        # Opens the file at the specified image_path in binary write mode ('wb').
        # The with statement ensures that the file is properly closed after writing.
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved: {image_path}")
    else:
        print(f"Failed to download image: {image_url}")


def scrape_book_links_from_category(category_url):
    """
    Scrape all books from a given category page, including all subsequent pages.
    """
    books_links = []

    while category_url:
        # Fetch and parse the current category page
        soup = get_soup(category_url)

        # Find all book links on the current page
        books = soup.find_all("div", class_="image_container")
        for book in books:
            link = book.find("a")
            if link and link.has_attr("href"):
                link = (link["href"])[9:]
                full_link = urljoin(base_url_book, link)
                books_links.append(full_link)

        # Check for a "next" page
        next_button = soup.find("li", class_="next")
        if next_button:
            next_link = next_button.find("a")["href"]
            category_url = urljoin(category_url, next_link)
        else:
            category_url = None  # No more pages

    return books_links


def extract_books_data(books_links):
    """
    Extract product information for all books in the list of book links.
    """
    category_books_data = []

    for link in books_links:
        soup = get_soup(link)
        product_info = extract_product_info(soup)
        product_info['product_page_url'] = link  # Add the URL of the book page
        category_books_data.append(product_info)

        # Download the image and save it locally
        image_url = product_info['image_url']
        image_name = get_title(soup) + ".jpg"
        download_image(image_url, image_dir, image_name)

    return category_books_data


def generate_unique_filename(category_link):
    # Parse the URL
    parsed_url = urlparse(category_link)
    # Get the path part of the URL
    path = parsed_url.path
    # Extract the part of the path between "books/" and "/index.html"
    category_segment = path.split('books/')[1].split('/index.html')[0]
    filename = f"{category_segment}_books_data.csv"
    return filename


# Step 1: Scrape all book links from the category
all_books = scrape_book_links_from_category(category_books)
# Step 2: Extract product information for each book
category_books_data = extract_books_data(all_books)

df = pandas.DataFrame(category_books_data)
filename = generate_unique_filename(category_books)
save_csv_to_data_folder(df, filename)

"""
Phase 3: Extract the relevant data from all the pages of all the categorie.
"""
soup = get_soup(base_url_site)
categories_div = soup.find("div", class_="side_categories")
categories_div_links = categories_div.find_all("a")
# Remove the first link
categories_div_links = categories_div_links[1:]
category_links = []

# Get all category links
for cat_link in categories_div_links:
    if cat_link.has_attr("href"):
        full_link = urljoin(base_url_site, cat_link["href"])
        category_links.append(full_link)


for category_link in category_links:
    print(f"Scraping category: {category_link}")
    all_cat_books = scrape_book_links_from_category(category_link)
    category_books_data = extract_books_data(all_cat_books)
    # soup object passed as an argument to retrieve correct data
    for book_link in all_cat_books:
        book_soup = get_soup(book_link)
        product_info = extract_product_info(book_soup)
        category_books_data.append(product_info)
    # Convert the data to a DataFrame
    df = pandas.DataFrame(category_books_data)
    filename = generate_unique_filename(category_link)
    save_csv_to_data_folder(df, filename)
