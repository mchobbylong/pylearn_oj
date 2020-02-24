from versatileimagefield.versatileimagefield import CroppedImage
from versatileimagefield.datastructures.sizedimage import SizedImage
from versatileimagefield.registry import versatileimagefield_registry
from PIL import Image

class ThumbCropImage(CroppedImage):
	"""
	Resize an image first, then crop
	"""
	filename_key = 'thumbcrop'

	def process_image(self, image, image_format, save_kwargs,
					  width, height):
		old_width, old_height = image.size
		ratio = max(width / old_width, height / old_height)
		image.resize((round(old_width*ratio), round(old_height*ratio)), resample=Image.LANCZOS)
		return super().process_image(
			image,
			image_format,
			save_kwargs,
			width,
			height,
		)

versatileimagefield_registry.register_sizer('thumbcrop', ThumbCropImage)
