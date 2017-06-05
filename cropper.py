from PIL import Image
import numpy as np
import scipy.misc


def autoCrop(in_image, out_image):

    im = Image.open(in_image)
    pix = np.asarray(im)

    pix = pix[:,:,0:3] # Drop the alpha channel
    idx = np.where(pix-255)[0:2] # Drop the color when finding edges
    box = map(min,idx)[::-1] + map(max,idx)[::-1]

    region = im.crop(box)
    region_pix = np.asarray(region)

    scipy.misc.imsave(out_image, region_pix)
