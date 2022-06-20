import cv2
from plates.plate_analyzer import predict_country_from_plate
from plates.plate_detector import getPlates

if __name__ == "__main__":
    image = cv2.imread("extractors/plates/test-images/romanian.png")
    for plate in getPlates(image):
        print(predict_country_from_plate(plate))

    image = cv2.imread("extractors/plates/test-images/gb.jpg")
    for plate in getPlates(image):
        print(predict_country_from_plate(plate))

    plate = cv2.imread("extractors/plates/test-images/paulo_sousa.png")
    print(predict_country_from_plate(plate))