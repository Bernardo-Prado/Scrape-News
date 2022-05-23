import requests
import time
from parsel import Selector
from tech_news.database import create_news


def fetch(url):
    try:
        response = requests.get(url, timeout=4)
        response.raise_for_status()
        time.sleep(1)
    except (requests.HTTPError, requests.Timeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    news = selector.css(
        "div.tec--list__item a.tec--card__title__link::attr(href)"
    ).getall()
    return news


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page = selector.css(
        "a[href*='novidades?page=']::attr(href)"
    ).get()
    return next_page


# Requisito 4
def scrape_noticia(html_content):
    page = Selector(text=html_content)
    url = page.xpath("//meta[@property='og:url']/@content").get()
    title = page.xpath("//h1[@id='js-article-title']/text()").get()
    timestamp = page.xpath("//time[@id='js-article-date']/@datetime").get()
    writer = page.css(".tec--author__info *:first-child *::text").get()
    shares_count = page.xpath(
            "//div[@class='tec--toolbar__item']/text()"
        ).get()

    if not writer:
        writer = page.css(
            "div.tec--timestamp__item.z--font-bold a::text"
        ).get()

    if not shares_count:
        shares_count = 0

    else:
        number = [int(item) for item in shares_count.split() if item.isdigit()]
        shares_count = number[0]

    comments_count = int(
        page.xpath("//button[@class='tec--btn']/@data-count").get()
    )

    summaries = page.css(
        ".tec--article__body > p:first-child *::text"
    ).getall()
    summary = "".join(summaries)

    sources_itens = page.xpath(
        "//div[h2/text() = 'Fontes']/div/a/text()"
    ).getall()

    sources = [item.strip() for item in sources_itens]

    categories_itens = page.xpath(
        "//div[@id='js-categories']/a/text()"
    ).getall()

    categories = [item.strip() for item in categories_itens]

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer.strip() if writer else None,
        "shares_count": int(shares_count) if shares_count else 0,
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }


# Erick Marinho me ajudou nesse requisito 4
# Requisito 5
def get_tech_news(amount):
    novidades = list()
    url = "https://www.tecmundo.com.br/novidades"

    while len(novidades) < amount:
        html_content = fetch(url)
        novidades.extend(scrape_novidades(html_content))
        url = scrape_next_page_link(html_content)

    scrape = novidades[:amount]

    scraped_news = [scrape_noticia(fetch(news)) for news in scrape]
    create_news(scraped_news)

    return scraped_news
