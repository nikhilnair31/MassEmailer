import psycopg2
import pandas as pd
import multiscript_config as msc
import boto.ses
from jinja2 import Environment, PackageLoader
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Email(object):
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None

    def _render(self, filename, fname, urls):
        template = env.get_template(filename)
        return template.render(name = fname, linklist = urls, image = 'static/image.png')

    def html(self, filename, name, urlist):
        self._html = self._render(filename, name, urlist)

    def send(self, from_addr=None):
        body = self._html
        if isinstance(self.to, str):
            self.to = [self.to]
        if not from_addr:
            from_addr = 'support@easemylearning.com'
        if not self._html and not self._text:
            raise Exception('You must provide a text or html body.')
        if not self._html:
            body = self._text
        connection = boto.ses.connect_to_region( msc.AWS_REGION,aws_access_key_id=msc.AWS_ACCESS_KEY, 
            aws_secret_access_key=msc.AWS_SECRET_KEY )
        return connection.send_email( from_addr, self.subject, None, self.to,
            text_body=self._text, html_body=self._html )

def getTagsofEmailsCombined(conn) :
    list_email_tag_strength = []
    cur = conn.cursor()
    cur.execute( """SELECT DISTINCT users.email, users.first_name
                    FROM ((strength_analysis INNER JOIN quiz_submissions ON strength_analysis.submission_id = quiz_submissions.id)
                    INNER JOIN users ON users.id = quiz_submissions.user_id)""" )
    for emailid in cur.fetchall() :
        dict_user = {}
        dict_user.__setitem__('email', emailid[0])
        dict_user.__setitem__('first_name', emailid[1])
        cur.execute("""SELECT DISTINCT strength_analysis.tag,  strength_analysis.strength
                        FROM ((users INNER JOIN quiz_submissions ON users.id = quiz_submissions.user_id)
                        INNER JOIN strength_analysis ON strength_analysis.submission_id = quiz_submissions.id) WHERE users.email = '{}'""".format(emailid[0]) )
        for tag in cur.fetchall() :
            dict_user.__setitem__(tag[0], tag[1])
        print(f'dict_user :\n{dict_user}')
        list_email_tag_strength.append(dict_user)
    return list_email_tag_strength

def get_urls(keyword):
    article_list = []
    wiki_basesearch_url = msc.WIKIPEDIA_BASEURL
    medium_basesearch_url = msc.MEDIUM_BASEURL
    youtube_basesearch_url = msc.YOUTUBE_BASEURL

    for n in keyword.split():                                    # Wiki
        wiki_basesearch_url += '{}_'.format(n)
    # print(f'Wiki : {wiki_basesearch_url}')
    article_list.append(wiki_basesearch_url)
   
    for n in keyword.split('-'):                                    # Medium
        medium_basesearch_url += '{}%20'.format(n)
    driver.get(medium_basesearch_url)
    elems = driver.find_elements_by_xpath("//div[@class='postArticle-content']//a[@href]")
    for elem in elems[:msc.ARTICLES_PER_SITE_MID]:
        article_list.append(elem.get_attribute("href"))

    for n in keyword.split('-'):                                    # Youtube
        youtube_basesearch_url += '{}+'.format(n)
    driver.get(youtube_basesearch_url)
    elems = driver.find_elements_by_xpath("//div[@id='title-wrapper']//a[@href]")
    for elem in elems[:msc.ARTICLES_PER_SITE_MID]:
        article_list.append(elem.get_attribute("href"))

    return article_list

def get_userdata():
    list_of_user_dicts = getTagsofEmailsCombined(conn)
    temp_dict = dict(list_of_user_dicts[0])
    del temp_dict['email'] 
    del temp_dict['first_name'] 
    sorted_temp = {k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1])}
    print(f'sorted_temp :\n{sorted_temp}\n')
    article_dict = {}
    for key in sorted_temp:
        article_dict[key] = get_urls(key)
    print(f'article_dict :\n{article_dict}\n')
    print(f'list_of_user_dicts :\n{list_of_user_dicts}\n')
    return article_dict, list_of_user_dicts

def final_url_list(article_dict, list_of_user_dicts):
    for user in list_of_user_dicts:
        email = user['email']
        first_name = user['first_name'] 
        del user['email'] 
        del user['first_name'] 
        mail = Email(to=email, subject='AWS SES Test')
        sorted_user_tags = {k: v for k, v in sorted(user.items(), key=lambda item: item[1])}
        print(f'sorted_user_tags :\n{sorted_user_tags}\n')
        url_list = []
        for key in sorted_user_tags:
            if -15 < sorted_user_tags[key] < -5:
                url_list.append(article_dict[key][:msc.ARTICLES_PER_SITE_MAX])
            elif -5 < sorted_user_tags[key] < 5:
                url_list.append(article_dict[key][:msc.ARTICLES_PER_SITE_MID])
            elif 5 < sorted_user_tags[key] < 15:
                url_list.append(article_dict[key][:msc.ARTICLES_PER_SITE_MIN])
        print(f'url_list : {url_list}\n')
        flat_url_list = [l for sublist in url_list for l in sublist]
        print(f'flat_url_list : {flat_url_list}\n')
        mail.html('email.html', first_name, flat_url_list)
        mail.send()

if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    env = Environment(loader=PackageLoader('sql_ses_url_email', 'templates'))
    conn = psycopg2.connect( host = msc.DB_URL, port = msc.DB_PORT, user = msc.DB_USERNAME,
        password = msc.DB_PASSWORD, database = msc.DB_NAME )
    cursor = conn.cursor()

    dict_of_urls_by_tags, list_of_user_dicts = get_userdata()
    final_url_list(dict_of_urls_by_tags, list_of_user_dicts) 