#!/usr/bin/python3
# streams.py

import config
from time import sleep
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def locate(url, search_parameters=['.m3u8', '.mp4', '.mp3']):
    server = Server(config.BROWSERMOB_PROXY)
    server.start()
    proxy = server.create_proxy()
    options = Options()
    options.headless = config.HEADLESS
    profile = webdriver.FirefoxProfile(config.FIREFOX_PROFILE)
    selenium_proxy = proxy.selenium_proxy()
    profile.set_proxy(selenium_proxy)
    browser = webdriver.Firefox(firefox_profile=profile, options=options)
    proxy.new_har('source', options={'captureHeaders': True})
    browser.get(url)
    sleep(10)
    browser.close()
    server.stop()
    streams = []
    subtitles = []
    for entry in proxy.har['log']['entries']:
        for param in search_parameters:
            request = {'method': entry['request']['method'], 'url': entry['request']['url'], 'headers': {x['name']: x['value'] for x in entry['request']['headers']}}
            if param in entry['request']['url'].split('?')[0]:
                if request not in streams:
                    streams.append(request)
            elif '.vtt' in entry['request']['url'].split('?')[0] or '.srt' in entry['request']['url'].split('?')[0] or '.ass' in entry['request']['url'].split('?')[0]:
                if request not in subtitles:
                    subtitles.append(request)
    return (streams, subtitles)
