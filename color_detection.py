import cv2
import numpy as np
import pandas as pd
import argparse
from pathlib import Path

#Reading csv file (from the images folder next to this script, so it works from any folder) and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv(Path(__file__).parent / 'images' / 'colors.csv', names=index, header=None)

#Converting every known color to Lab once, since Lab distances match how people see color
known_bgr = csv[["B","G","R"]].to_numpy(dtype=np.uint8).reshape(-1, 1, 3)
known_lab = cv2.cvtColor(known_bgr, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)

#function to find the closest matching color, comparing against all colors at once
def getColorName(R,G,B):
    lab = cv2.cvtColor(np.uint8([[[B,G,R]]]), cv2.COLOR_BGR2LAB).reshape(3).astype(np.float32)
    distances = np.linalg.norm(known_lab - lab, axis=1)
    best = csv.iloc[int(np.argmin(distances))]
    return best["color_name"], best["hex"]

#function to read an image and shrink big images (e.g. phone photos) so the whole picture fits on screen
def load_image(img_path, max_w=1200, max_h=800):
    img = cv2.imread(img_path)
    if img is None:
        raise SystemExit("Could not read image: " + img_path)
    scale = min(max_w / img.shape[1], max_h / img.shape[0], 1.0)
    if scale < 1.0:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    return img

def main():
    #Creating argument parser to take image path from command line
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help="Image Path")
    args = vars(ap.parse_args())
    img = load_image(args['image'])

    #state shared with the mouse callback
    state = {"clicked": False, "r": 0, "g": 0, "b": 0, "xpos": 0, "ypos": 0}

    #function to get x,y coordinates of mouse click
    def draw_function(event, x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            #Averaging a 5x5 patch around the click so photo noise doesn't change the answer
            patch = img[max(y-2,0):y+3, max(x-2,0):x+3].reshape(-1, 3)
            b,g,r = (int(v) for v in patch.mean(axis=0).round())
            state.update(clicked=True, r=r, g=g, b=b, xpos=x, ypos=y)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_function)

    text = None
    while(1):
        r, g, b = state["r"], state["g"], state["b"]

        if (state["clicked"]):
            #Creating text string to display( Color name, hex code and RGB values )
            name, hex_code = getColorName(r,g,b)
            text = name + ' ' + hex_code.upper() + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
            print(text)
            state["clicked"]=False

        #Drawing on a copy so the banner never covers the pixels you click next
        display = img.copy()
        if text:
            #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
            cv2.rectangle(display,(10,10), (display.shape[1]-10,60), (b,g,r), -1)
            cv2.rectangle(display,(10,10), (display.shape[1]-10,60), (0,0,0), 2)

            #For very light colours we will display text in black colour
            text_color = (0,0,0) if r+g+b>=600 else (255,255,255)

            #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
            cv2.putText(display, text,(25,45),2,0.8,text_color,2,cv2.LINE_AA)

            #Marking the clicked spot
            cv2.circle(display,(state["xpos"],state["ypos"]),6,(255,255,255),2)
            cv2.circle(display,(state["xpos"],state["ypos"]),8,(0,0,0),1)

        cv2.imshow("image",display)

        #Break the loop when user hits 'esc' key or closes the window
        if cv2.waitKey(20) & 0xFF ==27:
            break
        if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
