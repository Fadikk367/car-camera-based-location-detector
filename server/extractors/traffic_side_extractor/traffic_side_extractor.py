import cv2
import numpy as np
import csv
import math

# Implementation based on road lines recognition from: https://medium.com/analytics-vidhya/road-lane-detection-using-opencv-3e2d2740a4d

def region_of_interest(img,vertices): 
    mask = np.zeros_like(img)    
    match_mask_color=  255   #(255,) * channel_count
    cv2.fillPoly(mask,vertices,match_mask_color)
    masked_image=cv2.bitwise_and(img,mask) 
    return masked_image

def get_traffic_side_lists():
    left_side_list = []
    right_side_list = []
    
    with open("extractors/traffic_side_extractor/traffic_rules.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        counter = 1
        for line in reader:
            counter = counter + 1
            
            if counter == 1:
                continue
            else:
                if line[2] == 'YES':
                    right_side_list.append(line[0].lower())
                else:
                    left_side_list.append(line[0].lower())

    return left_side_list, right_side_list

LEFT_SIDE_LIST, RIGHT_SIDE_LIST = get_traffic_side_lists()

def return_estimated_countries(right_side_probability):
    # left_side_list, right_side_list = get_traffic_side_lists()
    threshold = 0.5
    
    if right_side_probability > threshold:
        return RIGHT_SIDE_LIST, right_side_probability
    else:
        return LEFT_SIDE_LIST, 1 - right_side_probability
    

def get_left_right_recognition(x, img_width):
    if x > img_width / 2.:
        return 0
    else:
        return 1

def get_probability(img,lines): 
    imge=np.copy(img)     
    blank_image=np.zeros((imge.shape[0],imge.shape[1],3), dtype=np.uint8)
    global_count = 0
    total_count = 0

    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                total_count += 1
                local_count = get_left_right_recognition(x1, image.shape[1])
                if y2 > y1:
                    local_count = get_left_right_recognition(x2, image.shape[1])

                cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),thickness=3)
                imge = cv2.addWeighted(imge,0.8,blank_image,1,0.0)
                
                global_count += local_count
            
    
    # return percantage of right-like lanes
    if(total_count == 0):
        return imge, 0
    return imge, global_count / total_count

def traffic_side_extractor(frame):
    image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    height=image.shape[0]
    width=image.shape[1]
    region_of_interest_coor=[(0,height),(0,400),(width/2,height/3), (width,height)]
    
    gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    canny_image = cv2.Canny(gray_image,100,200)
    
    cropped=region_of_interest(canny_image, np.array([region_of_interest_coor],np.int32))
    lines = cv2.HoughLinesP(cropped,rho=2,theta=np.pi/120,threshold=120,lines=np.array([]),minLineLength=100,maxLineGap=35)

    image, count = get_probability(image,lines)
    more_likely_countries, probability = return_estimated_countries(count)
    
    # uncomment for testing
    # cv2.imshow("Test", image)

    return more_likely_countries, probability

# if __name__ == '__main__':
#     image=cv2.imread('test_images/example_image_right_side.jpg')
#     countries, probability = traffic_side_extractor(frame=image)
