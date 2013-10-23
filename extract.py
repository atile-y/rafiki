#!/usr/bin/env python
import os
import sys
import argparse

from raf import RafCollection
from utils import mkdir_p, convert_lol_path



parser = argparse.ArgumentParser(description='Extract or Pack files from/to Riot Archive Format, optionally filtering extracted file paths')
parser.add_argument('action',
	metavar='action',
	type=str,
	choices=['extract', 'pack'],
	help='This is the desired action, either extract or pack'
)

parser.add_argument('-s',
	dest="source_path",
	required=True,
	help="Path to Leauge of Legends installation, required for both extracting and packaging. Will never be overriden or written to."
)

parser.add_argument('-o',
	dest='out_path',
	default=None,
	help='Target directory where extracted/packed files are places. **Existing files will be overwritten**'
)

parser.add_argument('-f',
	dest="filter",
	default=None,
	help="Only extract files with path containing **string**"
)

parser.add_argument("-r",
	dest="override",
	default=None,
	help="**When packaging up RAFs looks for a matching paths for overrides. If found an override will be packed in instead of the original file"
)

args = parser.parse_args()

basepath = "extracted"
if(not os.path.isdir(args.source_path)):
	print('"%s" is not a directory, please provide full path to LOL' % args.source_path)
	sys.exit()

collection = RafCollection(args.source_path)
if(args.filter):
	files = collection.search("hud2012")
else:
	files = collection.index.values()
# for raf_file in files:
# 	data = raf_file.extract()
# 	raf_file_path = convert_lol_path(raf_file.path)
# 	mkdir_p(basepath + os.sep + os.path.dirname(raf_file_path))
# 	with open(basepath + os.sep + raf_file_path, 'wb') as target_file:
# 		target_file.write(data)