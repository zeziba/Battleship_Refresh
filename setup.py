import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Battleship_revisited",
    version="0.0.1",
    author="Charles Engen",
    author_email="owenengen@gmail.com",
    description="Battleship the Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeziba/Battleship_revisited",
    project_urls={
        "Bug Tracker": "https://github.com/zeziba/Battleship_revisited/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
