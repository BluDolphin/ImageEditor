# Importing Image class from PIL module
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)


# Opens a images in RGB mode
leftHalf = Image.open("testImage.jpg")
rightHalf = Image.open("testImage.jpg")


# Size of the image in pixels (size of original image)
width, height = leftHalf.size # Get hight and width of the image
logging.info("width = " + str(width) + " height = " + str(height))

halfWidth = int(width/2) # Get the half width of the image
halfHeight = int(height/2) # Get the half height of the image
logging.info("halfWidth = " + str(halfWidth) + " halfHeight = " + str(halfHeight))


# Cropping image to get left and right half
leftHalf = leftHalf.crop((0, 0, halfWidth, height))
rightHalf = rightHalf.crop((halfWidth, 0, width, height))

rotAmount = 15 # Variable for rotation amount
leftHalf = leftHalf.rotate(rotAmount, expand=True, fillcolor=(255,255,255)) # Rotate the left half
rightHalf = rightHalf.rotate(-rotAmount, expand=True, fillcolor=(255,255,255)) # Rotate the right half


# Create a background to paste the images on
rootImage = Image.new('RGB', (leftHalf.width + rightHalf.width, max(leftHalf.height, rightHalf.height)), (255,255,255))  # Create background with the overall width of both images, and the maximum height
rootImage.paste(leftHalf, (0, 0))  # Paste the left half on the left with mask
rootImage.paste(rightHalf, (leftHalf.width, 0))  # Paste the right half on the right

#rootImage.show() # Show the image
rootImage.thumbnail((4080, 3488)) # Resize the image to desired size

rootImage.show() # Show the image
rootImage.save("editedImage.jpg") # Save the image