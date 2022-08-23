import cv2
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFilter
import math

form_w = 1240 
form_h = 1754
qr_box_size = 8
qr_size = 21 * qr_box_size 

def main():
# save_white_img(form_w, form_h, 'blank')
# save_qr(123,'qr/qr1')
# border = 80
# place_qr_on_image('blank', 'qr/qr1', [form_w - qr_size - border, border], 'blank')
# place_qr_on_image('blank', 'qr/qr1', [border, border],                    'blank')
# place_qr_on_image('blank', 'qr/qr1', [border, form_h - qr_size - border], 'blank')
#
  orig = get_qr_triangle('blank')
  cur = get_qr_triangle('blankr')
  
  transform_form(orig, cur, 'blankr')

def transform_form(orig, cur, filename):
  
  M = cv2.getAffineTransform(np.float32(cur), np.float32(orig))

  blank = cv2.imread(filename + '.png')
  final = cv2.warpAffine(blank, M, (form_w, form_h), flags=cv2.INTER_LINEAR)

  cv2.imwrite(filename + '_processed.png', final)


def get_qr_triangle(filename):
  _, data, bbox,_ = cv2.QRCodeDetector().detectAndDecodeMulti(cv2.imread(filename + '.png'))
  bl, tl, tr = sort_bboxes(bbox)
  return np.array([bl[3], tl[0], tr[1]])

def sort_bboxes(bboxes):
  used = [False, False, False]
  rightmost_coord = -math.inf
  rightmost_index = -1
  for i in range(3):
    for c in bboxes[i]:
      if c[0] > rightmost_coord:
        rightmost_coord = c[0]
        rightmost_index = i

  lowest_coord = -math.inf
  lowest_index = -1
  for i in range(3):
    for c in bboxes[i]:
      if c[1] > lowest_coord:
        lowest_coord = c[1]
        lowest_index = i

  central_index = -1
  for i in range(3):
    if i != rightmost_index and i != lowest_index:
      central_index = i

  return bboxes[lowest_index], bboxes[central_index], bboxes[rightmost_index]


def get_white_img(w,h):
  img = np.zeros((h,w,1), np.uint8)
  img.fill(255)
  return img

def save_white_img(w,h,filename):
  cv2.imwrite(filename + '.png',get_white_img(w,h))


def save_qr (data, filename):
  qr = qrcode.QRCode(
    version=1,
    box_size=qr_box_size,
    border=0,
  )
  qr.add_data(data)
  qr.make(fit=True)
  qr.make_image(fill_color="black", back_color="white").save(filename + '.png')


def place_qr_on_image (srcfile, qrfile, coords, filename):
  qr = Image.open(qrfile + '.png')
  src = Image.open(srcfile + '.png')
  ret = src.copy()
  ret.paste(qr, coords)
  ret.save(filename + '.png')



def restore_form (filename):

  src = cv2.imread(filename + '.png')
  data, bbox, straight_qr = cv2.QRCodeDetector().detectAndDecode(src)

  dest = [[2065,  100],  [2379, 100],  [2379,  414],  [2065,  414]] 

  M = cv2.getAffineTransform(np.float32(bbox[0][1:]), np.float32(dest[1:]))

  final = cv2.warpAffine(blank, M, (2480, 3508), flags=cv2.INTER_LINEAR)
  
  cv2.imwrite('processed.png', final)





if __name__ == '__main__':
  main()
