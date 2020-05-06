#!/usr/bin/python3
# extractor.py

import os
import config
from time import sleep
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def locate_stream(url, search_parameters=['.m3u8', '.mp4', '.mp3']):
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
    sleep(5)
    browser.close()
    server.stop()
    streams = []
    subtitles = []
    for entry in proxy.har['log']['entries']:
        for param in search_parameters:
            if param in entry['request']['url']:
                request = {'method': entry['request']['method'], 'url': entry['request']['url'], 'headers': {x['name']: x['value'] for x in entry['request']['headers']}}
                streams.append(request)
            elif '.vtt' in entry['request']['url'] or '.srt' in entry['request']['url'] or '.ass' in entry['request']['url']:
                request = {'method': entry['request']['method'], 'url': entry['request']['url'], 'headers': {x['name']: x['value'] for x in entry['request']['headers']}}
                subtitles.append(request)


locate_stream('https://fmovies.wtf/film/onward.pp2wj/2okj502')