#!/usr/bin/python3
# extractor.py

import os
import sys
import m3u8
import streams
import requests
import warnings
from subprocess import Popen, PIPE

warnings.filterwarnings("ignore")


def progress_bar(percentage):
    chars = os.get_terminal_size().columns - 7
    equals = round(chars * percentage)
    spaces = chars - equals
    return '[' + '=' * (equals - 1) + ('>' if equals > 0 else '') + ' ' * spaces + '] ' + (str(round(percentage * 100)) + '%').rjust(4, ' ')


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
        response = requests.get(stream_source['url'], verify=False, headers=stream_source['headers']) if stream_source['method'].lower() == 'get' else requests.post(stream_source['url'], verify=False, headers=stream_source['headers'])
        m3u8_file = response.text

        m3u8_obj = m3u8.loads(m3u8_file)
        duration = sum(x.get('duration') for x in m3u8_obj.data.get('segments'))

        ts_files = m3u8_file.split('\n')

        if stream_source['url'].startswith('https://'):
            https = True
            base_url = 'https://' + stream_source['url'].replace('https://', '', 1).split('/')[0]
        else:
            https = False
            base_url = 'http://' + stream_source['url'].replace('http://', '', 1).split('/')[0]

        open(os.path.join(os.path.abspath(os.getcwd()), name + '.mp4'), 'w').close()

        progress = 0.0

        for i in range(len(ts_files)):
            if ts_files[i].startswith('#EXTINF'):
                progress += float(ts_files[i].split(':')[-1].replace(',', ''))
            elif ts_files[i].endswith('.ts'):

                print('\r' + progress_bar(progress / duration), end='')

                if ts_files[i].startswith('http://') or ts_files[i].startswith('https://'):
                    pass
                elif ts_files[i].startswith('/'):
                    ts_files[i] = os.path.join(base_url, ts_files[i][1:])
                else:
                    ts_files[i] = os.path.join(os.path.dirname(stream_source['url']), ts_files[i])

                response = requests.get(ts_files[i], verify=False, headers=stream_source['headers']) if stream_source['method'].lower() == 'get' else requests.post(ts_files[i], verify=False, headers=stream_source['headers'])
                if response.status_code == 200:
                    with open(os.path.join(os.path.abspath(os.getcwd()), '.' + name + '.ts'), 'wb') as file:
                        file.write(response.content)

                    Popen(['ffmpeg', '-i', 'concat:' + os.path.join(os.path.abspath(os.getcwd()), name + '.mp4') + '|' + os.path.join(os.path.abspath(os.getcwd()), '.' + name + '.ts'), '-codec', 'copy', os.path.join(os.path.abspath(os.getcwd()), '.' + name + '.mp4')], stdout=PIPE, stderr=PIPE).communicate()
                    os.rename(os.path.join(os.path.abspath(os.getcwd()), '.' + name + '.mp4'), os.path.join(os.path.abspath(os.getcwd()), name + '.mp4'))
                    os.remove(os.path.join(os.path.abspath(os.getcwd()), '.' + name + '.ts'))
    else:
        response = requests.get(stream_source['url'], verify=False, headers=stream_source['headers']) if stream_source['method'].lower() == 'get' else requests.post(stream_source['url'], verify=False, headers=stream_source['headers'])
        with open(os.path.join(os.path.abspath(os.getcwd()), name + '.' + ext), 'wb') as file:
            file.write(response.content)
    print('\r[+] Extracted stream to \'' + name + '.' + ext + '\'')

if subtitle_source:
    # Download subtitle source
    print('[-] Extracting subtitles...', end='')
    ext = subtitle_source['url'].split('?')[0].split('.')[-1]
    response = requests.get(subtitle_source['url'], verify=False, headers=subtitle_source['headers']) if subtitle_source['method'].lower() == 'get' else requests.post(subtitle_source['url'], verify=False, headers=subtitle_source['headers'])
    with open(os.path.join(os.path.abspath(os.getcwd()), name + ' Subtitles.' + ext), 'wb') as file:
        file.write(response.content)
    print('\r[+] Extracted subtitles to \'' + name + '.' + ext + '\'')
