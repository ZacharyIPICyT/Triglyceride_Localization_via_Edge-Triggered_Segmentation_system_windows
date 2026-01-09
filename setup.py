from setuptools import setup, find_packages

setup(
    name="triglyceride-analysis-system",
    version="1.0.0",
    author="Ing. Marco Zachary Moreno Bautista",
    description="Triglyceride Localization via Edge-Triggered Segmentation",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
        "pillow>=10.0.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Intended Audience :: Science/Research"
    ],
    entry_points={
        "console_scripts": [
            "triglyceride-analysis=src.main:main",
        ],
    },
)
