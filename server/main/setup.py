from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("karrio/server/VERSION", "r") as v:
    version = v.read().strip()

setup(
    name="karrio.server",
    version=version,
    description="Multi-carrier shipping API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio-server",
    author="karrio",
    author_email="danielk.developer@gmail.com",
    license="Apache License Version 2.0",
    packages=find_namespace_packages("."),
    install_requires=[
        "django",
        "djangorestframework",
        "djangorestframework-simplejwt",
        "django-constance",
        "django-filter",
        "django-picklefield",
        "django-email-verification",
        "django-cors-headers",
        "django-redis",
        "drf-api-tracking",
        "drf-yasg",
        "gunicorn",
        "hiredis",
        "uvicorn",
        "jsonfield",
        "more-itertools",
        "requests",
        "python-decouple",
        "karrio.server.core",
    ],
    entry_points={"console_scripts": ["karrio = karrio.server.__main__:main"]},
    dependency_links=[
        "https://git.io/karrio",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False,
    include_package_data=True,
)
