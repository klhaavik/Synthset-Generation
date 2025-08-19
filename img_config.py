from PIL import Image, ImageEnhance 
import cv2
import os
import numpy as np
import glob

def brighten_images_in_dir(dir):
    for image_file in os.listdir(dir):
        image = Image.open(os.path.join(dir, image_file))
        enhancer = ImageEnhance.Brightness(image)
        bright_image = enhancer.enhance(1.5)
        bright_image.save(image_file)

def remove_channels_for_images_in(dir):
    for imgfile in os.listdir(dir):
        filename = os.path.join(dir, imgfile)
        if(filename.endswith('checkpoints')): continue
        print(filename)
        image = cv2.imread(filename)
        # arr = np.asarray(bytearray(img.read()), dtype=np.uint8)
        # image = cv2.imdecode(img,-1) # 'load it as it is'
        s = image.shape
        #check if third tuple of s is 4
        #if it is 4 then remove the 4th channel and return the image.
        if len(image.shape) > 2 and image.shape[2] == 4:
        #convert the image from RGBA2RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR) 
        cv2.imwrite(filename, image)

def convert_to_binary(input_path, output_path, threshold=128):
    """
    Converts a PNG image to true black and white (binary).

    Args:
        input_path (str): Path to the input PNG image.
        output_path (str): Path to save the output binary PNG image.
        threshold (int): Pixel value threshold (0-255). 
                            Pixels above this value become white (255), 
                            and pixels below become black (0).
    """
    try:
        img = Image.open(input_path).convert('L')  # Open and convert to grayscale ('L' mode)

        # Apply threshold to binarize the image
        # 'point' method applies a function to each pixel
        # 'mode=1' specifies a 1-bit pixel format (black and white)
        binary_img = img.point(lambda x: 255 if x > threshold else 0, mode='1')

        binary_img.save(output_path)
        print(f"Image successfully converted and saved to {output_path}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_to_binary_dir(dir, desired_threshold):
    for imgfile in os.listdir(dir):
        filename = os.path.join(dir, imgfile)
        if(filename.endswith(".png")):
            input_image_path = filename
            output_image_path = filename
            convert_to_binary(input_image_path, output_image_path, desired_threshold)

def resize_images(dir):
    for imgfile in os.listdir(dir):
        filename = os.path.join(dir, imgfile)
        if(filename.endswith('checkpoints')): continue
        print(filename)
        image = Image.open(filename)
        image.resize((1666,1666)).save(filename.split('.')[0] + "_resized.png")

def resize_image(filename, size):
    image = Image.open(filename)
    resized_image = image.resize(size)
    resized_image.save(filename.split('.')[0] + "_resized.png")

def gaussian_blur_images(dir, kernel_size=(5, 5), sigma=0):
    for imgfile in os.listdir(dir):
        filename = os.path.join(dir, imgfile)
        if(filename.endswith('checkpoints')): continue
        print(filename)
        image = cv2.imread(filename)
        blurred_image = cv2.GaussianBlur(image, kernel_size, sigma)
        cv2.imwrite(os.path.join(dir, imgfile), blurred_image)

if __name__ == "__main__":
    city = "washington"
    dir = f"C:/Users/bachc/Downloads/{city}_real/Sem_seg"
    desired_threshold = 100
    convert_to_binary_dir(dir, desired_threshold)