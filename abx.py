# Android Backup Extractor
# Copyright (C) 2014 InFo-Lab
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# Lesser General Public License as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not,
# write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

# coding=utf-8

import argparse
import os
import sys
import zlib

# Android Backup description: 
# http://nelenkov.blogspot.com.ar/2012/06/unpacking-android-backups.html

C_BUFFER_SIZE = 1048576


def ArgParse():
    """
    Parses the command line arguments

    :return: argparse dictionary
    """
    parser = argparse.ArgumentParser(
        description="xbackup: extracts an Android ICS+ backup file.")
    parser.add_argument("ipath",
                        help="Input path.")
    parser.add_argument("opath",
                        help="Output path.")
    return parser.parse_args()


def Extract(args):
    """
    Extracts the .tar file of an Android Backup. Assumes the backup is not encrypted and is
    compressed.

    :param args:
    :return:
    """
    with open(args.ipath, "rb") as ifile, open(args.opath, "wb") as ofile:
        data = ifile.read(C_BUFFER_SIZE)
        pos = data.find(b"none\n") + 5  # Change to bytes
        if pos < 5:
            print("Error: Backup file format not recognized.")
            return 1
        data = data[pos:]
        dc = zlib.decompressobj()
        while data:
            ofile.write(dc.decompress(data))
            data = ifile.read(C_BUFFER_SIZE)
    return 0


def main():
    args = ArgParse()
    if os.path.isfile(args.ipath):
        return Extract(args)
    else:
        print("Could not open input file!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
