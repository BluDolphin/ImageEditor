from PIL import Image
import logging
from PIL import ImageFilter

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
                print("Invalid input")
                continue


# OPENING IMAGE ---------------------------------------------------------------------
while True:
    print("Make sure the image is in the same directory as this program\n")
    fileName = str(userInput("s", "Enter the file name of the image: ")) # Get file name from user
    try:
        leftHalf = Image.open(fileName)
        rightHalf = Image.open(fileName)
        logging.info("Image opened: Generated left and right half\n")
        break
    except:
        print("Invalid file name/ File not found\n")
        continue

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


# CROPPING IMAGE ---------------------------------------------------------------------
while True:
    fullOrMirror = str(userInput("s", "Full or Mirror image (f/m): ")).lower() # Get input from user
    if fullOrMirror == "f": # If full image
        logging.info(f"leftHalf size: {leftHalf.size}  rightHalf size: {rightHalf.size}")
        leftHalf = leftHalf.crop((0, 0, halfWidth, height)) # Crop the left half from the left to the middle point
        rightHalf = rightHalf.crop((halfWidth, 0, width, height)) # Crop the right half from the middle point to the right
        logging.info(f"Crop successful: leftHalf size: {leftHalf.size}  rightHalf size: {rightHalf.size}")
        break
    
    elif fullOrMirror == "m": # If mirrored image
        break # Do nothing
    
    else:
        print("Invalid input: Input f or m\n")
        continue

# ROTATING IMAGE ---------------------------------------------------------------------
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

# SPACING IMAGE ---------------------------------------------------------------------
while True:
    spacerInput = userInput("i", "Enter the amount for spacing (defualt 500): ") # Get rotation amount from user
    if spacerInput == "": # If no input
        spacerWidth = 500 # Set rotation amount to 1 (defualt 500)
        logging.info("spacerWidth = 500")
        break
        
    elif 0 <= int(spacerInput) <= 1500: # if input is between 0 and 1500
        spacerWidth = int(spacerInput) # Convert input to int
        break # Break the loop
    
    else:
        print("Invalid input: Input a number between 0 and 1500\n")
        continue

logging.info("Creating spacer image")
spacer = Image.new('RGB', (spacerWidth, max(leftHalf.height, rightHalf.height)), (255,255,255))  # Create background with the overall width of both images, and the maximum height

# SMOOTHING IMAGE ---------------------------------------------------------------------
# Convert images back to "RGB" mode before applying the filter
leftHalf = leftHalf.convert("RGBA")
leftHalf = leftHalf.filter(ImageFilter.SMOOTH)

rightHalf = rightHalf.convert("RGBA")
rightHalf = rightHalf.filter(ImageFilter.SMOOTH)

#smooth edges of the immages
leftHalf = leftHalf.filter(ImageFilter.SMOOTH)
rightHalf = rightHalf.filter(ImageFilter.SMOOTH)

# COMBINING IMAGES ---------------------------------------------------------------------
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

# SIZING IMAGE ---------------------------------------------------------------------
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

# ADDING TO BACKGROUND --------------------------------------------------------------
background = Image.new('RGB', (600, 600), (255,255,255))  # Create background to stick the root on 
logging.info("background created")

if fullOrMirror == "f": # If full image
    offset =+ 10
else:
    offset =+ 5

logging.info(f"Offset set to {offset}, Pasting rootImage on background")    
background.paste(rootImage, (int((600 - rootImage.width)/2) + offset, int((600 - rootImage.height)/2) + offset)) # Paste the right half on the right
logging.info("rootImage pasted on background, showing image")

# SETTING TO A4 SIZE ----------------------------------------------------------------
finalPage = Image.new('RGB', (1150, 1626), (255,255,255))  # Create A4 page
logging.info("A4 page created")

#past background at the top left corder of the A4 page
finalPage.paste(background, (50, 50))  # Paste the right half on the right
logging.info("background pasted on A4 page, showing image")

finalPage.show() # Show the image

# SAVING IMAGE ---------------------------------------------------------------------
while True:
    save = str(userInput("s", "Save image? (y/n): ")).lower() # Get input from user
    if save == "y": # If input is y
        logging.info("removing file extention and saving image as .png")
        fileName = fileName[:fileName.index(".")] # remove extention from file name 
        background.save(fileName + "_edited.png") # Save the image
        finalPage.save(fileName + "_edited(A4).png")
        logging.info(f"Image saved as {fileName}_edited.png")
        break # Break the loop
    
    elif save == "n": # If input is n
        break # Break the loop
    
    else:
        print("Invalid input\n"
            "Input y or n\n")
        continue