import os
import time
from PIL import Image, ImageDraw
from multiprocessing import Pool

input_dir = "dataset"
output_dir = "output_parallel"
os.makedirs(output_dir, exist_ok=True)

def process_image(args):
    cls, img_name = args
    in_path = os.path.join(input_dir, cls, img_name)
    out_path = os.path.join(output_dir, cls, img_name)
    try:
        img = Image.open(in_path).convert("RGBA").resize((128, 128))
        txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
        ImageDraw.Draw(txt).text((10, 110), "WATERMARK", fill=(255, 255, 255, 128))
        Image.alpha_composite(img, txt).convert("RGB").save(out_path)
    except Exception:
        pass

def run_parallel(workers):
    for cls in os.listdir(input_dir):
        os.makedirs(os.path.join(output_dir, cls), exist_ok=True)

    all_imgs = [(cls, img) for cls in os.listdir(input_dir)
                if os.path.isdir(os.path.join(input_dir, cls))
                for img in os.listdir(os.path.join(input_dir, cls))]

    start = time.perf_counter()
    with Pool(processes=workers) as pool:
        pool.map(process_image, all_imgs)
    return time.perf_counter() - start

if __name__ == "__main__":
    print(f"CPU cores available: {os.cpu_count()}")
    times = {}
    for w in [1, 2, 4, 8]:
        t = run_parallel(w)
        times[w] = t
        print(f"Workers: {w}, Time: {t:.2f}s")

    base = times[1]
    print("\nWorkers | Time (s) | Speedup")
    print("--------|----------|---------")
    for w, t in times.items():
        print(f"{w:<7} | {t:<8.2f} | {base/t:.2f}x")
