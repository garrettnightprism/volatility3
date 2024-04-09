import os
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--volatility",
        action="store",
        required=True,
        help="Path to the volatility script",
    )

    parser.addoption(
        "--python",
        action="store",
        default="python3",
        help="Name of the interpreter to use when running the volatility script",
    )

    parser.addoption(
        "--image", action="append", default=[], help="Path to an image to test"
    )

    parser.addoption(
        "--image-dir",
        action="append",
        default=[],
        help="Path to a directory containing images to test",
    )


def pytest_generate_tests(metafunc):
    """Parameterize tests based on image names"""

    images = metafunc.config.getoption("image")
    for image_dir in metafunc.config.getoption("image_dir"):
        images += [
            os.path.join(image_dir, filename) 
            for filename in os.listdir(image_dir)
        ]

    # Tests with "image" parameter are run against images
    if "image" in metafunc.fixturenames:
        metafunc.parametrize(
            "image", images, ids=[os.path.basename(image) for image in images]
        )


# Fixtures
@pytest.fixture
def volatility(request):
    return request.config.getoption("--volatility")


@pytest.fixture
def python(request):
    return request.config.getoption("--python")
