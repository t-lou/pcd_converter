import open3d as o3d
import numpy as np
import shutil

from pcd_loader import PcdLoader


def create_test_pointcloud(type_name: str) -> str:
    print(f"start with {type_name}")
    setting_save = {
        "ascii": {
            "write_ascii": True,
        },
        "binary": {
            "write_ascii": False,
            "compressed": False,
        },
        "binary_compressed": {
            "write_ascii": False,
            "compressed": True,
        },
    }

    points = np.array(
        [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
        dtype=np.float64,
    )

    filename = f"./{type_name}.pcd"
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(points)

    print(f"save {pc} in {filename}")
    o3d.io.write_point_cloud(filename, pc, **setting_save[type_name])

    return filename


def check_ascii_file(filename: str):
    answer = """# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH 4
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS 4
DATA ascii
0 0 0
1 0 0
0 1 0
0 0 1
"""
    with open(filename, "r", encoding="utf-8") as fi:
        content = fi.read().replace(".0 ", " ").replace(".0\n", "\n")

    print(content)
    print(answer)
    assert content.strip() == answer.strip()


def test_type(type_name: str):
    filename = create_test_pointcloud(type_name=type_name)

    loader = PcdLoader(filename)

    loader.save_ascii("test_ascii.pcd")
    check_ascii_file("test_ascii.pcd")


test_type(type_name="ascii")
test_type(type_name="binary")
test_type(type_name="binary_compressed")
