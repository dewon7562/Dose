from setuptools import setup, find_packages

setup(
    name="dose",
    version="1.0.0",
    description="Dose DDoS Tool for educational purposes",
    author="Anonymous",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.1",
        "colorama>=0.4.5",
        "rich>=12.5.1",
        "scapy>=2.4.5"
    ],
    entry_points={
        "console_scripts": [
            "dose=dose.dose:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux"
    ]
)
