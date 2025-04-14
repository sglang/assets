import os
import glob
import cairosvg
from PIL import Image

RESOLUTIONS = [
	(1920, 1920),
	(1280, 1280),
	(640, 640)
]

OUTPUT_DIR = "out"
SVG_DIR = ".."
FORMATS = ["png", "jpg"]

def ensure_dir(directory):
	os.makedirs(directory, exist_ok=True)

def convert_svg_to_png(svg_path, output_path, width, height):
	cairosvg.svg2png(
		url=svg_path,
		write_to=output_path,
		output_width=width,
		output_height=height
	)

def convert_png_to_jpg(png_path, jpg_path):
	img = Image.open(png_path)
	if img.mode in ('RGBA', 'LA'):
		background = Image.new('RGB', img.size, (255, 255, 255))
		background.paste(img, mask=img.split()[3])
		img = background
	img.save(jpg_path, 'JPEG', quality=90)

def process_svg(svg_path):
	print(f"Processing {svg_path}...")
	
	svg_basename = os.path.basename(svg_path)
	name_without_ext = os.path.splitext(svg_basename)[0]
	
	for width, height in RESOLUTIONS:
		resolution_dir = f"{width}x{height}"
		
		for fmt in FORMATS:
			output_dir = os.path.join(OUTPUT_DIR, name_without_ext, resolution_dir, fmt)
			ensure_dir(output_dir)
			
			output_filename = f"{name_without_ext}.{fmt}"
			output_path = os.path.join(output_dir, output_filename)
			
			if fmt == "png":
				convert_svg_to_png(svg_path, output_path, width, height)
			elif fmt == "jpg":
				png_temp_path = os.path.join(output_dir, f"{name_without_ext}.temp.png")
				convert_svg_to_png(svg_path, png_temp_path, width, height)
				convert_png_to_jpg(png_temp_path, output_path)
				os.remove(png_temp_path)
	
	print(f"Finished processing {svg_path}")

def main():
	ensure_dir(OUTPUT_DIR)
	
	svg_files = glob.glob(os.path.join(SVG_DIR, "*.svg"))
	
	if not svg_files:
		print("No SVG files found in the current directory.")
		return
	
	print(f"Found {len(svg_files)} SVG files")
	
	for svg_file in svg_files:
		process_svg(svg_file)
	
	print("All SVG files processed successfully!")

if __name__ == "__main__":
	main()
