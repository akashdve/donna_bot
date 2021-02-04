import requests
from bs4 import BeautifulSoup

from constants import COLLEGE_UPDATES_TEMPLATE


def fetch_rss_feed(source):
    try:
        r = requests.get(source)
        print(r.status_code)
        soup = BeautifulSoup(r.content, features="xml")
        articles = soup.find_all('item')

        article_list = []
        for a in articles:
            try:
                title = a.find('title').text
            except:
                title = "Not found"
            try:
                description = a.find('description').text
            except:
                description = "Not found"
            try:
                link = a.find('link').text
            except:
                link = "Not found"
            try:
                published_on = a.find('pubDate').text
            except Exception as e:
                print(e)
                published_on = "Not found"

            article = {
                'title': title,
                'description': description,
                'link': link,
                'published_on': published_on
            }
            article_list += [article]

        return r.status_code, article_list

    except Exception as e:
        print("Error while fetching feed from Centennial College.",e)
        return 500, []


def get_college_updates(source_url, n_updates=1) -> str:
    status, data = fetch_rss_feed(source=source_url)
    updates = ""
    if status == 200 and len(data) > 0:
        filtered_data = data[-n_updates:]
        filtered_data.reverse()
        for d in filtered_data:
            updates = updates + COLLEGE_UPDATES_TEMPLATE.format(d["published_on"], d["title"], d["description"], d["link"])
        return updates
    else:
        return updates
