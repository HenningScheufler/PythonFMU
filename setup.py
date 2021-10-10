import os, pathlib, platform
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

cwd = os.getcwd()
print("platform.system()",platform.system())
print("os.name",os.name)
WINDOWS = (platform.system() == 'Windows')
print("on WINDOWS.name",WINDOWS)

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        if not os.path.exists(os.path.join(cwd,"tmp-build")):
            os.mkdir(os.path.join(cwd,"tmp-build"))
            build_type = 'Release'
            # configure
            cmake_args = [
                'cmake',
                '../pythonfmu/pythonfmu-export',
                '-DCMAKE_BUILD_TYPE={}'.format(build_type)
            ]
            print("cmake_args",cmake_args)
            if WINDOWS:
                cmake_args.append('-A x64')
            print("cmake_args after windows",cmake_args)
            os.chdir(os.path.join(cwd,"tmp-build"))
            subprocess.check_call(cmake_args)
            cmake_args_build = [
                'cmake',
                '--build',
                '.'
            ]
            if WINDOWS:
                cmake_args_build.append('--config Release')
            print("cmake_args_build after windows",cmake_args)
            subprocess.check_call(cmake_args_build)
            os.chdir("..")

class CMakeBuild(build_ext):
    def run(self):
        pass
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        pass

# See setup.cfg for Python package parameters
setup(
    ext_modules=[CMakeExtension('.')],
    cmdclass=dict(build_ext=CMakeBuild),
)
