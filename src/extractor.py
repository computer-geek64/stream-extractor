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