from setuptools import setup, find_packages

with open("VERSION.txt", "r", encoding="utf-8") as f:
    version = f.read().strip()

setup(
    name="idsideai",
    version=version,
    description="idsideAI application",
    packages=find_packages(exclude=("tests", "qc", "docs", ".github")),
    include_package_data=True,
    install_requires=["fastapi", "uvicorn", "sqlmodel", "requests"],
    python_requires=">=3.11",
)
