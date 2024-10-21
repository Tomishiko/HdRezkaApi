from HdRezkaApi import *
import os
import subprocess
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser(
                        prog='parser',
                        description='Streams from hdrezka.ag',
                        epilog='eat a dick')
    parser.add_argument('url')
    parser.add_argument('-e','--episode',help='which episode to play')
    parser.add_argument('-s','--season',help='which season to play')
    parser.add_argument('-q','--quality',help='quality of the video')
    parser.add_argument('-v','--voiceover',help='which voiceover/translation')
    parser.add_argument('-o','--output',help='output file name (if not specified extracted urls are not saved)')

    args = parser.parse_args()
    return args

def watch(rezka, args):
    #print('getting links')
    (links, isPlaylist ) = GetLinks(rezka,args.voiceover,args.season,args.episode,args.quality)
    #print('finished getting links',time.process_time())
    if args.output:
        try:
            os.mkdir('playlists')
        except Exception:
            pass
        f = open(f'playlists/{args.output}', "w",encoding='UTF-8')
        f.write(links)
        f.close()
        f = open (f'{args.output}.bat','w',encoding='UTF-8')
        f.write(f"@echo off\nstart %~dp0\\mpv\\mpv.exe --playlist=./playlists/{args.output}")
        print(f'File playlist saved at {os.path.abspath(f.name)}')
    else:
        if isPlaylist:
            subprocess.run(['./mpv/mpv.exe','--playlist=-'],input=links.encode('UTF-8'))
        else:
            subprocess.run(["./mpv/mpv.exe",links])


def GetLinks(rezka, voiceover,season={},episode={},quality='720p'):
    if quality == None:
        quality = '720p'
    if rezka.type == 'HdRezkaMovie':
        #print('get stream movie')
        #time.process_time()
        return (rezka.getStream(voiceover)[0],False)
    else:
        if episode:
            #print('get stream episode')
            #time.process_time()
            return (rezka.getStream(season,episode,voiceover),False)
        else:
            #print('get stream season')
            #time.process_time()
            params=''
            for i, stream in rezka.getSeasonStreams(season,voiceover):
                params += f"{stream(quality)[0]}\n"
            return (params,True)




def main():
    args = parse_args()
    rezka = HdRezkaApi(args.url)
    print(f"Extracting: {rezka.name}")
    watch(rezka,args)
    #params = ""

    # for i, stream in rezka.getSeasonStreams(args.season,args.voiceover):
    #     params += f"{stream(args.quality)[1]}\n"

    # if args.output:
    #     f = open(args.output, "w",encoding='UTF-8')
    #     f.write(params)
    #     f.close()
    # else:
    #     subprocess.run(["./mpv/mpv.exe","--playlist=-"],input=params.encode('UTF-8'))

if __name__ == '__main__': main()



