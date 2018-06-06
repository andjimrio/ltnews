import feedparser
from newspaper import Article

from news.service.feed_services import get_feed_by_link, create_feed, exists_feed_id_by_link
from news.service.section_services import create_section
from news.service.item_services import exists_item_by_link, create_item
from news.utility.python_utilities import redo_string, redo_date
from news.utility.web_utilities import clean_html, extract_img_html


def populate_rss(link, title_section, user_id):
    rss = feedparser.parse(link)

    if rss.entries:
        if exists_feed_id_by_link(link):
            feeder = get_feed_by_link(link)
        else:
            feeder = create_feed(title=rss.feed.get('title', ''),
                                 link_rss=link,
                                 link_web=rss.feed.get('link', ''),
                                 description=rss.feed.get('description', ''),
                                 language=rss.feed.get('language', ''),
                                 logo=redo_string(rss.feed, 'image', 'href'))[0]

        section = create_section(title_section, user_id)[0]
        feeder.sections.add(section)
        feeder.save()

        for post in rss.entries:
            if not exists_item_by_link(post.get('link', '')):
                __populate_item(post, feeder.id)

        return True
    else:
        return False


def update_feed(link, printer=False):
    cont = 0
    rss = feedparser.parse(link)
    feed_id = get_feed_by_link(link).id

    if printer:
        print("\t" + rss.feed['title'])

    for post in rss.entries:
        if not exists_item_by_link(post.get('link', '')):
            __populate_item(post, feed_id)

            if printer:
                cont += 1

    if printer:
        print('\t\tActualizadas ' + str(cont) + ' entradas.')


def get_article(link):
    """
    Nos da el objeto Article dado una dirección web

    :param link: url de la noticia
    :return: Article de la noticia
    """
    article = Article(link)
    article.download()
    article.parse()
    return article


def __populate_item(post, feed_id):
    top_image = ''
    text = ''

    try:
        article = get_article(post.link)

        top_image = article.top_image
        text = article.text
    except Exception:
        print("ERROR-Article")
        print("\t" + post.title)
        print("\t" + post.link)

    if text == '':
        text = clean_html(post.get('description', ''))

    if top_image == '':
        top_image = extract_img_html(post.get('description', ''))

    item, created = create_item(title=post.get('title', ''),
                                link=post.get('link', ''),
                                description=post.get('description', ''),
                                image=top_image,
                                article=text,
                                creator=post.get('author', ''),
                                pubDate=redo_date(post, 'published'),
                                feed_id=feed_id)

    return item, created
