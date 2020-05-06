#!/usr/bin/python3
# extractor.py

import streams


print('[-] Locating streams...', end='')
stream_sources, subtitle_sources = streams.locate('https://fmovies.wtf/film/onward.pp2wj/2okj502')

if len(stream_sources) > 0:
    print('\r[+] Streams found:     ')
    for i in range(len(stream_sources)):
        print(str(i) + ': ' + stream_sources[i]['url'])

    selection = input('\nEnter a selection (default=0, n=none): ')
    stream_source = None
    if not selection.isnumeric() or int(selection) < 0 or len(stream_sources) <= int(selection):
        stream_source = stream_sources[int(selection)]

if len(subtitle_sources) > 0:
    print('\r[+] Subtitles found:   ')
    for i in range(len(subtitle_sources)):
        print(str(i) + ': ' + subtitle_sources[i]['url'])

    selection = input('\nEnter a selection (default=0, n=none): ')
    subtitle_source = None
    if not selection.isnumeric() or int(selection) < 0 or len(subtitle_sources) <= int(selection):
        subtitle_source = subtitle_sources[int(selection)]
