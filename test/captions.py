import sys
sys.path.append('.')

import webvtt
import googletrans

caption_file = webvtt.read(
    'video_dl/YsLJssA01b4-Smash Ultimate - Art of Falco.en.vtt')
translator = googletrans.Translator()

for caption in caption_file:
    print(caption.text)
    try:
        translated = translator.translate(caption.text, dest='zh-cn', src='en')
        print(translated.text)
        if translated._response.status_code == 429:
            raise ValueError('return 429')
    except Exception as e:
        print(e)
caption_file.save('video_dl/test.vtt')
