#!/usr/bin/env python3.6
"""Install script for Python package: `whois'"""
__version__ = (0,0,2)
__date__ = '2017-11-23'

import os
import re
import shutil
import subprocess
import sys
import time

USER_HOME = os.getenv('HOME') # Where to make the install of the distribution/package.
GIT_HOME = os.path.join(USER_HOME, 'git')
WHOIS_DEST = os.path.join(USER_HOME, 'bin')
WHOIS_HOME = os.path.join(WHOIS_DEST, 'whois')
WHOIS_BIN = os.path.join(WHOIS_HOME, 'bin')
COMPATIBLE_RELEASES = ['aws', 'manjaro', 'arch']
COMPATIBLE_SYSTEMS = ['Linux', ]
MAJOR_DEPENDENCIES = ['git', 'pip']
MINIMUM_PYTHON_VERSION_REQUIRED = 3.5
PACKAGE_NAME = 'whois'
PYTHON_PKG_DIST_TOOLS = ['setuptools', 'virtualenv', 'wheel']
PY3_VENV_PATH = f'{WHOIS_HOME}/bin/python' # Where Python should be running if in venv.
VERSION_NO = re.compile(r'(?P<major>\d)\.(?P<minor>\d)\.(?P<micro>\d)').search
PACKAGE_MANAGER_CMDS = { 'aws': 'sudo apt-get install',
                         'ubuntu': 'sudo apt-get install',
                         'manjaro': 'sudo pacman -Ssy',
                         'arch': 'sudo pacman -Ssy', }


def colorstr(msg, color=32):
    """Return a colored string given an 8-bit ANSI fg-color value (31-38).
    Default is green (32)."""
    return msg.join([f'\033[{int(color)}m', '\033[0m'])


def print_color(msg, color=32, *args, **kwargs):
    """Print a colored string.

    Uses colorstr to print a string in a color, given as the value of an
    8-bit ANSI fg-color escape sequence (31-38). Default is green (32).
    Additional args and kwargs will be passed to the `print' function and
    printed normally."""
    print(colorstr(msg, color), *args, **kwargs)


def prompt(func, *args, **kwargs):
    """Return func(*args, **kwargs) wrapped in a classic (y/N)-style prompt."""

    def proceed(*args, **kwargs):
        """Return the result of *func* executed if y or Y is given at the
        prompt, or None for if n or N is given. Continue indefinitely prompting
        for all else. If the keyword argument 'prompt' is given, it is used as
        the prompt string, with '(y/N)? ' automatically appended. Otherwise,
        '(y/N)? ' is used as the default.
        """
        prmpt = kwargs.get('prompt', '')
        prmpt += '(y/N)? '
        while True:
            try:
                answer = input(prmpt)[0].lower()
                if answer == 'y':
                    return func(*args, **kwargs)
                elif answer == 'n':
                    return
            except IndexError: # No input received.
                continue
    return proceed


@prompt
def install_package(*args, **kwargs):
    print_color(f"""Installing `{kwargs["pkg"]}'. May require `sudo'.""")
    cmd = kwargs.get('cmd').split(' ')
    cmd.append(kwargs.get('pkg'))
    return subprocess.run(cmd)


def install_prompt(pkg):
    """Return a colorized string for a prompt.
    A utility function to construct the *prompt* keyword arg for
    install_package."""
    return colorstr(f"`{pkg}' is not installed, and is required to proceed. "
                     "Would you like me to install {pkg} for you ", color=33)


def normalize_release(release):
    """Return the release name in lowercase."""
    return release.split('-')[-1].lower()


def is_compatible_OS(system, release):
    """Return true if the system and release are compatible.

    "Compatible" means the system is POSIX (Unix-based), and we know the
    command for the package manager.

    Get info about the host system, so we know which package manager to use.
    sysname: Linux, Darwin | release: Manjaro, aws | version: Ubnuntu
    Object with 5 attrs, namely sysname, release, version.
    """
    return (system in COMPATIBLE_SYSTEMS and release in COMPATIBLE_RELEASES)


def has(package):
    """Return true if *package* is installed on the local system."""
    return True if subprocess.getoutput(f'which {package}') else False

def missing_python_pkg_dist_tools():
    """Return a list of any missing Python packages.
    The tools listed in PYTHON_PKG_DIST_TOOLS are those that are searched for.
    They are not installed by default, so the `pip show' command is used to
    check whether they've been installed."""
    return [pkg for pkg in PYTHON_PKG_DIST_TOOLS if not subprocess.getoutput(f'pip show {pkg}')]


def is_python3_venv():
    """Return true if we're running Python from the virtual environment.

    Make sure we're using the distribution in the venv, first! If we're using
    the proper distribution, then wherever we put the venv dir should be the
    prefix of the path for python ('../bin/python') and pip ('../bin/pip').
    """
    # Current running Python process vs where Python should be running in the venv.
    return subprocess.getoutput('which python') != PY3_VENV_PATH


def install_whois():
    """
    # If installing globally, add 'sudo', or, at least in the case of `pip',
    # 'sudo', '-H'.

    # So I guess I do need the version of Python installed that I want to
    # install in the virtualenv.

    # Unfortunately, installing py3mods as requirements using the '-e' option
    # will cause pip to not recognize the path, so it can't be used. So, I do
    # not know if that package is installed as symbolic links. I guess I'll
    # have to make a change and find out.
    #
    # py3mods ends up installed at <venv>/lib/python3.6/site-package/py3mods
    # whereas, whois is at <venv>/lib/python3.6/site-packages/whois.egg-link

    # I don't know how to install requirements from a file with -e option.
    # So, I'll have to download those as well.
    """
    # returncode can be either 0 or 1; returncode 1 -> dir exists
    if 0 <= subprocess.run(['mkdir', '-p', WHOIS_HOME]).returncode <= 1:
        os.chdir(WHOIS_HOME)
        if subprocess.run(['git', 'clone', 'https://github.com/prisonersDilemma/orionscripts.git', f'{GIT_HOME}/orionscripts']).returncode == 0:
            if subprocess.run(['git', 'clone', 'https://github.com/prisonersDilemma/py3mods.git', f'{GIT_HOME}/py3mods']).returncode == 0:
                if subprocess.run(['virtualenv', '--python=/usr/bin/python3.6', '.']).returncode == 0:
                    if subprocess.run([f'{WHOIS_BIN}/pip', 'install', '-e', f'{GIT_HOME}/orionscripts/whois']).returncode == 0:
                        print_color('Installing dependencies.')
                        if subprocess.run([f'{WHOIS_BIN}/pip', 'install', '-e', f'{GIT_HOME}/py3mods']).returncode == 0:
                            return 0
                        else: return -1
                    else: return -2
                else: return -3
            else: return -4
        else: return -5
    else: return -6


def main():

    print_color('Getting information about the host environment...', end=' ')
    uname = os.uname()
    system, release = uname.sysname, normalize_release(uname.release)
    if not is_compatible_OS(system, release): return -1
    print_color(f'{system} is compatible.')


    print_color('Obtaining the requiste package manager command...')
    pkgmgr_cmd = PACKAGE_MANAGER_CMDS.get(release, None)
    if not pkgmgr_cmd: return (-2, (system, release))


    print_color('Checking for major dependencies...')
    for pkg in MAJOR_DEPENDENCIES: # pip == python-pip
        if has(pkg): print_color(f"`{pkg}' is installed.")
        elif not install_package(prompt=install_prompt(pkg), cmd=pkgmgr_cmd, pkg=pkg):
            return (-3, pkg)


    # Check for/get the Python tools to build the package/distribution. Make
    # sure we have either venv or virtualenv installed, along with setuptools,
    # and wheel. Add -U update option when calling pip.

    print_color("""Checking for the Python tools to build the `whois' """
                """distribution (i.e., "package"). This may require `sudo'.""", color=33)
    for pkg in missing_python_pkg_dist_tools():
        print_color(f"Using `pip' to install {pkg}.", color=33)
        subprocess.run(['sudo', '-H', 'pip', 'install', pkg])


    # Start the installation of the whois package.
    print_color("Beginning installation of `whois'. This may require `sudo'.")

    if not is_python3_venv():
        print_color("ERROR: Installation cannot be completed at this time. "
                    "Something went wrong, and I don't seem to be operating "
                    "within the context of the virtual environment. Please "
                    "report this error.", color=31)
        return -4

    whois_install_returncode = install_whois()
    if returncode == 0: return 0
    else: return -5, whois_install_returncode



if __name__ == '__main__':
    exit_code = main()

    # Return/exit codes:
    # -1: incompatible system or release
    # -2: cannot find pkgmgr_cmd for system, release
    # -3: missing `pkg' dependency
    # -4: Not running Python in the venv.
    # -5: installation of whois or dependencies failed



# Not sure installing here is ideal. Need an executable in there that can run
# the Python distro of choice, and be able to import the necessary modules, and
# understand the hierarchy of configs.
#WHOIS_DEST = '/usr/bin' # Also there is ~/.local at least on aws.
#
#def has_git():
#    """Return true if git can be found installed on the system."""
#    return True if subprocess.getoutput('which git') else False
#
## if not, install python-pip
#def has_pip():
#    """Return true if pip can be found installed on the system."""
#    return True if subprocess.getoutput('which pip') else False
#
# Shouldn't need these. I can install whichever Python I want via pip, in the venv.
#def has_python3():
#    return True if subprocess.getoutput('which python3') else False
#
#def have_py3_compatible():
#    ver = VERSION_NO(subprocess.getoutput('python3 --version').split()[-1])
#    verno = float('.'.join([ver.group('major'), ver.group('minor')]))
#    return verno >= 3.5
#
#
## Shouldn't need to do this if installed in /usr/bin (once locate database is updated).
#@prompt
#def add_alias(*args, **kwargs):
#    """Add an alias for the whois command to ~/.bashrc if y/Y given when prompted."""
#    bashrc = os.path.join(USER_HOME, '.bashrc')
#    with open(bashrc, mode='a') as f:
#        f.write(f'alias whois="{PY3_VENV_PATH} -m whois"\n')
#
#
#    add_alias(colorstr("Would you like me to add an alias for `whois' in ~/.bashrc (y/N)?"))
#
#requirements = subprocess.Popen(['cat', f'{WHOIS_HOME}/whois/requirements.txt'], stdout=subprocess.PIPE).stdout
#if subprocess.run([f'{WHOIS_BIN}/pip', 'install', '-e'], stdin=requirements).returncode == 0:
#
#if subprocess.run([f'{WHOIS_BIN}/pip', 'install', '-e', f'{WHOIS_HOME}/whois/requirements.txt']).returncode == 0:
#    #print_color('Cleaning up')
#    #try: shutil.rmtree('orionscripts')
#    #except PermissionError:
#    #    if subprocess.run(['sudo', 'rm', '-rf', 'orionscripts']).returncode == 0: pass
