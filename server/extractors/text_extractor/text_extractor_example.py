import cv2
from text_extractor import extract_all
import json

def get_frames_from_video(video_path):
    reader = cv2.VideoCapture(video_path)
    is_next_frame, frame = reader.read()
    frames = []
    while is_next_frame:
        frames.append(frame)
        is_next_frame, frame = reader.read()
    reader.release()
    return frames

if __name__ == "__main__":

    # images = ['china', 'china3', 'polska', 'ukraina', 'spain',
    # 'tanzania', 'japan2', 'arab', 'usa', 'instacart']
    
    # img = cv2.imread("images/" + images[4] + ".jpg")

    frames = get_frames_from_video('images/video-1522071144.mp4')

    result = extract_all(frames[0])
    print(result)
    # with open("data_file.json", "w") as write_file:
    #     json.dump(result, write_file)
    # print("\n\n")

