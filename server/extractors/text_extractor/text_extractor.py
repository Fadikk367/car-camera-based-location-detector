import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt
from imutils.object_detection import non_max_suppression
from langdetect import detect_langs
from easyocr import Reader

model = "extractors/text_extractor/model/frozen_east_text_detection.pb"
STANDARD_WIDTH = 320
STANDARD_HEIGHT = 320
CONF_THRESHOLD = 0.01

def extract_text_from_image(image):
    orig = image.copy()

    (image, ratioW, ratioH) = prepare_image(image)
    (scores, geometry) = prepare_net(image)
    (boxes, confidences) = predictions(scores, geometry, CONF_THRESHOLD)
    boxes = non_max_suppression(np.array(boxes), confidences)
    #indices = cv2.dnn.NMSBoxesRotated(boxes, confidences, CONF_THRESHOLD, 0.4)
    text = recognize_text(orig, boxes, ratioW, ratioH)
    return detect_language(text), text

def prepare_image(image):
    (origH, origW) = image.shape[:2]
    (newW, newH) = (STANDARD_WIDTH, STANDARD_HEIGHT)
    ratioW = origW / float(newW)
    ratioH = origH / float(newH)

    image = cv2.resize(image, (newW, newH))
    return (image, ratioW, ratioH)

def prepare_net(image):
    blob = cv2.dnn.blobFromImage(image, 1.0, (STANDARD_WIDTH, STANDARD_HEIGHT), (123.68, 116.78, 103.94), True, False)
    net = cv2.dnn.readNet(model)

    outputLayers = []
    outputLayers.append("feature_fusion/Conv_7/Sigmoid")
    outputLayers.append("feature_fusion/concat_3")

    net.setInput(blob)
    (scores, geometry) = net.forward(outputLayers)

    return (scores, geometry)

def predictions(scores, geometry, confThreshold):
	(numR, numC) = scores.shape[2:4]
	boxes = []
	confidence_val = []

	for y in range(0, numR):
		scoresData = scores[0, 0, y]
		x0 = geometry[0, 0, y]
		x1 = geometry[0, 1, y]
		x2 = geometry[0, 2, y]
		x3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		for i in range(0, numC):
			if scoresData[i] < confThreshold:
				continue

			(offX, offY) = (i * 4.0, y * 4.0)

			angle = anglesData[i]
			cos = np.cos(angle)
			sin = np.sin(angle)

			h = x0[i] + x2[i]
			w = x1[i] + x3[i]

			endX = int(offX + (cos * x1[i]) + (sin * x2[i]))
			endY = int(offY - (sin * x1[i]) + (cos * x2[i]))
			startX = int(endX - w)
			startY = int(endY - h)

			boxes.append((startX, startY, endX, endY))
			confidence_val.append(scoresData[i])

	return (boxes, confidence_val)

def recognize_text(orig, boxes, ratioW, ratioH):
    results = []

    pytesseract.pytesseract.tesseract_cmd = (
        r'/usr/bin/tesseract'
    )

    i = 1
    for (startX, startY, endX, endY) in boxes:
        offset = 3
        startX = int((startX-offset) * ratioW)
        startY = int((startY-offset) * ratioH)
        endX = int((endX+offset) * ratioW)
        endY = int((endY+offset) * ratioH)

        try:
            r = orig[startY:endY, startX:endX]
            r = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)

            plt.subplot(len(boxes), 1, i)
            plt.imshow(r, 'gray')
            i += 1

            text = pytesseract.image_to_string(r, config='--oem 1 --psm 8')
            text = text[:len(text)-2]
            results.append(text)
            #print(detect_langs(text))
        except Exception as e:
            print(e)
    
    #print(results)
    return results


def extract_text_easyocr(img, reader):
  text = reader.readtext(img, detail = 0)
  return detect_language(text), text

def detect_language(text):
  #print(text)
  text_concat = ""
  for t in text:
    text_concat += t
  try:
    res = detect_langs(text_concat)
    #print(res, '\n')
    return res
  except Exception as e:
    #print(e)
    return ""

def extract_all(img):
    langs = ['ch_sim', 'ar', 'ja', 'uk']
    result = []
    result.append(extract_text_from_image(img))
    for l in langs:
        result.append(extract_text_easyocr(img, Reader(['en', l])))
    return result