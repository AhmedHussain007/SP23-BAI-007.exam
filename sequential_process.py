import os, time
from PIL import Image, ImageDraw, ImageFont

input_dir = "dataset"
output_dir = "output_seq"
os.makedirs(output_dir, exist_ok=True)

start = time.time()

for cls in os.listdir(input_dir):
    cls_path = os.path.join(input_dir, cls)
    if not os.path.isdir(cls_path):
        continue
    save_path = os.path.join(output_dir, cls)
    os.makedirs(save_path, exist_ok=True)

    for img_name in os.listdir(cls_path):
        img_path = os.path.join(cls_path, img_name)
        try:
            img = Image.open(img_path).convert("RGBA")
            img = img.resize((128, 128))
            txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt)
            draw.text((10, 110), "WATERMARK", fill=(255, 255, 255, 128))
            watermarked = Image.alpha_composite(img, txt)
            watermarked.convert("RGB").save(os.path.join(save_path, img_name))
        except Exception as e:
            print(f"Error processing {img_name}: {e}")

print(f"Total execution time: {time.time() - start:.2f} seconds")
