import open3d as o3d
import numpy as np
import pytest


from pcd_loader import PcdLoader

POINTS = np.array(
    [
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ],
    dtype=np.float64,
)


def create_test_pointcloud(type_name: str) -> str:
    """Fixture for creating fixed pointcloud.

    Args:
        type_name: whether the target is ascii or binary or binary_compressed
    """
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

    filename = f"./{type_name}.pcd"
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(POINTS)

    print(f"save {pc} in {filename}")
    o3d.io.write_point_cloud(filename, pc, **setting_save[type_name])

    return filename


def check_values(filename: str):
    """Check whether the data is as expected.

    The point cloud points are predefined, it must be the same.

    Args:
        filename: input filename
    """
    pc = o3d.io.read_point_cloud(filename)
    points = np.asarray(pc.points)
    assert np.abs(points - POINTS).max() < 1e-6


def check_ascii_file(filename: str):
    """Check whether the converted ascii is as expected.

    If fails assertion when the content is not the same; during checking,
    ".0" in the saved file wille be skipped.

    Args:
        filename: input filename
    """
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


@pytest.mark.parametrize(
    "type_name",
    [
        ("ascii"),
        ("binary"),
        ("binary_compressed"),
    ],
)
def test_type(type_name: str):
    """Check for one pcd type.

    Args:
        type_name: whether the target is ascii or binary or binary_compressed
    """
    filename = create_test_pointcloud(type_name=type_name)

    loader = PcdLoader(filename)

    loader.save_ascii("test_ascii.pcd")
    check_ascii_file("test_ascii.pcd")

    check_values(filename)
    check_values("test_ascii.pcd")
