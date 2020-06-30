import redis
import multiscript_config as msc
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from sklearn.preprocessing import StandardScaler

#To avoid getting dataconverstion warnings
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

def getdata(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    driver.get(url)
    driver.execute_script(open("js/jquery-3.5.1.js").read())
    js_info = driver.execute_script(open("js/js_mc_nc.js").read(), msc.AVG_READ_SPEED)

    url_info_df = pd.DataFrame(js_info, columns = ["content", "tag", "awordlength", "noofwords", "avgwordlength", "avgsentencelength", "linkdensity", 
            "fontSize", "fontWeight", "left", "top", "width", "height", "text", "atext"]) 
    cleanData(url_info_df)

def cleanData(url_info_df):
    global scaled_df, text_list, meta_titles, meta_info
    meta_titles = (url_info_df.iloc[[0, 1, 2, 3, -1]]["atext"]).to_list()
    meta_info= (url_info_df.iloc[[0, 1, 2, 3, -1]]["text"]).to_list()
    url_info_df = url_info_df.drop([url_info_df.index[0] , url_info_df.index[1], url_info_df.index[2], url_info_df.index[3], url_info_df.index[-1]])
    text_list = url_info_df["text"].to_list()
    url_info_df = url_info_df.drop(['content', 'tag', 'text', 'atext'],axis=1)
    scaled_df = StandardScaler().fit_transform(url_info_df).tolist()

def main(url):
    getdata(url)
    return scaled_df, text_list, meta_titles, meta_info