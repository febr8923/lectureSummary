import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim



def cmpimages(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err

def find_slides(input_file: object, output_file: object) -> []:

    # Open the original video
    cap = cv2.VideoCapture(input_file)

    # Original video's frame rate
    original_fps = cap.get(cv2.CAP_PROP_FPS)

    # Desired frame rate (new_fps < original_fps)
    new_fps = 1

    # Frame skipping rate
    skip_rate = round(original_fps / new_fps)

    frame_count = 0
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if there are no frames to read
        # only use every 'skip_rate'th frame
        if frame_count % skip_rate == 0:
            if frame_count > 1:
                frames.append(frame)
        frame_count += 1

    # Release everything when the job is finished
    cap.release()

    # Define the codec and create VideoWriter object + output Video properties
    #unnecessary of images of slides
   #fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # or use 'XVID' if saving as .avi
    #frame_width = int(cap.get(3))
    #frame_height = int(cap.get(4))
    #out = cv2.VideoWriter(output_file, fourcc, new_fps, (frame_width, frame_height))

    current_frame = [frames[0], 0]
    next_frame = [frames[0], 0]
    best_err = 0

    change_frame_times = []
    change_frames = []

    for i in range(len(frames)):
        err_to_cur = cmpimages(frames[i],current_frame[0])
        err_to_candidate = cmpimages(frames[i], next_frame[0])
        if err_to_cur > 2000:
            if err_to_candidate < 2000:
                if (err_to_cur > best_err):
                    next_frame[0] = frames[i]
                    next_frame[1] = i
            else:
                current_frame[0] = next_frame[0]
                current_frame[1] = next_frame[1]
                change_frame_times.append(current_frame[1])
                change_frames.append(current_frame[0])

                next_frame[0] = frames[i]
                next_frame[1] = i
                best_err = err_to_candidate
                #out.write(current_frame[0])

    #out.release()
    i=0
    for frame_change in change_frames:
        frame_filename = f"./images/{i}.png"
        cv2.imwrite(frame_filename, frame_change)
        print(frame_filename)
        i = i+1

    timestamps = []
    for frame_change_time in change_frame_times:
        timestamps.append((frame_change_time*skip_rate/original_fps))
    return timestamps


