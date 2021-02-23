from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() + '\n\n' + open('CHANGELOG.txt').read()

setup(
    name="YSL-H-isaac23",
    version="1.1.2",
    author="John Isaac Delgado",
    author_email="dev.isaac23@gmail.com",
    description="A package for automated liking of Active YouTube Streams in the background using selenium and requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/H-isaac23/Youtube-Streams-Liker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['selenium', 'requests', 'mysql-connector-python'],
    python_requires='>=3.6'
)