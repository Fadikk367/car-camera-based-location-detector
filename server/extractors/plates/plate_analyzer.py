import cv2
import numpy as np
from plates.dominating_color import get_dominating_colors

def hsv_to_color(hsv):
    h, s, v = hsv

    if s < 40 and v > 128:
        return "WHITE"
    if (s < 40 and v < 128) or (s > 40 and v < 64):
        return "BLACK"

    if (h >= 0 and h < 20) or (h >= 170 and h <= 180):
        return "RED"
    elif h >= 20 and h < 35:
        return "YELLOW"
    elif h >= 35 and h < 85:
        return "GREEN"
    elif h >= 85 and h < 140:
        return "BLUE"
    elif h >= 150 and h < 160:
        return "PINK"

def predict_country_from_plate(plate):
    height, width, _ = np.shape(plate)

    # left strip:
    strip_len = width//10
    left_strip = plate[:, 0:strip_len]

    # right strip:
    right_strip = plate[:, width-strip_len:width]

    dominating_whole = hsv_to_color(get_dominating_colors(plate)[0])
    dominating_left = hsv_to_color(get_dominating_colors(left_strip)[0])
    dominating_right = hsv_to_color(get_dominating_colors(right_strip)[0])

    # print(dominating_left, dominating_whole, dominating_right)

    if dominating_whole == "YELLOW" and dominating_left == "BLUE":
        return ["nl", "lb"] # Netherlands
    elif dominating_whole == "YELLOW":
        return ["en", "he"] # UK/Israel
    elif dominating_whole == "WHITE" and dominating_left == "BLUE" and dominating_right == "RED":
        return ["nl"] # Belgium
    elif dominating_whole == "WHITE" and dominating_left == "BLUE" and dominating_right == "YELLOW":
        return ["pt"] # Portugal
    elif dominating_whole == "WHITE" and dominating_left == "YELLOW":
        return ["uk"] # Ukraine
    elif dominating_whole == "WHITE" and dominating_left == "RED":
        return ["sq"] # Albania
    elif (dominating_whole == "WHITE" or dominating_whole == "BLACK") and dominating_left == "BLUE":
        return ["bg", "bs", "cs", "da", "de", "el", "en", "es", "et", 
                "eu", "fi", "fr", "ga", "hr", "hu", "is", "lt", "lv",
                "mk", "mt", "no", "pl", "rm", "sk", "sr", "sv"] # Europe
    elif dominating_left  == "BLUE"  and dominating_right == "BLUE":
        return ["it"]
    elif dominating_whole == "GREEN" and dominating_left == "BLUE":
        return ["no"]
    elif (dominating_whole == "WHITE" or dominating_whole == "BLACK") and dominating_left == "WHITE" and dominating_right == "WHITE":
        return ["en", "ru"]
    else:
        return []

if __name__ == '__main__':
    img = cv2.imread('plates/gb_front.png')
    predicted = predict_country_from_plate(img)
    print(predicted)
    