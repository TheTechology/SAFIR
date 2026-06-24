from setuptools import setup, find_packages

setup(
    name="safir-irrigation",
    version="0.1.0",
    description="SAFIR: AI-driven irrigation monitoring for climate resilience in Laos",
    author="SAFIR Project",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pydantic",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "safir=safir.cli:main",
        ],
    },
)
