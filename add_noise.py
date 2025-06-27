import os
import argparse
from PIL import Image
import numpy as np

def remove_noise(args):
    image = Image.open(args.input_dir).convert("RGB")
    image_np = np.array(image).astype(np.float32)
    normalized = False
    if image_np.max() > 1.0:
        image_np /= 255.0
        normalized = True
    noise = np.random.normal(args.mean, args.std, image_np.shape)
    noisy_image_np = image_np + noise
    noisy_image_np = np.clip(noisy_image_np, 0.0, 1.0)
    if normalized:
        noisy_image_np *= 255.0
    noisy_image_np = noisy_image_np.astype(np.uint8)
    noisy_image = Image.fromarray(noisy_image_np)
    output_dir = os.path.join(args.output_dir, os.path.basename(args.input_dir))
    noisy_image.save(output_dir)
    noisy_image.show()
    print('Saved noise image to:', output_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='datasets/HQ_face/00001.jpg')
    parser.add_argument('--output_dir', type=str, default='datasets/LQ_face')
    parser.add_argument('--mean', type=float, default=0.0)
    parser.add_argument('--std', type=float, default=0.3)
    args = parser.parse_args()

    print('Adding noise for image:', args.input_dir)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    remove_noise(args)