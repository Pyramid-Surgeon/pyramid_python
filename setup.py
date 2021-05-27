import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyramid_python",
    version="0.0.2",
    author="Pyramid Surgeon",
    author_email="n/a",
    description="Repository of Python scripts made during CTFs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pyramid-Surgeon/pyramid_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'gmpy2',
        'pycryptodome',
        'PyJWT',
        'cryptography'
      ],
    python_requires='>=3.8',
)
