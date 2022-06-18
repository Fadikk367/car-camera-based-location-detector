import cv2
import text_extractor as te

if __name__ == "__main__":

    images = ['china', 'china3', 'polska', 'ukraina', 'spain',
    'tanzania', 'japan2', 'arab', 'usa', 'instacart']
    
    for img in images:
        img = cv2.imread("images/" + img + ".jpg")
        print(te.extract_all(img))
        print("\n\n")