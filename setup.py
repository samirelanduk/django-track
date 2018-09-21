from setuptools import setup, find_packages

setup(
 name="django-track",
 version="0.1.0",
 description="A django app for doing analytics on site usage.",
 url="https://track.samireland.com",
 author="Sam Ireland",
 author_email="mail@samireland.com",
 license="MIT",
 classifiers=[
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Topic :: System :: Logging",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.5",
  "Programming Language :: Python :: 3.6",
  "Programming Language :: Python :: 3.7",
 ],
 keywords="django analytics logging",
 packages=find_packages(),
 include_package_data=True,
 install_requires=["django==2.0", "geoip2"]
)
