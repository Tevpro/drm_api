import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oracle_drm_api",
    version="0.1.0",
    author="Keith Kikta",
    author_email="keith.kikta@tevpro.com",
    description="Oracle Data Relationship Management API Client",
    long_description=long_description,
    url="https://github.com/tevpro/drm_api",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'zeep>=2.5.0',
    ]
)
