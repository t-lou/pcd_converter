import sys


from pcd_loader import PcdLoader

path_in = sys.argv[1]
path_out = sys.argv[2]

PcdLoader(path_in).save_ascii(path_out)
