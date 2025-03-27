from ffmpeg import FFmpeg

#make audio file

def toaudio(input_name, output_name):
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(input_name)
        .output(output_name)
    )
    ffmpeg.execute()