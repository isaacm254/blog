import hashlib
import base64
import datetime
from werkzeug.utils import secure_filename
import os
from main import app

SECRET = 'FNWUI34HRF734BU9FGB498CBRIFU6uhghfg6'

def hash_password(password):
    #hash the admins password
	text_ = str(password) + SECRET
	return hashlib.md5(text_.encode('utf-8')).hexdigest()

# get the imgs with thier urls
def get_imgs_from_url(rows):
    # new rows array to return
    new_rows = []
    # new row array
    new_row = []
    # new sub imgs array
    new_sub_imgs = []
    for row in rows:
        # convert the current row articles data with main img to array from tuple
        new_row = convert_to_array(row['row'])
        # change the main img url in article row to string base64
        new_row[2] = get_base64_img(new_row[2])
        # convert article sub imgs tuple to array
        sub_imgs = get_sub_imgs_array(row['sub_imgs'])
        for img_url in sub_imgs:
            # append the img base64 into the new sub imgs array
            new_sub_imgs.append(get_base64_img(img_url))
        # item is an temp object to append the new row and new sub imgs to new rows table 
        item = {}
        item['row'] = new_row
        item['sub_imgs'] = new_sub_imgs
        item['readings'] = row['readings']
        item['classes'] = row['classes']
        new_rows.append(item)
        new_sub_imgs = []
    return new_rows

def get_base64_img(url):
    # get img data from url and convert it to base64 
    with open(url, 'rb') as f:
        base64_img = base64.b64encode(f.read())
        return 'data:image/jpeg;base64,' + base64_img.decode("utf-8")

def get_sub_imgs_array(tuple_):
    # to convert the sub imgs tuple to array
    new_array = []
    for elem in tuple_:
        new_array.append(elem[0])
    return new_array

def convert_to_array(tuple_):
    # to convert the article row tuple to array
    new_array = []
    for elem in tuple_:
        new_array.append(elem)
    return new_array

def save_imgs(imgs):
    # to save img base64 data to .jpeg file which its name is the current date
    imgs_url = []
    for img in imgs:
        # to split base64 img which is strcture like 'data:image/extension;base64, image data' this strocture is invailed for byte
        img = split_img(img)
        # img file name is the current datetime
        c_date = datetime.datetime.now()
        # create secure file name
        filename = secure_filename(str(c_date) + '.jpeg')
        # decode image base64 and convert it to byte data
        imgdata = decode_base64(img)
        # create file to save the img in it
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
            f.write(imgdata)
        imgs_url.append(app.config['UPLOAD_FOLDER']+ filename)
    return imgs_url
# to split the image
def split_img(img):
    return img.split(',')[1]

def decode_base64(data):
    # convert image to byte and then decode it
    data = bytes(data, encoding="UTF-8")
    return base64.decodestring(data)

