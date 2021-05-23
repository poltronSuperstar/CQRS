from distutils.core import setup


packages = [
    "CQRS",
    ".",
]


setup(
    name="CQRS",
    version="0.0.1",
    description="CQRS in Python",
    author="me",
    url="https://github.com/poltronSuperstar/CQRS",
    license="BSD-3-Clause",
    packages=packages,
    #package_data={"CQRS": ["py.typed"]},
    package_dir = {"":"."},
    install_requires=[],
    extras_require= {"toolz":"toolz<=0.99.99"},
    
    zip_safe=False,
    long_description="WIP WIP WIP",
    keywords=[
        "cqrs",
        "cqs",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
