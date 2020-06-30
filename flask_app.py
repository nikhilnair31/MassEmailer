import redis
import spacy
import js2svm
import jsinfo
import spacy_tfidf
import spacy_freq
import multiscript_config as msc
from celery import Celery
from celery import group
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from youtube_search import YoutubeSearch

app = Flask(__name__)
app.config.from_object("multiscript_config")
celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
db = SQLAlchemy(app)
nlp = spacy.load("en_core_web_sm")

class Articles(db.Model):  
   id = db.Column('article_id', db.Integer, primary_key = True)  
   title = db.Column(db.String(200))
   author = db.Column(db.String(200))
   domain = db.Column(db.String(200))
   og_url = db.Column(db.String(200))
   avg_read_time = db.Column(db.String(200))
   article_text = db.Column(db.String(20000))
   keywords = db.Column(db.String(200))
   def __init__(self, title, author, domain, og_url, avg_read_time, article_text, keywords):
      self.title = title
      self.author = author
      self.domain = domain
      self.og_url = og_url
      self.avg_read_time = avg_read_time
      self.article_text = article_text
      self.keywords = keywords

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

@celery.task(name="flask_app.siteinfo")
def siteinfo(site):
   scaled_df, text_list, meta_titles, meta_info = jsinfo.get_site_data(site)
   final_article_text = js2svm.main(site, scaled_df, text_list, meta_titles, meta_info)
   final_keywords = spacy_tfidf.get_keyword(nlp, final_article_text)
   article = Articles(final_article_text[0], final_article_text[1], final_article_text[2], final_article_text[3],
                      final_article_text[4], final_article_text[5], final_keywords)  
   db.session.add(article)
   db.session.commit()
   print(f'final_article_text :\n{final_article_text[:5]}')
   print(f'final_keywords :\n{final_keywords}')
   return ' '.join([str(elem) for elem in final_article_text])+final_keywords

@app.route('/')
def input():
   return render_template('input.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      article_list = get_urls()
      jobs = group(siteinfo.s(url) for url in article_list[:-msc.ARTICLES_PER_SITE])
      result = jobs.apply_async()
      results = result.get()
      return '\t'.join([str(el) for el in results])

def get_urls():
   article_list = []
   analyticsvidhya_basesearch_url = msc.ANALYTICSVIDHYA_BASEURL
   mlmastery_basesearch_url = msc.MLMASTERY_BASEURL
   youtube_basesearch_url = msc.YOUTUBE_BASEURL
   wiki_basesearch_url = msc.WIKIPEDIA_BASEURL
   medium_basesearch_url = msc.MEDIUM_BASEURL
   keyword = request.form['keyword']
   # AnalyticsVidhya
   for n in keyword.split():
      analyticsvidhya_basesearch_url += '{}+'.format(n)
   driver.get(analyticsvidhya_basesearch_url)
   elems = driver.find_elements_by_xpath("//div[@class='row block-streams el-module-search']//a[@href]")
   for elem in elems[:msc.ARTICLES_PER_SITE]:
      article_list.append(elem.get_attribute("href"))
   # MLMastery
   for n in keyword.split():
      mlmastery_basesearch_url += '{}+'.format(n)
   driver.get(mlmastery_basesearch_url)
   elems = driver.find_elements_by_xpath("//section[@id='main']//a[@href]")
   for elem in elems[:msc.ARTICLES_PER_SITE]:
      article_list.append(elem.get_attribute("href"))
   # Medium
   for n in keyword.split():
      medium_basesearch_url += '{}%20'.format(n)
   driver.get(medium_basesearch_url)
   elems = driver.find_elements_by_xpath("//div[@class='postArticle-content']//a[@href]")
   for elem in elems[:msc.ARTICLES_PER_SITE]:
      # print(f'medium_basesearch_url :\n{elem.get_attribute("href")}')
      article_list.append(elem.get_attribute("href"))
   # Wiki
   for n in keyword.split():
      wiki_basesearch_url += '{}_'.format(n)
   article_list.append(wiki_basesearch_url)
   # Youtube
   results = YoutubeSearch(keyword, max_results=msc.ARTICLES_PER_SITE).to_dict()
   for item in results:
      full_url = youtube_basesearch_url+item['link']
      article_list.append(full_url)
   print(f'\narticle_list :\n{article_list}\n')
   return article_list

if __name__ == '__main__':
   #app.run(host="0.0.0.0")
   db.create_all()
   app.run(debug = True)