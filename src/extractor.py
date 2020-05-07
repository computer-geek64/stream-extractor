#!/usr/bin/python3
# extractor.py

import os
import sys
import streams
import requests
import warnings
import youtube_dl.utils


warnings.filterwarnings("ignore")

url = sys.argv[1] if len(sys.argv) > 1 else input('Enter the website URL: ')

print('[-] Locating streams...', end='')
stream_sources, subtitle_sources = streams.locate(url)
stream_sources = stream_sources[::-1]
subtitle_sources = subtitle_sources[::-1]

stream_source = None
if len(stream_sources) > 0:
    print('\r[+] Streams found:     ')
    for i in range(len(stream_sources)):
        print(str(i) + ': ' + stream_sources[i]['url'])

    selection = input('\nEnter a selection (default=0, n=none): ')
    if selection == '':
        stream_source = stream_sources[0]
    elif selection.isnumeric() and 0 <= int(selection) < len(stream_sources):
        stream_source = stream_sources[int(selection)]
else:
    print('\r[!] No streams found   ')

subtitle_source = None
if len(subtitle_sources) > 0:
    print('[+] Subtitles found:')
    for i in range(len(subtitle_sources)):
        print(str(i) + ': ' + subtitle_sources[i]['url'])

    selection = input('\nEnter a selection (default=0, n=none): ')
    if selection == '':
        subtitle_source = subtitle_sources[0]
    elif selection.isnumeric() and 0 <= int(selection) < len(subtitle_sources):
        subtitle_source = subtitle_sources[int(selection)]
else:
    print('[!] No subtitles found')

if stream_source or subtitle_source:
    name = input('Enter the stream name: ')

if stream_source:
    # Download stream source
    print('[-] Extracting stream...', end='')
    ext = stream_source['url'].split('?')[0].split('.')[-1]
    if ext == 'm3u8':
        print()
        ext = 'mp4'
        youtube_dl_options = {
            'nocheckcertificate': True,
            'outtmpl': os.path.join(os.path.abspath(os.getcwd()), name + '.%(ext)s')
        }
        youtube_dl.utils.std_headers.update(stream_source['headers'])
        with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([stream_source['url']])
    else:
        response = requests.get(stream_source['url'], verify=False)
        with open(os.path.join(os.path.abspath(os.getcwd()), name + '.' + ext), 'wb') as file:
            file.write(response.content)
    print('\r[+] Extracted stream to \'' + name + '.' + ext + '\'')

if subtitle_source:
    # Download subtitle source
    print('[-] Extracting subtitles...', end='')
    ext = subtitle_source['url'].split('?')[0].split('.')[-1]
    response = requests.get(subtitle_source['url'], verify=False)
    with open(os.path.join(os.path.abspath(os.getcwd()), name + ' Subtitles.' + ext), 'wb') as file:
        file.write(response.content)
    print('\r[+} Extracted subtitles to \'' + name + '.' + ext + '\'')
