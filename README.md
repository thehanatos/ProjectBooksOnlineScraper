### ProjectBooksOnlineScraper

This script is designed to scrape detailed information about books from an online bookstore. The script navigates through various book categories, extracts relevant data for each book, and saves the data to CSV files. Additionally, it downloads and saves images associated with each book.

#### Features

- **Category Scraping:** Automatically scrapes all book links from each category, including pagination.
- **Data Extraction:** Retrieves specific details about each book, including title, price, availability, description, and rating.
- **Image Downloading:** Downloads the cover image of each book and saves it locally.
- **CSV Export:** Saves the extracted book data to CSV files, with a separate file for each category.

#### Requirements

- Python 3.11.9
- Required Python libraries (install using `pip`):
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `os` (Standard Python library)
  - `urllib.parse` (Standard Python library)

#### Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:thehanatos/ProjectBooksOnlineScraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd ProjectBooksOnlineScraper
   ```

3. Create and activate the virtual env:

   ```bash
   python -m venv env
   source env/bin/activate
   ```

4. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

#### Usage

**Configure Base URL:**

- Update the `base_url_site` and `base_url_book` variables in the script to reflect the root URL of the site you are scraping.

**Run the Script:**

- Execute the script using Python:

  ```bash
  python scrape_books.py
  ```

**Data Output:**

- The script will create a CSV file for each category in the current working directory, named as `categoryname_books_data.csv`.
- Downloaded images will be saved in the `images` directory (created automatically).

#### Functions Overview

###### `get_soup(url)`

Fetches and parses the HTML content of the specified URL, returning a BeautifulSoup object for further manipulation.

###### `scrape_book_links_from_category(category_url)`

Scrapes all book links from the specified category, including paginated results.

###### `extract_product_info(soup)`

Extracts detailed information about a book from its product page.

###### `extract_books_data(books_links)`

Iterates over a list of book URLs, extracts information using `extract_product_info`, and returns a list of dictionaries with book data.

###### `download_image(image_url, save_dir, image_name)`

Downloads an image from a URL and saves it to a specified directory.

###### `generate_csv_filename(category_link)`

Generates a unique filename for the CSV based on the category link.

#### Folder Structure

```
├── scrape_books.py        # Main script for scraping
├── requirements.txt       # List of required libraries
├── README.md              # Project documentation
├── data/                  # Directory where CSV files are saved
└── images/                # Directory where images are saved
```

#### License

This project is licensed under the MIT License. See the LICENSE file for details.