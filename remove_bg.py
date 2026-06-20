from PIL import Image

img = Image.open('assets/logo.png').convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    # Calculate brightness
    brightness = max(item[0], item[1], item[2])
    
    # Set alpha based on brightness to preserve the soft neon glow
    newData.append((item[0], item[1], item[2], brightness))

img.putdata(newData)
img.save("assets/logo.png", "PNG")
print("Background removed from image.")
