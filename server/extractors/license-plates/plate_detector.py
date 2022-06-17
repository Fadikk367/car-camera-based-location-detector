import cv2
from matplotlib import pyplot

def detectPlates(frame, cascade):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    plates = cascade.detectMultiScale(frame_gray)
    return plates

def getPlates(image):
    plates = []
    face_cascade = cv2.CascadeClassifier("images/test/haarcascade_russian_plate_number.xml")
    for plate in detectPlates(image, face_cascade):
        (x,y,w,h) = plate
        plates.append(image[y:y+h, x:x+w])
        cropX, cropY = int(w*0.1), int(h*0.1)
        plates.append(image[y+cropY:y+h-cropY, x+cropX:x+w-cropX])
        pyplot.imshow(cv2.cvtColor(image[y+cropY:y+h-cropY, x+cropX:x+w-cropX], cv2.COLOR_BGR2RGB))
        pyplot.show()
    return plates
