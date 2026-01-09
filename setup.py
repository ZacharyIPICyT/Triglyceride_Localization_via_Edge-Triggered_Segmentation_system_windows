from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="triglyceride-analysis-system",
    version="1.0.0",
    author="Marco Zachary Moreno Bautista",
    author_email="marco.moreno@ipicyt.edu.mx",
    description="Triglyceride Localization via Edge-Triggered Segmentation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZacharyIPICyT/Triglyceride_Localization_via_Edge-Triggered_Segmentation_system_windows",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
        "scipy>=1.11.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pyinstaller>=5.13.0",
            "pywin32>=306",
            "twine>=4.0.0",
            "wheel>=0.40.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "triglyceride-analysis=main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/ZacharyIPICyT/Triglyceride_Localization_via_Edge-Triggered_Segmentation_system_windows/issues",
        "Source": "https://github.com/ZacharyIPICyT/Triglyceride_Localization_via_Edge-Triggered_Segmentation_system_windows",
        "IPICYT": "https://www.ipicyt.edu.mx/",
    },
)
