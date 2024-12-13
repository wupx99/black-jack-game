from PIL import Image, ImageDraw
import os

def add_rounded_corners(image, radius):
    """
    Add rounded corners to an image.
    
    :param image: The original image.
    :param radius: The radius of the rounded corners.
    :return: A new image with rounded corners.
    """
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
    result = Image.new('RGBA', image.size, (0, 0, 0, 0))
    result.paste(image, mask=mask)
    return result

def add_black_border(image, border_width, border_color=(0, 0, 0)):
    """
    Add a black border to an image.
    
    :param image: The original image.
    :param border_width: The width of the border.
    :param border_color: The color of the border (default is black).
    :return: A new image with a black border.
    """
    new_size = (image.width + 2 * border_width, image.height + 2 * border_width)
    new_image = Image.new('RGBA', new_size, border_color)
    new_image.paste(image, (border_width, border_width))
    return new_image

def process_images_in_folder(folder_path, output_folder, radius, border_width, border_color=(0, 0, 0)):
    """
    Process all PNG images in a folder to add rounded corners and a black border,
    and save them to a new folder.
    
    :param folder_path: The path to the folder containing the images.
    :param output_folder: The path to the folder where processed images will be saved.
    :param radius: The radius of the rounded corners.
    :param border_width: The width of the border.
    :param border_color: The color of the border (default is black).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            file_path = os.path.join(folder_path, filename)
            with Image.open(file_path) as img:
                img = add_rounded_corners(img, radius)
                img = add_black_border(img, border_width, border_color)
                output_file_path = os.path.join(output_folder, filename)
                img.save(output_file_path)  # Save the modified image to the new folder

# 使用示例
folder_path = 'cards'
output_folder = 'card_new'
radius = 20  # 圆角半径
border_width = 5  # 边框宽度
process_images_in_folder(folder_path, output_folder, radius, border_width)