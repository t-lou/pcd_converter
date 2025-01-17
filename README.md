## load and convert one PCD file without dependency

This script can be used to
1. load one pcd to a primary python structure
    - elements in int or float
    - primary python lists, groupped by field names
2. convert one pcd file, either binary or binary_compressed, to ascii

minimal example for converting binary to ascii, please note that there might be a lot of stdout

```bash
python -m pytest test_pcd_loader.py
python conv_pcd.py binary_compressed_repeating.pcd binary_compressed_to_ascii.pcd
python conv_pcd.py binary_simple.pcd binar_to_ascii.pcd
```

Feel to delete any pcd file `rm *.pcd` or delete strange files `git clean -df`, this code is std-python only.