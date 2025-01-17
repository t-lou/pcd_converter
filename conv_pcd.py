#!/usr/bin/env python3

import sys
import argparse

from pcd_loader import PcdLoader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="conv_pcd", description="convert pcd to ascii format"
    )
    parser.add_argument("path_in")
    parser.add_argument("path_out")

    args = parser.parse_args()
    data = PcdLoader(args.path_in)
    print(data)
    data.save_ascii(args.path_out)

else:
    print("oops, not a dep")
    sys.exit(1)
