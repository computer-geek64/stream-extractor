#!/usr/bin/python3
# extractor.py

import os
import streams
import requests
import youtube_dl.utils


print('[-] Locating streams...', end='')
stream_sources, subtitle_sources = streams.locate('https://fmovies.wtf/film/insidious-chapter-2.zp2w/zl6q8kw')

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
    ext = 'mp4'
        youtube_dl_options = {
            'nocheckcertificate': True,
            'outtmpl': os.path.join(os.path.abspath(os.getcwd()), name + '.%(ext)s')
        }
        youtube_dl.utils.std_headers.update(stream_source['headers'])
        with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([stream_source['url']])
    print('[+] Extracted stream to \'' + name + '.' + ext + '\'')

if subtitle_source:
    # Download subtitle source
    response = requests.get(subtitle_source, verify=False)
    with open(os.path.join(os.path.abspath(os.getcwd()), name + ' Subtitles.' + subtitle_source['url'].split('?')[0]), 'wb') as file:
        file.write(response.content)
