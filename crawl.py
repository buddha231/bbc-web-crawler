from bs4 import BeautifulSoup
import requests
import re


def crawl_sub_categories(category_link, category_name):
    """ crawls the cat_link to return a list containing
    the links of different subcategories
    """

    html_doc = requests.get(category_link)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    """Find anker tags with /category_name because everysubcategory
    is /category_name/additional_path"""
    subcat = soup.find_all("a", {"href": re.compile(f"/{category_name}")})[:10]
    subcat = [i for i in subcat if i]

    def is_short(string): return bool(len(string.split("/")) == 3)
    def join_base(path): return category_link.split(category_name)[0][:-1]+path

    subcat1 = list()
    for i in subcat:
        url = join_base(i["href"])
        if is_short(i["href"]) and url not in subcat1:
            subcat1.append(url)

    return subcat1


def get_headlines(link):
    html_doc = requests.get(link)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    hey = soup.find_all("h3")
    headlines = []
    for h in hey[1:15]:
        headline = h.text.strip()
        if len(headline) > 3:
            # To remove short headline tags
            headlines.append(headline)
    return headlines
