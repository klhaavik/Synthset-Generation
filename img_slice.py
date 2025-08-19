import os
from PIL import Image
from pathlib import Path
home = Path.home()

def slice_image_with_overlap(image_path, output_dir, slice_size=(256, 256), overlap=(32, 32), iteration=0):
    """
    Slices an image into patches of given size with specified pixel overlap.

    Args:
        image_path (str): Path to the input image.
        output_dir (str): Directory to save the slices.
        slice_size (tuple): (width, height) of each slice in pixels.
        overlap (tuple): (overlap_x, overlap_y) in pixels.
    """
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)
    width, height = img.size
    slice_w, slice_h = slice_size
    overlap_x, overlap_y = overlap

    step_x = slice_w - overlap_x
    step_y = slice_h - overlap_y

    count = 0
    row = 0
    y = 0
    while y < height:
        x = 0
        col = 0
        while x < width:
            left = x
            upper = y
            right = min(left + slice_w, width)
            lower = min(upper + slice_h, height)

            # Adjust box if it goes out of bounds
            if right - left < slice_w:
                left = max(0, right - slice_w)
            if lower - upper < slice_h:
                upper = max(0, lower - slice_h)

            box = (left, upper, right, lower)
            slice_img = img.crop(box)
            slice_filename = os.path.join(output_dir, f"slice_{row}_{col}_{iteration}.png")
            slice_img.save(slice_filename)
            count += 1

            x += step_x
            col += 1
        y += step_y
        row += 1

    print(f"Saved {count} slices to {output_dir}")

def slice_all_images_in_dir(input_dir, output_dir, slice_size, overlap):
    counter = 0
    for img_file in os.listdir(input_dir):
        if img_file.endswith(".png"):
            image_path = os.path.join(input_dir, img_file)
            output_dir = f"data/output_slices/{img_type}"
            slice_image_with_overlap(image_path, output_dir, slice_size=(256, 256), overlap=(32, 32), iteration=counter)
            counter += 1

if __name__ == "__main__":
    user = "haavik.2" #Update as needed
    city = "washington" #Update as needed
    img_type = "Sem_seg" #Update as needed
    render_engine = "Cycles" #Update as needed

    input_dir = f"C:/Users/{user}/Documents/GitHub/Synthset-Generation/Blender/{city}/Images/{render_engine}/{img_type}"
    output_dir = f"C:/Users/{user}/Documents/GitHub/Synthset-Generation/{city}/output_slices"
    slice_all_images_in_dir(input_dir, output_dir, slice_size=(256, 256), overlap=(32, 32))

