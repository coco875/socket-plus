import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="socket-plus",
    version="0.0.2",
    author="coco875",
    author_email="pereira.jannin@gmail.com",
    description="A librairie in python to comunicate more efficiently possible with structures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coco875/socket-plus",
    project_urls={
        "Bug Tracker": "https://github.com/coco875/socket-plus/issues",
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
