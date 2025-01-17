#!/usr/bin/env python3
import open3d as o3d
import numpy as np
import pytest


from pcd_loader import PcdLoader

# the testing data
TEST_DATA = {
    "simple": {
        "data": np.array(
            [
                [0, 0, 0],
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ],
            dtype=np.float64,
        ),
        "ascii": """# .PCD v0.7 - Point Cloud Data file format
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
""",
    },
    "repeating": {
        "data": np.array(
            [
                [0, 0, 1],
            ]
            * 1000,
            dtype=np.float64,
        ),
        "ascii": """# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH 1000
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS 1000
DATA ascii
"""
        + """0 0 1
"""
        * 1000,
    },
}


def create_test_pointcloud(type_name: str, data_name: str) -> str:
    """Fixture for creating fixed pointcloud.

    Args:
        type_name: whether the target is ascii or binary or binary_compressed
        data_name: name of the test data (in TEST_DATA)
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

    filename = f"./{type_name}_{data_name}.pcd"
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(TEST_DATA[data_name]["data"])

    print(f"save {pc} in {filename}")
    o3d.io.write_point_cloud(filename, pc, **setting_save[type_name])

    return filename


def check_values(filename: str, data_name: str):
    """Check whether the data is as expected.

    The point cloud points are predefined, it must be the same.

    Args:
        filename: input filename
        data_name: name of the test data (in TEST_DATA)
    """
    pc = o3d.io.read_point_cloud(filename)
    points = np.asarray(pc.points)
    assert np.abs(points - TEST_DATA[data_name]["data"]).max() < 1e-6


def check_ascii_file(filename: str, data_name: str):
    """Check whether the converted ascii is as expected.

    If fails assertion when the content is not the same; during checking,
    ".0" in the saved file wille be skipped.

    Args:
        filename: input filename
        data_name: name of the test data (in TEST_DATA)
    """
    with open(filename, "r", encoding="utf-8") as fi:
        content = fi.read().replace(".0 ", " ").replace(".0\n", "\n")

    assert content.strip() == TEST_DATA[data_name]["ascii"].strip()


@pytest.mark.parametrize(
    "type_name",
    [
        ("ascii"),
        ("binary"),
        ("binary_compressed"),
    ],
)
@pytest.mark.parametrize(
    "data_name",
    [
        ("simple"),
        ("repeating"),
    ],
)
def test_type(type_name: str, data_name: str):
    """Check for one pcd type.

    Args:
        type_name: whether the target is ascii or binary or binary_compressed
        data_name: name of the test data (in TEST_DATA)
    """
    # create
    filename = create_test_pointcloud(type_name=type_name, data_name=data_name)

    # read
    loader = PcdLoader(filename)

    loader.save_ascii(filename=f"test_ascii_{type_name}_{data_name}.pcd")
    check_ascii_file(
        filename=f"test_ascii_{type_name}_{data_name}.pcd", data_name=data_name
    )

    check_values(filename=filename, data_name=data_name)
    check_values(
        filename=f"test_ascii_{type_name}_{data_name}.pcd", data_name=data_name
    )
