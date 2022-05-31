from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SAG Recommender",
    version="0.9.5",
    description="Working",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 0.9.5 - Ready to count test matrix",
        "License :: OSI Approved :: Lesser General Public License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Machine Learning :: Graph Search",
        "Operating System :: OS Independent",
    ],
    keywords="",
    url="https://github.com/zer0deck/SARS-Avatar",
    author="@zer0deck/Aleksey Grandilevskii",
    author_email="zer0deck@icloud.com",
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.22.2",
        "pandas>=1.2.1",
        "nltk>=3.6.7",
        "pymorphy2>=0.9.1",
        "gensim>=4.1.2",
    ],
    include_package_data=True,
    zip_safe=False,
)
