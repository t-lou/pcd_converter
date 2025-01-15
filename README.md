## load and convert one PCD file without dependency

minimal example for converting binary to ascii

```
python -m pytest test_pcd_loader.py
python conv_pcd.py binary_compressed.pcd binary_compressed_to_ascii.pcd
python conv_pcd.py binary.pcd binary_to_ascii.pcd
```