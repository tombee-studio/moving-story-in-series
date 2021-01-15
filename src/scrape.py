import time
import tqdm
import re
import sys
import os
import glob

from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from static import COLUMNS

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

load_dotenv()

EXECUTABLE_PATH = os.getenv('CHROME_DRIVER_EXECUTABLE_PATH')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(executable_path=EXECUTABLE_PATH, options=options)
driver.set_page_load_timeout(15)
wait = WebDriverWait(driver, 10)


def get_episodes_num(elements):
    return len(elements)


def text_to_be_met_with_condition(driver, type, name, episode, pattern: re.Pattern):
    elem = driver.find_element(type, name)
    elem_text = elem.text
    match = re.match(pattern, elem_text)
    if match:
        return elem
    else:
        return False


def scrape(title_id, t):
    df = pd.DataFrame(columns=COLUMNS)

    driver.get('https://www.b-ch.com/titles/%s/' % title_id)
    title = re.search(r'([^|]+)\|', driver.title)[1]
    episodes_num = get_episodes_num(driver.find_element_by_id('bch-stories')
                                    .find_elements_by_class_name('bch-c-box-movie'))
    for episode in range(1, episodes_num + 1):
        t.set_description('%s %d/%d' % (title, episode, episodes_num))
        driver.get('https://www.b-ch.com/titles/%s/%s/' % (title_id, str(episode).zfill(3)))
        try:
            wait.until(lambda driver: text_to_be_met_with_condition(driver,
                                                                    By.CLASS_NAME,
                                                                    'bch-c-rating-plays__num',
                                                                    episode,
                                                                    re.compile('[0-9,]+')))
            txt = driver.find_element_by_class_name('bch-c-rating-plays__num').text.replace(',', '')
            rating_plays = int(txt)
            story_title = driver.find_element_by_class_name('bch-p-heading-mov__summary').text
            df = df.append(pd.DataFrame([[episode, story_title, rating_plays]], columns=COLUMNS))
        except TimeoutException as err:
            t.set_description('can\'t load %s. continue...' % title)
        time.sleep(5.0)
    df.to_excel('excel/%s.xlsx' % title_id)


def main(loadfile):
    files = list(map(lambda file: os.path.splitext(os.path.basename(file))[0], glob.glob('excel/*.xlsx')))
    with open(loadfile) as f:
        t = tqdm.tqdm(f.readlines())
        for line in t:
            title_id = line.strip()
            if title_id not in files:
                scrape(title_id=title_id, t=t)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('%sは1つ以上の引数が必要です' % sys.argv[0])
