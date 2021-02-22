from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() + open('CHANGELOG.txt').read()

setup(
    name="YSL-H-isaac23", # Replace with your own username
    version="1.0.0",
    author="John Isaac Delgado",
    author_email="dev.isaac23@gmail.com",
    description="A package for automated liking of Active YouTube Streams in the background.",
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