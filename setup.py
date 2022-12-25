from setuptools import setup, find_packages
from os.path import isfile, join
from os import environ
from logging import getLogger
logger=getLogger(__name__)
warning=logger.warning

if environ.get("LITREPL_ROOT",None):
  LITREPL_ROOT=environ["LITREPL_ROOT"]
else:
  LITREPL_ROOT='.'

if environ.get("LITREPL_VERSION",None):
  LITREPL_VERSION=environ["LITREPL_VERSION"]
  SETUPTOOLS_SCM_FOUND=False
else:
  try:
    from setuptools_scm import get_version
    LITREPL_VERSION=get_version(root=LITREPL_ROOT)
    SETUPTOOLS_SCM_FOUND=True
  except ImportError:
    warning('`setuptool_scm` package not found, version is set to None')
    LITREPL_VERSION='9999'
    SETUPTOOLS_SCM_FOUND=False

with open(join('python','litrepl','version.py'), 'w') as f:
  f.write("# AUTOGENERATED!\n")
  f.write(f"__version__ = '{LITREPL_VERSION}'\n")

def local_scheme(version):
  return ""

setup(
  name="litrepl",
  zip_safe=False, # https://mypy.readthedocs.io/en/latest/installed_packages.html
  use_scm_version={
    "root": LITREPL_ROOT,
    "local_scheme": local_scheme,
  },
  package_dir={'':'python'},
  packages=find_packages(where='python'),
  install_requires=['lark'],
  setup_requires=['setuptools_scm'] if SETUPTOOLS_SCM_FOUND else [],
  scripts=['./python/bin/litrepl'],
  python_requires='>=3.6',
  author="Sergei Mironov",
  author_email="grrwlf@gmail.com",
  description="LitREPL a macroprocessing Python library for Litrate "\
              "programming and code execution.",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: POSIX :: Linux",
    "Topic :: Software Development :: Build Tools",
    "Intended Audience :: Developers",
    "Development Status :: 3 - Alpha",
  ],
)

