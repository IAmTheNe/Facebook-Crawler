# Import libraries and packages
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from time import sleep
from random import randint

import json

# 0. Some important variables
XPATH = {
    'more_comments': '//*[@id="m_story_permalink_view"]//div[@class="async_elem"]/a'
}

CLASS = {
    'comment_button': '_15kq',
    'comment_info': '_2b06'
}

data = dict()  # Store post & all comments information
list_comments = []  # Store all comments
i_comment = dict()  # Store a comment information (user, comment content, profile link)

# 1. Paste the Facebook post 's link
# url = input('Input Facebook post you want to crawler: ')
url = 'https://www.facebook.com/thaoo.nguyenn.16/posts/1517775055239799'

# Store some information
data['id'] = url.split('/')[-1]
data['link-post'] = url

# Use mobile version
url = url.replace('www.', '').replace('//facebook', '//mobile.facebook')

# 2. Setup
try:
    driver = webdriver.Edge("edgedriver_win64\msedgedriver.exe")
except WebDriverException:
    print('Please install Edge and download webdriver from http://go.microsoft.com/fwlink/?LinkId=619687')
    input('Press Enter to quit')
    quit()

# Login
driver.get('https://www.facebook.com/')
input('Login and press Enter to start crawler')

driver.get(url)

# 3. Find comment button
sleep(randint(1, 3))

try:
    comment_button = driver.find_element_by_class_name(CLASS['comment_button'])
    comment_button.click()
except NoSuchElementException:
    print('This post seems has no comment button')
    driver.close()

# 4. Check the post if it has more comments
while True:
    sleep(randint(1, 3))
    try:
        more_comments = driver.find_element_by_xpath(XPATH['more_comments'])
        print("Found more comments link:" +
              more_comments.get_attribute("href"))
        more_comments.click()
    except NoSuchElementException:
        break

# 5. Read comment
try:
    sleep(randint(1, 3))
    comment_info = driver.find_elements_by_class_name(CLASS['comment_info'])

    for cmt in comment_info:
        div = cmt.find_elements_by_tag_name('div')
        user = div[0].text
        profile = div[0].find_element_by_tag_name('a').get_attribute('href').replace(
            '//mobile.', '//www.').replace('?fref=nf&__tn__=R', '').replace('&fref=nf&__tn__=R', '')
        comment = div[1].text

        i_comment['user'] = user
        i_comment['profile'] = profile
        i_comment['comment'] = comment

        list_comments.append(i_comment.copy())

except NoSuchElementException:
    print('This post seems has no comments')

# 6. Export file
data['comments'] = list_comments

with open('{}.json'.format(data['id']), 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))

# 6. Close Edge
print('Crawler successfully! ')
driver.close()
