# -*- coding:utf-8 -*-
###
# File: setup.py
# Created Date: Thursday, June 15th 2023, 9:51:16 am
# Author: iYuqinL
# -----
# Last Modified: Thu Jun 15 2023
# Modified By: iYuqinL
# -----
# Copyright © 2023 iYuqinL Holding Limited
# 
# All shall be well and all shall be well and all manner of things shall be well.
# Nope...we're doomed!
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import glob
import sys, re
import setuptools
import pybind11


# (c) Sylvain Corlay, https://github.com/pybind/python_example
def has_flag(compiler, flagname):

  import tempfile

  with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:

    f.write('int main (int argc, char **argv) { return 0; }')

    try:
      compiler.compile([f.name], extra_postargs=[flagname])
    except setuptools.distutils.errors.CompileError:
      return False

  return True


# (c) Sylvain Corlay, https://github.com/pybind/python_example
def cpp_flag(compiler):

  if   has_flag(compiler,'-std=c++14'): return '-std=c++14'
  elif has_flag(compiler,'-std=c++11'): return '-std=c++11'
  raise RuntimeError('Unsupported compiler: at least C++11 support is needed')


# (c) Sylvain Corlay, https://github.com/pybind/python_example
class BuildExt(build_ext):

  c_opts = {
    'msvc': ['/EHsc'],
    'unix': [],
  }

  if sys.platform == 'darwin':
    c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

  def build_extensions(self):
    ct = self.compiler.compiler_type
    opts = self.c_opts.get(ct, [])
    if ct == 'unix':
      opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
      opts.append(cpp_flag(self.compiler))
    elif ct == 'msvc':
      opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
    for ext in self.extensions:
      ext.extra_compile_args = opts
    build_ext.build_extensions(self)


src_dir = "facedet"
inc_dir = "facedet"

src_file = glob.glob(f"{src_dir}/facedet*.cc")


ext_modules = [
  Extension(
    'pyfacedet',
    src_file,
    include_dirs=[
      pybind11.get_include(False),
      pybind11.get_include(True ),
      inc_dir,
    ],
    language='c++'
  ),
]

# packages = ["."]
# print(packages)
setup(
    name=f"pyfacedet",
    version="0.0.3",
    description="face detection python library",
    author="YuqinLiang",
    author_email="YuqinLiangX@gmail.com",
    url="",
    # download_url=f"{URL}/archive/{__version__}.tar.gz",
    keywords=[],
    python_requires=">=3.8",
    install_requires=[],
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
    # packages=packages,
    # include_package_data=include_package_data,
)