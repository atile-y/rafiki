#!/usr/bin/env python
import os
import unittest
import shutil
from raf.utils import mkdir_p, convert_lol_path
from raf.raf import RafArchive

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))


class TestExporting(unittest.TestCase):
	def setUp(self):
		self.archive = RafArchive(os.path.join(TEST_ROOT, "data", "Archive_194801136.raf"))
		self.tmp_dir = os.path.join(TEST_ROOT, 'tmp')
		mkdir_p(self.tmp_dir)

	def tearDown(self):
		pass
		shutil.rmtree(self.tmp_dir)

	def test_dogfooding(self):
		exported_raf_file = os.path.join(self.tmp_dir, 'exported.raf')
		for path, raf_file in self.archive.index.iteritems():
			data = raf_file.extract()
			data = data[:len(data) / 2] + "testword" + data[:len(data) / 2]
			raf_file.insert(data)
		self.archive.export(exported_raf_file)

		exported_archive = RafArchive(exported_raf_file)
		for path, raf_file in exported_archive.index.iteritems():
			data = raf_file.extract()
			self.assertEqual(data[len(data) / 2 - 4:(len(data) / 2) + 4], 'testword')
			self.assertEqual(data, self.archive.index[path].data)

	def test_content_read(self):
		file_name = "DATA/Menu/fontconfig_pl_PL.txt"
		self.assertIn(file_name, self.archive.index)
		raf_file = self.archive.index[file_name]
		raf_data = raf_file.extract()
		self.assertIn("karze wyzwiska homofobiczne czy rasowe", raf_data)

	def test_content_write(self):
		dummy_contents = "Hello Word"
		exported_raf_file = os.path.join(self.tmp_dir, 'minimap_export.raf')
		for path, raf_file in self.archive.index.iteritems():
			if(path.find("fontconfig_pl_PL") > -1):
				data = raf_file.extract()
				with open(os.path.join(self.tmp_dir, os.path.basename(convert_lol_path(path))), 'w') as f:
					f.write(dummy_contents)
				with open(os.path.join(self.tmp_dir, os.path.basename(convert_lol_path(path))), 'rb') as f:
					raf_file.insert(f.read())

		self.archive.export(exported_raf_file)
		exported_archive = RafArchive(exported_raf_file)
		for path, raf_file in exported_archive.index.iteritems():
			if(path.find("fontconfig_pl_PL") > -1):
				data = raf_file.extract()
				self.assertEqual(data, dummy_contents)