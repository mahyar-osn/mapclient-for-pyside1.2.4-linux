#!/usr/bin/env python
import platform, sys, os
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
from mapclient.settings import version as app_version


SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
version = app_version.__version__

# Define the list of requirments
install_requires = ['rdflib',
                    'virtualenv',
                    'python-dateutil',
                    'dulwich',
                    'pmr2.client']

try:
    import importlib
except ImportError:
    # Python < 2.7 doesn't have importlib in the core distribution
    install_requires.append('importlib')


def createApplication(install_dir):
    from subprocess import call
    call([sys.executable, 'shimbundle.py', 'MAP Client', version],
          cwd=os.path.join(install_dir, 'mapclient', 'tools', 'osxapp'))


# For OS X we want to install MAP Client into the Applications directory
class InstallCmd(_install):

    def run(self):
        _install.run(self)
        mac_release, _, _ = platform.mac_ver()
        if mac_release:
            self.execute(createApplication, (self.install_lib,),
                         msg="Creating OS X Application")

        import subprocess
        subprocess.call(['pip', 'install', '-r', os.path.join(SETUP_DIR, 'requirements.txt')])


# For OS X we want to install MAP Client into the Applications directory
class DevelopCmd(_develop):

    def run(self):
        _develop.run(self)
        mac_release, _, _ = platform.mac_ver()
        if  mac_release:
            self.execute(createApplication, (self.setup_path,),
                         msg="Creating OS X Application")


setup(name='mapclient',
     version=version,
     description='A framework for managing and sharing workflows.',
     author='MAP Client Developers',
     author_email='mapclient-devs@physiomeproject.org',
     url='https://github.com/MusculoskeletalAtlasProject',
     # namespace_packages=['mapclientplugins', ],
     packages=find_packages(exclude=['tests', 'tests.*', 'mapclientplugins', 'mapclientplugins.*', 'model', 'model.*' ]),
     package_data={'mapclient.tools.annotation': ['annotation.voc'], 'mapclient.tools.osxapp': ['mapclient.icns']},
     # py_modules=['mapclient.mapclient'],
     entry_points={'console_scripts': ['mapclient=mapclient.application:main']},
     install_requires=install_requires,
     cmdclass={'install': InstallCmd, 'develop': DevelopCmd}
)
