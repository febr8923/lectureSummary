import whisper
from openai import OpenAI
import cv2
import numpy as np


#make audio file to text:: local whisper model
def audiototext_local(input_file, output_file):
    model = whisper.load_model("base")
    result = model.transcribe(input_file)

    # print the recognized text
    f = open(output_file, 'w')
    f.write(result["text"])
    f.close()
    return result["text"]


#make audio file to text:: open ai api
def audiototext_api(input_file, output_file):
    client = OpenAI()
    audio_file = open(input_file, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    f = open(output_file, 'w')
    f.write(transcript.text)
    f.close()
    return transcript.text
    #print(transcript.text)
