import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llfp",
    version="0.0.3",
    author="JJTech0130",
    author_email="jjtech0130@outlook.com",
    description="Lutron LEAP for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JJTech0130/LLFP",
    classifiers=[
        "Development Status :: 3 - Alpha"
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
)


