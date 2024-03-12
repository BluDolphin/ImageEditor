from PIL import Image, ImageFilter
import logging


def debugMode():
    logging.basicConfig(level=logging.INFO)
    logging.debug("Debug mode is on")
    return True
debugMode() if input("Debug mode? (y/n): ").lower() == "y" else print("")

def userInput(type, prompt):
    while True:
        if type == "s":
            return str(input(prompt))
        if type == "i":
            temp = input(prompt)
            if temp == "": return temp
            
            try:
                temp = int(temp)
                return temp
            except:
                print("Invalid input\n")
                continue

"""
order of operations for editing an image
1) open image
2) setup image
3) crop image
4) rotate image
5) create spacer
6) smooth image
7) combine images into root
8) resizing image
9) adding to background
10) save image
"""

def saveImage():
    global rootImage, fileName
    while True:
        save = str(userInput("s", "Save image? (y/n): ")).lower() # Get input from user
        if save == "y": # If input is y
            logging.info("removing file extention and saving image as .png")
            fileName = fileName[:fileName.index(".")] # remove extention from file name 
            rootImage.save(fileName + "_edited.png") # Save the image
            logging.info(f"Image saved as {fileName}_edited.png")
            break # Break the loop
        
        elif save == "n": # If input is n
            break # Break the loop
        
        else:
            print("Invalid input\n"
                "Input y or n\n")
            continue
        
def backgroundImage():
    global rootImage, cropped, offset, background
    
    background = Image.new('RGB', (600, 600), (255,255,255))  # Create background to stick the root on 
    logging.info("background created")

    if cropped == True: # If full image
        offset =+ 10
    else:
        offset =+ 5

    logging.info(f"Offset set to {offset}, Pasting rootImage on background")    
    background.paste(rootImage, (int((600 - rootImage.width)/2) + offset, int((600 - rootImage.height)/2) + offset)) # Paste the right half on the right
    logging.info("rootImage pasted on background, showing image")
    background.show() # Show the image

def resizeImage():
    global rootImage
    
    while True:
        resizeInput = str(userInput("s", "fit to wing, whole wing, or custom? (1/2/3): ")).lower() # Get input from user
        if resizeInput == "1": # If input is y
            # Calculate new size: original size * 1.1 to make it 10% larger
            new_size = (int(rootImage.width * 1.025), int(rootImage.height * 1.025))
            break # Break the loop
        
        elif resizeInput == "2": # If input is n
            new_size = (int(rootImage.width * 1.5), int(rootImage.height * 1.5))
            break # Break the loop
        
        elif resizeInput == "3":
            print("\nEnter % to increase image size")
            widthPercent = int(userInput("i", "Width: ")) / 100
            heightPercent = int(userInput("i", "Height: ")) / 100
            
            logging.info(f"width increase = {widthPercent} height increase = {heightPercent}")
            new_size = (int(rootImage.width * (1 + widthPercent)), int(rootImage.height * (1 + heightPercent))) 
            logging.info(f"new size = {new_size}")
            break
        else:
            print("Invalid input: Input 1, 2, or 3\n")
            continue

    rootImage = rootImage.resize(new_size)
    logging.info(f"rootImage resized to {new_size}")
    return rootImage

def combiningImages():
    #SET GLOBAL VARIABLES
    global leftHalf, rightHalf, spacer, rootImage
    
    logging.info("\nCombining images")
    logging.info(f"Creating new image with width: {leftHalf.width + spacer.width + rightHalf.width} and height: {max(leftHalf.height, spacer.height, rightHalf.height)}")
    rootImage = Image.new('RGB', (leftHalf.width + spacer.width + rightHalf.width, max(leftHalf.height, spacer.height, rightHalf.height)), (255,255,255))  # Create background with the overall width of both images, and the maximum height
    logging.info("rootImage created, pasting images")
    rootImage.paste(leftHalf, (0, 0))  # Paste the left half on the left with mask
    rootImage.paste(spacer, (leftHalf.width, 0))  # Paste the left half on the left with mask
    rootImage.paste(rightHalf, (leftHalf.width + spacer.width, 0))  # Paste the right half on the right

    logging.info("rootImage created, rotating rootImage 45 degrees and resizing to 650x650 pixels")
    rootImage = rootImage.rotate(45, expand=True, fillcolor=(255,255,255)) # Rotate the image 90 degrees
    rootImage.thumbnail((650, 650)) # Resize the image to desired size

def smoothImage():
    #SET GLOBAL VARIABLES
    global leftHalf, rightHalf
    
    # Convert images back to "RGB" mode before applying the filter
    leftHalf = leftHalf.convert("RGBA")
    leftHalf = leftHalf.filter(ImageFilter.SMOOTH)

    rightHalf = rightHalf.convert("RGBA")
    rightHalf = rightHalf.filter(ImageFilter.SMOOTH)

    #smooth edges of the immages
    leftHalf = leftHalf.filter(ImageFilter.SMOOTH)
    rightHalf = rightHalf.filter(ImageFilter.SMOOTH)

def createSpacer():
    #SET GLOBAL VARIABLES
    global spacerWidth, spacer
    
    while True:
        spacerInput = userInput("i", "Enter the amount for spacing (defualt 500): ") # Get rotation amount from user
        if spacerInput == "": # If no input
            spacerWidth = 500 # Set rotation amount to 1 (defualt 500)
            logging.info("spacerWidth = 500")
            break
            
        elif 0 <= int(spacerInput) <= 1501: # if input is between 0 and 1500
            spacerWidth = int(spacerInput) # Convert input to int
            break # Break the loop
        
        else:
            print("Invalid input: Input a number between 0 and 1500\n")
            continue

    logging.info("Creating spacer image")
    spacer = Image.new('RGB', (spacerWidth, max(leftHalf.height, rightHalf.height)), (255,255,255))  # Create background with the overall width of both images, and the maximum height

def rotatingImage():
    #SET GLOBAL VARIABLES
    global rotAmount, leftHalf, rightHalf
    
    while True:
        rotAmount = userInput("i", "Enter the rotation amount (defualt 1): ") # Get rotation amount from user
        if rotAmount == "": # If no input
            rotAmount = 1 # Set rotation amount to 1 (defualt)
            break
            
        elif 0 <= int(rotAmount) < 360: # if input is between 0 and 360
            rotAmount = int(rotAmount) # Convert input to int
            break # Break the loop
        
        else:
            print("Invalid input: Input a number between 0 and 360\n")
            continue
        
    leftHalf = leftHalf.rotate(rotAmount, expand=True, fillcolor=(255,255,255)) # Rotate the left half
    rightHalf = rightHalf.rotate(-rotAmount, expand=True, fillcolor=(255,255,255)) # Rotate the right half
    logging.info("Both halfs rotated")

def cropImage(kiteType):
    #SET GLOBAL VARIABLES
    global fullOrMirror, leftHalf, rightHalf, width, height, halfWidth, halfHeight, cropped
    

    if kiteType == "tinyDancer":
        while True:
            fullOrMirror = str(userInput("s", "Full or Mirror image (f/m): ")).lower() # Get input from user
            if fullOrMirror == "f": # If full image
                logging.info(f"leftHalf size: {leftHalf.size}  rightHalf size: {rightHalf.size}")
                leftHalf = leftHalf.crop((0, 0, halfWidth, height)) # Crop the left half from the left to the middle point
                rightHalf = rightHalf.crop((halfWidth, 0, width, height)) # Crop the right half from the middle point to the right
                logging.info(f"Crop successful: leftHalf size: {leftHalf.size}  rightHalf size: {rightHalf.size}")
                cropped = True
                break
            
            elif fullOrMirror == "m": # If mirrored image
                break # Do nothing
            else:
                print("Invalid input: Input f or m\n")
                continue
            
    elif kiteType == "generalImage":
        while True:
            verticalOrHorizontal = str(userInput("s", "Vertical or Horizontal crop (v/h): ")).lower() # Get input from user
            if verticalOrHorizontal == "v": #crop vertically
                leftHalf = leftHalf.crop((0, 0, halfWidth, height)) # Crop the left half from the left to the middle point
                rightHalf = rightHalf.crop((halfWidth, 0, width, height)) # Crop the right half from the middle point to the right
                cropped = True
                break
            
            elif verticalOrHorizontal == "h": #crop horizontally
                leftHalf = leftHalf.crop((0, 0, width, halfHeight)) # Crop the left half from the left to the middle point
                rightHalf = rightHalf.crop((0, halfHeight, width, height)) # Crop the right half from the middle point to the right
                cropped = False
                break
            else:
                print("Invalid input: Input f or m\n")
                continue

def imagePrep():
    #SET GLOBAL VARIABLES
    global leftHalf,rightHalf, width, height, aspectRatio, halfWidth, halfHeight
    
    width, height = leftHalf.size # Get height and width of the image
    logging.info("width = " + str(width) + " height = " + str(height))

    #get aspect ratio
    aspectRatio = width / height
    logging.info("aspectRatio = " + str(aspectRatio))

    #resize image to 3280 height
    if height < 3280:
        logging.info("Resizing image to 3280 pixels")
        leftHalf = leftHalf.resize((int(3280 * aspectRatio), 3280), resample=Image.LANCZOS)
        rightHalf = rightHalf.resize((int(3280 * aspectRatio), 3280), resample=Image.LANCZOS)
        width, height = leftHalf.size # Get height and width of the image
        logging.info("width = " + str(width) + " height = " + str(height))

    halfWidth = int(width/2) # Get the half width of the image
    halfHeight = int(height/2) # Get the half height of the image
    logging.info("halfWidth = " + str(halfWidth) + " halfHeight = " + str(halfHeight))

def imageOpening(numOfImages):
    #SET GLOBAL VARIABLES
    global fileName, leftHalf, rightHalf
    
    if numOfImages == 1:
        while True:
            print("\nMake sure the image is in the same directory as this program\n")
            fileName = str(userInput("s", "Enter the file name of the image: ")) # Get file name from user
            try:
                leftHalf = Image.open(fileName)
                rightHalf = Image.open(fileName)
                logging.info("Image opened: Generated left and right half\n")
                break
            except:
                print("Invalid file name/ File not found\n")
                continue
    elif numOfImages == 2:
        while True:
            print("Make sure the image is in the same directory as this program\n")
            fileName1 = str(userInput("s", "Enter the file name of the first image: ")) # Get file name from user
            fileName2 = str(userInput("s", "Enter the file name of the seccond image: ")) # Get file name from user
            try:
                leftHalf = Image.open(fileName1)
                rightHalf = Image.open(fileName2)
                logging.info("Image opened: Generated left and right half\n")
                break
            except:
                print("Invalid file name/ File not found\n")
                continue
    #Go to image prep to setup the image/s        
    imagePrep()


def tinyDancer():
    while True:
        numOfImages = userInput("i", "Enter the number of images (1/2): ") # Get input from user
        if numOfImages == 1 or numOfImages == 2:
            break
        else:
            print("Invalid input: Input 1 or 2\n")
            continue
    imageOpening(numOfImages)
    cropImage("tinyDancer")
    rotatingImage()
    createSpacer()
    smoothImage()
    combiningImages()
    resizeImage()
    backgroundImage()
    saveImage()
    
def generalImage():
    while True:
        numOfImages = userInput("i", "Enter the number of images (1/2): ") # Get input from user
        if numOfImages == 1 or numOfImages == 2:
            break
        else:
            print("Invalid input: Input 1 or 2\n")
            continue
    imageOpening(numOfImages)
    cropImage("generalImage")
    createSpacer()
    smoothImage()
    combiningImages()
    (rootImage:=resizeImage()).show()
    saveImage(rootImage)
    
def mainMenu():
    print("1) Tiny Dancer\n"
          "2) General image")
    
    choice = userInput("i", "Enter choice>  ")
    if choice == 1:
        tinyDancer()
    elif choice == 2:
        generalImage()
    else:
        print("Invalid input\n")
    mainMenu()
    
    
mainMenu()