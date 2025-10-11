# Copy this content to setup.py
from setuptools import setup, find_packages

setup(
    name="hand-gesture-mouse-control",
    version="1.0.0",
    author="Akash",
    author_email="kushawahaakash01@gmail.com",
    description="AI-powered hand gesture recognition for mouse control",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://https://github.com/Akashkushawaha/hand-gesture-mouse-control",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5.0",
        "mediapipe>=0.8.0",
        "pyautogui>=0.9.50",
        "numpy>=1.21.0",
        "pillow>=8.0.0",
    ],
)