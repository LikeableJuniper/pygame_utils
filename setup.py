import setuptools

setuptools.setup(
    name="pygame_utils_likeablejuniper",
    version="0.4.0",
    description="Package which provides some basic GUI elements for pygame",
    long_description=open("README.md", "r").read(),
    url="https://github.com/LikeableJuniper/pygame_utils",
    author="LikeableJuniper",
    license="MIT License",
    packages=[
        "pygame_utils_likeablejuniper",
        "pygame_utils_likeablejuniper/core",
        "pygame_utils_likeablejuniper/element",
        "pygame_utils_likeablejuniper/layout",
        "pygame_utils_likeablejuniper/style"
    ],
    install_requires=[
        "pygame-ce",
        "vectors_likeablejuniper"
    ]
)