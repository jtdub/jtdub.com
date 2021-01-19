import pytest
import os


@pytest.fixture
def posts_path():
    CWD = os.getcwd()
    PATH = CWD.split("/")
    PATH.append("_posts")
    PATH = "/".join(PATH)
    FILES = os.listdir(PATH)

    return {"path": PATH, "files": FILES}
