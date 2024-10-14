import cv2
import time
import pandas as pd
x=1
y=2
z=x*y

# Paths to the image and CSV file
img_path = 'image 2.png'
csv_path = 'colors.csv'

# Read the CSV file into a DataFrame
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Read and resize the image
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# Global variables to store color information and click status
clicked = False
r = g = b = xpos = ypos = 0

# Function to calculate the minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 1000
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d < minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

# Function to get x, y coordinates of mouse double-click
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)

# Creating window and setting a mouse callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        # Draw a rectangle and display the color name and RGB values
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)
        text = f'{get_color_name(r, g, b)} R={r} G={g} B={b}'
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    # Break the loop when 'ESC' key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

