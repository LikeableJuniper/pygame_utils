import setuptools

setuptools.setup(
    name="pygame_utils_likeablejuniper",
    version="0.2.0",
    description="Package which provides some basic GUI elements for pygame",
    url="https://github.com/LikeableJuniper/pygame_utils",
    author="LikeableJuniper",
    license="MIT License",
    packages=["pygame_utils_likeablejuniper", "pygame_utils_likeablejuniper/core"],
    install_requires=[
        "pygame-ce",
        "vectors_likeablejuniper"
    ]
)