#!/usr/bin/env python3
#
# recursive_conversion --- Concatenates and converts a directory tree recursively
#
# This script is useful for concatenating multiple series of DICOM files from
# e.g. multiple runs of an MRI machine. Assuming that different DICOM series
# are stored in subdirectories of the form Data/2011/STUD01/SER??, you could
# call the script as follows:
#
# ./recursive_conversion.py Data/2011/STUD01
#
# The result will be a series of files that are named SER??_x_y_z_b[u|s], where
# x, y, and z refer to the dimensions of the concatenated raw DICOM volume, b
# contains the number of bits for representing a single entry, and u|s
# indicates whether data is (un)signed.
#
# Copyright (c) 2014 Bastian Rieck
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

from dicomcat import *

import re
import os
import string


def usage():
	print("Usage: recursive_conversion.py FILE", file=sys.stderr)


def sort_files_accroding_index(file_names):
	file_names_map = {}
	files_path = os.path.os.path.dirname(file_names[0])
	print(files_path)
	for f in file_names:
		file_name = os.path.split(f)[-1]

		symbol = re.match(r'^\D+', file_name)
		digit = re.search(r'\d+$', file_name)

		if digit is not None and symbol is not None:
			file_names_map[string.atoi(digit.group())] = symbol.group()
		else:
			error_msg = str.format('error, the file %s do not have a common header with other files', f)
			print(error_msg)

	sorted_list = []
	for key in sorted(file_names_map.iterkeys()):
		sorted_name = file_names_map[key] + str(key)
		f = os.path.join(files_path, sorted_name)
		sorted_list.append(f)
	return sorted_list


def main():
	if len(sys.argv) != 2:
		usage()
		sys.exit(-1)

	for directory, subdirectories, files in os.walk(sys.argv[1], topdown=False):
		if files:
			prefix = os.path.basename(directory)
			# filenames = [str(os.path.join(directory, x)) for x in sorted(files)]
			file_names = [str(os.path.join(directory, x)) for x in sort_files_accroding_index(files)]
			# connvert_dicom_2_raw_with_check(prefix, filenames, True)
			# file_names = sort_files_accroding_index(files)
			connvert_dicom_2_raw_with_check(prefix, file_names, True)
		# subprocess.call(["./dicomcat.py", "--check", "--prefix", prefix] + filenames)


if __name__ == '__main__':
	main()
