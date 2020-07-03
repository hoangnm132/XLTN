import requests
import lxml.html
import constants


def get_content_by_category(category): 
    print('Fetching...')
    if category not in constants.categories: 
        raise Exception('Category not found.')

    cate_url = constants.host + '/' + category
    print(cate_url)
    response = requests.get(cate_url)
    tree = lxml.html.fromstring(response.text)
    article_urls = None
    try :
        article_urls = tree.xpath('//article[@class="list_news"]/h4[@class="title_news"]/a/@href')
        if len(article_urls) <= 0 :
            print('Case 2')
            raise IndexError('Not found')
    except IndexError : 
        try :
            article_urls = tree.xpath('//article[contains(@class,"list_item")]/div[@class="content_item"]/h2/a/@href')
            if len(article_urls) <= 0 :
                print('Case 3')
                raise Exception('Not found 2')
        except Exception :
            article_urls = tree.xpath('//article[contains(@class,"list_item")]/h2[@class="title_item"]/a/@href')

    

    return get_article_content(article_urls)


def get_article_content(article_urls):
    text_sections = []
    index = 0
    content = ''
    article_url = None
    while not content or not content.strip(): 
        article_url = article_urls[index]
        response = requests.get(article_url)
        tree = lxml.html.fromstring(response.text)
        
        try : 
            text_sections = tree.xpath('//section[contains(@class,"sidebar_1")]/article/p[@class="Normal"]')
            if len(text_sections) <= 0 : 
                raise Exception('Not found')
        except Exception : 
            text_sections = tree.xpath('//section[contains(@class,"sidebar_2")]//p[@class="Normal"]')
        
        content = '\n'.join([section.text for section in text_sections if section.text is not None])
        index = index + 1

    return content, article_url
