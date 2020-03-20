import re
from math import floor

from PIL import Image, ImageDraw, ImageFilter, ImageStat
from PIL.ImageFilter import Filter, BuiltinFilter
import numpy as np
import pytesseract
import pandas as pd
import cv2



pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def find_game_cards(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    dst = cv2.dilate(dst, None)
    ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
    dst = np.uint8(dst)

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

    # Now draw them
    res = np.hstack((centroids, corners))
    res = np.int0(res)

    for r in res:
        img[r] = [0, 0, 255]
          #  img[res[:, 1], res[:, 0]] = [0, 0, 255]
         #   img[res[:, 3], res[:, 2]] = [0, 255, 0]

    cv2.imshow('subpixel5.png', img)

    cv2.waitKey(0)  # waits until a key is pressed
    cv2.destroyAllWindows()  # destroys the window showing image

def regex_filter(val):
        return val and not re.fullmatch(r' *',str(val))


def find_white_squers(img:Image):
    width,hight = img.size
    split = img.split()[2]
    pix = split.load()
    ws = []
    cv_img  = np.array(img)
    h, w = cv_img.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    rect_width,rec_hight = int(width/10),int(hight/10)
    size = lambda i,j:(max(i-rect_width,0),max(j-rec_hight,0),min(rect_width+i,width),min(rec_hight+j,hight))
    for i in range(rect_width,int(width-rect_width/4),int(rect_width/4)):
        for j in range(rec_hight,int(hight-rec_hight/4),int(rec_hight/4)):

            image_crop = split.crop(size(i,j))

            stat = ImageStat.Stat(image_crop)
            white_thresh = (np.array(stat.mean) + np.array(stat.stddev))

            if(pix[i,j] > white_thresh):
                #image_crop.show()
                diff = (255,255,int(white_thresh/10))
                _, _, _, rect = cv2.floodFill(cv_img, mask= mask,seedPoint= (i,j), newVal=255, loDiff=diff, upDiff=diff, flags=cv2.FLOODFILL_FIXED_RANGE)
                ws.append((rect,white_thresh))
    #cv2.imshow('subpixel5.png', cv_img)


    # filter rects
    ws = [((r[0][0],r[0][1],r[0][0]+r[0][2],r[0][1]+r[0][3]),white_thresh)
          for r in ws if rec_hight > r[0][3] > (rec_hight/7) and (rect_width*2) > r[0][2] > (rect_width/1.7) ]
    for r1 in ws:
        for r2 in ws:
            if(r1[0]!= r2[0]):
                if(all(abs(r1v-r2v)<(rect_width/2) for r1v,r2v in zip(r1[0],r2[0]))):
                    ws.remove(r2)

    # if(len(ws) < 25):
    #     assert (False)
    #     return find_white_squers(img)

    # print(ws)
    # print(len(ws))
    imgD = ImageDraw.Draw(img)
    res = []
    for w in ws:
        res.append((w[0],img.crop(w[0]),w[1]))
        imgD.rectangle(w[0],outline="red",fill="yellow")

    img.show()
    return res

def one_word_ocr(image,lang="heb"):
    return simple_ocr(image,lang)

def simple_ocr(image,lang="heb"):
    """
    This function will handle the core OCR processing of images.
    """
    image = image.convert("L")
    img_thresh = 50
    img_s = image.point(lambda x: 0 if x < (255-img_thresh)*3 else 255).filter(ImageFilter.EDGE_ENHANCE_MORE)
    custom_oem_psm_config = ''
    text = pytesseract.image_to_data(img_s,output_type="data.frame", config=custom_oem_psm_config,lang=lang)
    text = text[text['text'].apply(regex_filter)]
    text = text[text['conf'] > 0]
    text = text.sort_values('conf', ascending=False)

    words =  [t for t in text['text'].values if len(t) > 1]
    # weidth,hight = image.size
    # text =  text[pd.notnull(text['text'])]
    # text = text[text['text'].str.len() > 1] # todo filter alphabetic
    # text = text.sort_values('conf',ascending = False)[:25]
    # text['sort'] = (text['top']*100+text['left']*10)
    # text = text.sort_values('sort')

    #sort:
    #words = sorted(words,key=lambda r:(round(r[1][0]/(width/5)),round(r[1][1]/(hight/5))))

    return words

def ocr_core2(image_file):
    #    dir -- either 1 (light text) or -1 (dark text), the direction the ray should be cast

    image = cv2.imread(image_file)
    final_img, swt_ld, cc_ld, cc_boxes, filtered_cc = pyswt.run(image)

   # for w in cc_boxes:
    #    image = cv2.rectangle(image, w[0], w[1], (0, 255, 0), 3)

    cv2.imshow('image', image)
    cv2.imshow('final_img', final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ocr_core(image):
    """
    This function will handle the core OCR processing of images.
    """
    image.show()
    image = image.convert("RGB")
    width,hight = image.size

    images_rect = find_white_squers(image)

    #image = black_white_filter(image)
    words = []
    for img in images_rect:
        # preprocessing
        img_s = img[1].convert('L')
        img_thresh = img[2]# grayscale
        img_s = img_s.point(lambda x: 0 if x < (255-img_thresh)*3 else 255).filter(ImageFilter.EDGE_ENHANCE_MORE)
        custom_oem_psm_config = ''
        lang = "heb"#None
        text = pytesseract.image_to_data(img_s,output_type="data.frame", config=custom_oem_psm_config,lang=lang)
        text = text[text['text'].apply(regex_filter)]
        text = text[text['conf'] > 0]
        text = text.sort_values('conf', ascending=False)
        #print(text)
        if len(text) == 0:
            #img_s.show()
            print(img[0])
# threshold (binarize)
        else:
            words.append((text['text'].values[0],img[0]))
    # weidth,hight = image.size
    # text =  text[pd.notnull(text['text'])]
    # text = text[text['text'].str.len() > 1] # todo filter alphabetic
    # text = text.sort_values('conf',ascending = False)[:25]
    # text['sort'] = (text['top']*100+text['left']*10)
    # text = text.sort_values('sort')

    #sort:
    words = sorted(words,key=lambda r:(round(r[1][0]/(width/5)),round(r[1][1]/(hight/5))))

    return words

if(__name__ == "__main__"):
    filename = 'data/img/10he.jpg'
    res = ocr_core2(filename)
    #custom_oem_psm_config = r''
    #image = Image.open(filename)
    #res = ocr_core2(image)
    print(res)
    print(len(res))


