import cv2
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model

def init_feature_extractor():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    return Model(inputs=base_model.input, outputs=base_model.get_layer('block5_conv3').output)

def align_images(img1, img2):
    """Align two images using ORB feature matching"""
    orb = cv2.ORB_create(nfeatures=2000) # Increased features for more robust matching
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    
    # Check if we have enough descriptors
    if des1 is None or des2 is None:
        return None
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # Check if we have any matches
    try:
        matches = bf.match(des1, des2)
        if not matches:
            return None
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Keep only good matches
        good_matches = matches[:50]
        
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
        
        M, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        
        # Check if a valid homography matrix was found
        if M is None:
            return None
            
        aligned = cv2.warpPerspective(img2, M, (img1.shape[1], img1.shape[0]))
        return aligned
    except cv2.error:
        return None

def preprocess_image(img):
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
