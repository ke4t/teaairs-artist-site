from PIL import Image

orig_path = '/Users/ke4t/.gemini/antigravity/brain/36b3ccfa-b634-4a1e-be7d-6c2a22b771f3/tea_neon_logo_1781889527426.png'
img = Image.open(orig_path).convert("RGBA")
datas = img.getdata()

newData = []
# Anything below this brightness is considered background texture/noise
threshold = 45

for item in datas:
    brightness = max(item[0], item[1], item[2])
    
    if brightness < threshold:
        # Completely transparent
        newData.append((0, 0, 0, 0))
    else:
        # Smoothly map the remaining brightness to alpha so the neon glow fades out softly
        alpha = int((brightness - threshold) * (255 / (255 - threshold)))
        newData.append((item[0], item[1], item[2], alpha))

img.putdata(newData)
img.save("assets/logo.png", "PNG")
print("Cleaned up logo texture.")
