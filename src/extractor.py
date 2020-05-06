#!/usr/bin/python3
# extractor.py

import os
import streams
import youtube_dl


print('[-] Locating streams...', end='')
stream_sources, subtitle_sources = streams.locate('https://fmovies.wtf/film/onward.pp2wj/2okj502')

stream_source = None
if len(stream_sources) > 0:
    print('\r[+] Streams found:     ')
    for i in range(len(stream_sources)):
        print(str(i) + ': ' + stream_sources[i]['url'])

    selection = input('\nEnter a selection (default=0, n=none): ')
    if selection.isnumeric() and 0 <= int(selection) < len(stream_sources):
        stream_source = stream_sources[int(selection)]
else:
    print('\r[!] No streams found   ')

subtitle_source = None
if len(subtitle_sources) > 0:
    print('[+] Subtitles found:')
    for i in range(len(subtitle_sources)):
        print(str(i) + ': ' + subtitle_sources[i]['url'])

    selection = input('\nEnter a selection (default=0, n=none): ')
    if selection.isnumeric() and 0 <= int(selection) < len(subtitle_sources):
        subtitle_source = subtitle_sources[int(selection)]
else:
    print('[!] No subtitles found')


if stream_source:
    # Download stream source
    youtube_dl_options = {
        'nocheckcertificate': True,
        'addheader': stream_source['headers'],
        'outtmpl': os.path.join(os.path.abspath(os.getcwd()), 'stream.%(ext)s')
    }
    with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([stream_source['url']])

if subtitle_source:
    print(subtitle_source)
    pass  # Download subtitle source
