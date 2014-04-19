import cv2
import os, os.path
import sys

def detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier(sys.argv[1])
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def calculate_crop(rects, img):
  square_size = min(img.shape[:2])

  if len(rects) > 0:
    min_x = min(x for x, _, _, _ in rects)
    min_y = min(y for _, y, _, _ in rects)
    max_x = max(x for _, _, x, _ in rects)
    max_y = max(y for _, _, _, y in rects)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
  else:
    center_x = img.shape[1] / 2
    center_y = img.shape[0] / 2

  min_x = center_x - square_size/2
  max_x = center_x + square_size/2

  min_y = center_y - square_size/2
  max_y = center_y + square_size/2

  #print min_y, max_y, min_x, max_x

  if min_y < 0:
    max_y -= min_y
    min_y = 0
  
  if max_y > img.shape[0]:
    min_y -= (max_y - img.shape[0])
    max_y = img.shape[0]
  
  if min_x < 0:
    max_x -= min_x
    min_x = 0
  
  if max_x > img.shape[1]:
    min_x -= (max_x - img.shape[1])
    max_x = img.shape[1]
  
  print square_size, min_y, max_y, min_x, max_x

  img_cropped = img[min_y:max_y,min_x:max_x]

  return img_cropped

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

    return img

for f in os.listdir('images/twitter'):
  print f

  if not os.path.isfile('cropped/images/twitter/' + f):
    try:
      rects, img = detect("images/twitter/" + f)
    except cv2.error:
      print "  Could not open"
      continue

    img_cropped = calculate_crop(rects, img)

    #box(rects, img)
      
    cv2.imwrite('cropped/images/twitter/' + f, img_cropped);

