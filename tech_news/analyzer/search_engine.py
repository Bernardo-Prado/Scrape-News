from tech_news.database import find_news
from datetime import date
# https://docs.python.org/3/library/datetime.html


# Requisito 6
def search_by_title(title):
    db = find_news()
    filtered_news = list()
    for news in db:
        if news["title"].lower() == title.lower():
            filtered_news.append(news)
    return [(news["title"], news["url"]) for news in filtered_news]


# Requisito 7
def search_by_date(date2):
    try:
        date.fromisoformat(date2)
    except ValueError:
        raise ValueError("Data inválida")

    db = find_news()
    filtered_news = list()
    for news in db:
        if news["timestamp"].startswith(date2):
            filtered_news.append(news)
    return [(news["title"], news["url"]) for news in filtered_news]


# Requisito 8
def search_by_source(source):
    db = find_news()
    filtered_news = list()
    for news in db:
        for new in news["sources"]:
            if new.lower() == source.lower():
                filtered_news.append(news)
    return [(news["title"], news["url"]) for news in filtered_news]


# Requisito 9
def search_by_category(category):
    db = find_news()
    filtered_news = list()
    for news in db:
        for new in news["categories"]:
            if new.lower() == category.lower():
                filtered_news.append(news)
    return [(news["title"], news["url"]) for news in filtered_news]
