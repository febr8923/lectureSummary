from pydub import AudioSegment

from multiprocessing import Pool


import whisper
from openai import OpenAI
from ffmpeg import FFmpeg

import videoprocessing.videotoaudio as videotoaudio
import videoprocessing.videoprocessing as videoprocessing
import videoprocessing.audiototext as audiototext
import videoprocessing.generate_promt as generate_promt

#file names
VIDEO_FILE = "input.mp4"
VIDEO_FILE_SLIDE = "video_slide.mp4"#creates a new video file only containing slides at this location
AUDIO_FILE = "videoaudio.mp3"#creates a new audio file at this location
TEXT_FILE = "text.txt"#creates transcription of audio file at this location
ANSWER_FILE = "answers.txt"#writes chatgpt answers into this file

#create audio file from video file
videotoaudio.toaudio(VIDEO_FILE, AUDIO_FILE)

#create slides from video file with timestamps of when slide changes
times = videoprocessing.find_slides(VIDEO_FILE, VIDEO_FILE_SLIDE)

print("finished video->audio, video->slides...\n")



#between each slide change look at audio and transcribe it: costs money :(
audio = AudioSegment.from_mp3(AUDIO_FILE)
for i in range(len(times) - 1):
    #start of the slide
    start = int(times[i] * 1000)

    #end of the slide
    end = int(times[i+1] * 1000)

    #if the time spoken for a slide is big enough
    if end-start > 1000:

        #generate cropped audio file between start and end
        seg = audio[start:end]
        seg.export(f"./audio_segments/{i}.mp3", format="mp3")

        #transcribe audio file
        #openai api (0.006/min -> 0.5 per lecture)
        spoken_text = audiototext.audiototext_api(f"./audio_segments/{i}.mp3", f"./text/{i}.txt")
        #local copy of model (slow but free)
        #spoken_text = audiototext.audiototext_local(f"./audio_segments/{i}.mp3", f"./text/{i}.txt")

        #get summary by chatgpt & write it into text file
        generate_promt.generate_answer(spoken_text, ANSWER_FILE, i)

#end = int(times[len(times) -1] * 1000)
#seg = audio[-end:]
#seg.export(f"./audio_segments/{len(times)-1}.mp3", format="mp3")
#audiototext.audiototext_api(f"./audio_segments/{len(times)-1}.mp3", f"./text/{len(times)-1}.txt")

#

