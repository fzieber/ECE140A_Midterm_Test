
# Import OpenCV
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Read the image
image_url = "./sudoku_test.jpeg"
img = cv2.imread(image_url, 0)
# 0 is a simple alias for cv2.IMREAD_GRAYSCALE


# Preprocessing

# Add a Gaussian Blur to smoothen the noise
blur = cv2.GaussianBlur(img.copy(), (9, 9), 0)
cv2.imwrite("Blur.png", blur)

# Threshold the image to get a binary image
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("Threshold.png", thresh)


# Invert the image to swap the foreground and background
invert = 255 - thresh
cv2.imwrite("Inverted.png", invert)

# Dilate the image to join disconnected fragments
kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
dilated = cv2.dilate(invert, kernel)
cv2.imwrite("Dilated.png", dilated)

# Get contours
contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest 15 contours
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

# Find best polygon and get location
location = None

# Finds rectangular contour
for contour in contours:
    approx = cv2.approxPolyDP(contour, 15, True)
    if len(approx) == 4:
        location = approx
        break

# Handle cases when no quadrilaterals are found        
if type(location) != type(None):
    print("Corners of the contour are: ",location)
else:
    print("No quadrilaterals found")

# Sudoku Specific: Transform a skewed quadrilateral
def get_perspective(img, location, height = 900, width = 900):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

if type(location) != type(None):
    result = get_perspective(img, location)
    result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite("Result.png", result)


# Split the board into 81 blocks
def split_boxes(board, input_size=100):
    rows = np.vsplit(board,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
        for box in cols:
            #box = cv2.resize(box, (input_size, input_size))/255.0
            _, bThresh = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            boxes.append(bThresh)
    return boxes

ans = split_boxes(result)




# Get text from each box
out = [[0]*9 for _ in range(9)]
print("Collecting initial grid data:") 
for i in range(9):
    for j in range(9):
        text = pytesseract.image_to_string(
            Image.fromarray(ans[9*i+j].astype(np.uint8)),
            lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        
        if ord(text[0]) >= 48 and ord(text[0]) <= 57:
            out[i][j] = text[0]
        else:
            text2 = pytesseract.image_to_string(
                Image.fromarray(ans[9*i+j].astype(np.uint8)),
                lang='eng', config='--psm 10 --oem 3 ')
            if (ord(text2[0]) == 114 or ord(text2[0]) == 103):
                out[i][j] = '9'
    print ("row %s complete"%i)



print("The grid detected is as follows:\n",out)




N= 9
def puzzle(out):
    for i in range(N):
        for j in range(N):
            print(out[i][j],end = " ")
        print()


def solve(out, row, col, num):
    for x in range(9):
        if int(out[row][x]) == num:
            return False
             
    for x in range(9):
        if int(out[x][col]) == num:
            return False
 
 
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if int(out[i + startRow][j + startCol]) == num:
                return False
    return True




def Suduko(out, row, col):
 
    if (row == N - 1 and col == N):
        return True
    if col == N:
        row += 1
        col = 0
    
    if int(out[row][col]) > 0:
        return Suduko(out, row, col + 1)
    for num in range(1, N + 1, 1): 
     
        if solve(out, row, col, num):
         
            out[row][col] = str(num)
            if Suduko(out, row, col + 1):
                return True
        out[row][col] = 0
    return False




if (Suduko(out, 0, 0)):
    puzzle(out)
else:
    print("Solution does not exist:(")