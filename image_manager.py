import io
from tkinter import filedialog
from PIL import Image

def attach_image():
    image_title = input("Image title: ").lower()
    image_description = input("Image description: ")
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a file.", filetypes = (("jpg files", "*.jpg"), ("png files", "*.png"), ("jpeg files", "*.jpeg"), ("pdf files", "*.pdf")))
    image = open(filename, "rb")
    image_bytes = image.read()
    return image_title, image_description, image_bytes

def read_image(byteform):
    img = Image.open(io.BytesIO(byteform))
    img.show()
    return