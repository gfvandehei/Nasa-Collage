from setuptools import setup, find_packages

setup(
    name="NasaPictureTrawler",
    version="0.0.1",
    author="Gabriel Vande Hei",
    author_email="gfvandehei@gmail.com",
    description="A python wrapper for the NASA image API",
    url="https://github.com/gfvandehei/Nasa-Collage.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)