from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="tg-error-notifier",
    version="1.0.0",
    author="Dusha",
    author_email="Ia12Kotik@yandex.ru",
    description="Telegram error notification library for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="telegram, error, notification, monitoring, logging",
    project_urls={
        "Bug Reports": "https://github.com/Dusha01/tg_error_notifier/issues",
        "Source": "https://github.com/Dusha01/tg_error_notifier",
    },
)