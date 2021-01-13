import sys
import re
import time
import tqdm

import pandas as pd

from selenium import webdriver

EXECUTABLE_PATH = './venv/lib/python3.8/site-packages/chromedriver_binary/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=EXECUTABLE_PATH, options=options)


def main(loadurl, txtfilenama, scroll=50):
    driver.get(loadurl)
    t = tqdm.tqdm(range(0, scroll))
    for _ in t:
        t.set_description('%d' % len(driver.find_elements_by_class_name('bch-c-box-movie')))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    ids = []
    for elem in driver.find_elements_by_class_name('bch-c-box-movie'):
        url = elem.find_element_by_tag_name('a').get_attribute('href')
        ids.append(re.search(r'\/([0-9]+)', url)[1])
    with open('%s.txt' % txtfilenama, 'w') as f:
        for id in ids:
            f.write('%s\n' % id)


if __name__ == '__main__':
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print('%sは2つ以上の引数が必要です' % sys.argv[0])
