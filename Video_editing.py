#classes and subclasses to import
import cv2
import numpy as np
import os
import datetime


#################################################################################################
'''THE BLENDING FUNCTION'''
#################################################################################################
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


def main(video_file_with_path):
    cap = cv2.VideoCapture(video_file_with_path)
    image_red = cv2.imread("Overlay_Images\\yellow_flower.png",-1)
    image_blue = cv2.imread("Overlay_Images\\pink_flower.png",-1)
    image_green = cv2.imread("Overlay_Images\\red_flower.png",-1)
    

    #to count the number iterations in the loop
    count=0
    #Time of starting video
    start_time = datetime.datetime.now()
    ###########
    ret,frame=cap.read()
    framegrab=frame.copy()
    #Determine the dimensions of the test video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('video_outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    while(ret):
        ret2, img = cap.read()
        if(ret2):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,127,255,1)
            _,contours,h = cv2.findContours(thresh,1,2)
            for cnt in contours:
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                px=img[cy,cx,0]
                px1=img[cy,cx,1]
                px2=img[cy,cx,2]
                if(px==254):
                    color='blue'
                    c=1
                elif(px1==127):
                    color='green'
                    c=2
                elif(px2==254):
                    color='red'
                    c=3
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                #To determine the shape
                if len(approx)==5:
                    shape= "pentagon"
                elif len(approx)==3:
                    shape= "triangle"
                elif len(approx)==4:
                    shape= "rhombus"
                elif len(approx)==6:
                    shape= "hexagon"
                elif len(approx) == 9:
                    shape= "half-circle"
                elif len(approx) > 9:
                    shape= "circle"
                x,y,w,h=cv2.boundingRect(cnt)
                #Determine the flower to overlap
                if(c==3):
                    overlay_image = cv2.resize(image_red, (w,h))
                elif(c==1):
                    overlay_image = cv2.resize(image_blue, (w,h))
                elif(c==2):
                    overlay_image = cv2.resize(image_green, (w,h))
                #Blending function call with the selected dimensions of the part on which flower need to be overlayed
                framegrab[y:y+h,x:x + w, :] = blend_transparent( img[y:y+h,x:x+w,:], overlay_image)
                count=count+1
                print (count)
        else:
            break
        out.write(framegrab)
    cap.release()
    #Time of program end
    end_time = datetime.datetime.now()
    tp = end_time-start_time
    print (tp)

#####################################################################################################

#####################################################################################################
    #sample of overlay code for each frame
    #x,y,w,h = cv2.boundingRect(current_contour)
    #overlay_image = cv2.resize(image_red,(h,w))
    #frame[y:y+w,x:x+h,:] = blend_transparent(frame[y:y+w,x:x+h,:], overlay_image)
#######################################################################################################

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main(r'Video.mp4')
