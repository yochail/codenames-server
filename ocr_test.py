import unittest
from os import path

from PIL import Image
import ocr


class MyTestCase(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(MyTestCase, self).__init__(*args, **kwargs)
		self.img_path = "./data/img"

	def test_find_all_white_squers_eng(self):
		eng_test_files = ["1.jpg","3.jpg","4.jpg","5.jpg","7.jpg"]
		for file in eng_test_files:
			image = Image.open(path.join(self.img_path,file))
			images_rest = ocr.find_white_squers(image)
			self.assertGreaterEqual(len(images_rest),25,file)

	def test_find_all_white_squers_he(self):
		heb_test_files = ["8he.jpg","9he.jpg"]
		file = "8he.jpg"
		image = Image.open(path.join(self.img_path,file))
		images_rest = ocr.find_white_squers(image)
		self.assertGreaterEqual(len(images_rest),25,file)

		file = "9he.jpg"
		image = Image.open(path.join(self.img_path, file))
		images_rest = ocr.find_white_squers(image)
		self.assertGreaterEqual(len(images_rest), 8, file)

if __name__ == '__main__':
	unittest.main()
