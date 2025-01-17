#!/usr/bin/env python3
import sys


from pcd_loader import PcdLoader

if len(sys.argv) <= 1 or sys.argv[1] in ("--help", "-h"):
    print("python conv_pcd.py input.pcd output.pcd")
    sys.exit(1)

path_in = sys.argv[1]
path_out = sys.argv[2]

PcdLoader(path_in).save_ascii(path_out)
