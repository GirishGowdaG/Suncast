"""
SunCast - Day-Ahead Solar Power Forecasting
Setup configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="suncast",
    version="1.0.0",
    author="Girish G",
    author_email="",
    description="Day-ahead solar PV power forecasting using machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GirishGowdaG/suncast",
    project_urls={
        "Bug Tracker": "https://github.com/GirishGowdaG/suncast/issues",
        "Documentation": "https://github.com/GirishGowdaG/suncast#readme",
        "Source Code": "https://github.com/GirishGowdaG/suncast",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "scikit-learn",
        "pandas",
        "numpy",
        "joblib",
        "python-dotenv",
        "pydantic",
        "jinja2",
        "aiofiles",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "ruff",
        ],
    },
    entry_points={
        "console_scripts": [
            "suncast-generate=src.data_generator:main",
            "suncast-train=src.train:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "solar",
        "forecasting",
        "machine-learning",
        "renewable-energy",
        "photovoltaic",
        "prediction",
        "gradient-boosting",
        "fastapi",
    ],
    license="MIT",
)
