from rembg import remove
from PIL import Image

input_path = 'p22.jpg'
output_path = 'p22.png'
inp = Image.open(input_path)
output = remove(inp)
output.save(output_path)
