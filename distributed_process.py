import os, time
from PIL import Image, ImageDraw
from multiprocessing import Process, Manager

input_dir = "dataset"
output_dir = "output_distributed"
os.makedirs(output_dir, exist_ok=True)

def process_images(images, node_id, results):
    start = time.time()
    for cls, img_name in images:
        in_path = os.path.join(input_dir, cls, img_name)
        out_cls = os.path.join(output_dir, cls)
        os.makedirs(out_cls, exist_ok=True)
        try:
            img = Image.open(in_path).convert("RGBA").resize((128, 128))
            txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
            ImageDraw.Draw(txt).text((10, 110), "WATERMARK", fill=(255, 255, 255, 128))
            Image.alpha_composite(img, txt).convert("RGB").save(os.path.join(out_cls, img_name))
        except Exception:
            pass
    results[node_id] = time.time() - start

if __name__ == "__main__":
    # Collect all image paths
    all_images = []
    for cls in os.listdir(input_dir):
        cls_path = os.path.join(input_dir, cls)
        if not os.path.isdir(cls_path): continue
        for img_name in os.listdir(cls_path):
            all_images.append((cls, img_name))

    half = len(all_images) // 2
    node1_imgs, node2_imgs = all_images[:half], all_images[half:]

    manager = Manager()
    results = manager.dict()

    start_total = time.time()
    p1 = Process(target=process_images, args=(node1_imgs, 1, results))
    p2 = Process(target=process_images, args=(node2_imgs, 2, results))

    p1.start(); p2.start()
    p1.join(); p2.join()
    total_time = time.time() - start_total

    n1_time, n2_time = results[1], results[2]
    print(f"Node 1 processed {len(node1_imgs)} images in {n1_time:.2f}s")
    print(f"Node 2 processed {len(node2_imgs)} images in {n2_time:.2f}s")
    print(f"Total distributed time: {total_time:.2f}s")

    seq_time = 18.24  # Replace with your sequential time
    print(f"Efficiency: {seq_time / total_time:.2f}x over sequential")
