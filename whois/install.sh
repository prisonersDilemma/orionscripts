#!/usr/bin/env bash
#
# Install script for Python package: `whois'
# version = '0.0.2'
#
PKGNAME='whois'
MINIMUM_PYTHON_VERSION_REQUIRED=3.5
#===============================================================================
# Get info about the host system, so we know which package manager to use.
#===============================================================================
printf "%b\n" "\033[32;1mGetting info about the host environment.\033[0m"
sleep 0.5
# Linux, Darwin
osystem=$(uname)
# Manjaro, aws. Won't work on OSX.
release=$(uname -r | sed 's/-/ /g' | awk '{ print $3 }')
# Ubnuntu.
#version=$(uname -v)
#===============================================================================
# Package manager commands.
#===============================================================================
if [[ "$osystem" -eq "Linux" ]]; then
    printf "%b\n" "\033[32;1mAh. A Linux distribution.\033[0m"
    if [[ "$release" -eq "aws" ]]; then
        printf "%b\n" "\033[32;1maws?.\033[0m"
        pkg_mgr_cmd='sudo apt-get install'
    elif [[ "$release" -eq "Manjaro" ]]; then
        pkg_mgr_cmd='sudo pacman -Ssy'
    fi
fi
#===============================================================================
# Check for necessary packages: git, python3
#===============================================================================
printf "%b\n" "\033[32;1mChecking for major dependencies (e.g., git, python3).\033[0m"
sleep 0.50
git_exists=$(if [[ -x $(which git) ]]; then echo "true"; else echo "false"; fi)
py3_exists=$(if [[ -x $(which python3) ]]; then echo "true"; else echo "false"; fi)
py3_version=$(python3 --version | sed 's/Python //')
#
# This type of test for equality is not going to work.
# Install git if necessary.
#printf "%b\n" "\033[32;1mInstalling git.\033[0m"
#if [[ $git_exists -eq "false" ]]; then
#    $("$pkg_mgr_cmd" "git")
#fi
#
# Install/update python3 if necessary.
#printf "%b\n" "\033[32;1mInstalling python3.\033[0m"
#if [[ $py3_exists -eq "false" ]] || \
#   [[ $py3_ver < $MINIMUM_PYTHON_VERSION_REQUIRED ]]; then
#    $("$pkg_mgr_cmd" "python3")
#fi
#===============================================================================
# Check for/get the Python tools to build the distribution/package.
#===============================================================================
# Make sure we have either venv or virtualenv installed, along with setuptools,
# and wheel. Add -U update option when calling pip.
printf "%b\n" "\033[32;1mChecking for Python tools for distribution build.\033[0m"
sleep 0.5
#
# If the string is empty, we need to install.
need_setuptools=$(pip show setuptools)
if [[ -z "${need_setuptools}" ]]; then
    printf "%s\n" "Using pip to install setuptools"
    sudo -H pip install setuptools
fi
#
need_venv=$(pip show venv)
if [[ -z "${need_venv}" ]]; then
    # If either venv or virtualenv can't be installed, try the other.
    printf "%s\n" "Using pip to install virtualenv"
    sudo -H pip install virtualenv
    #sudo -H pip install venv
fi
#
need_wheel=$(pip show wheel)
if [[ -z "${need_wheel}" ]]; then
    printf "%s\n" "Using pip to install wheel"
    sudo -H pip install wheel
fi
#===============================================================================
# Start the installation of the whois package.
#===============================================================================
printf "%b\n" "Installing the whois package."
sleep 0.25
#
# Temporary location to download the resources.
#tempdir=/tmp/whois
#mkdir $tempdir
#cd $tempdir
#
# Where to make the install of the distribution/package.
WHOIS_HOME="${HOME}/bin/whois-venv"
# Create a home directory for the  package, and any parent directories.
if [[ ! -d "${WHOIS_HOME}" ]]; then
    printf "%b\n" "\033[32;1mInstall at: ${WHOIS_HOME}\033[0m"
    mkdir -p ${WHOIS_HOME}
fi
#
# Create the "Virtual Environment".
virtualenv "${WHOIS_HOME}"
# Download the package.
cd "$WHOIS_HOME"
# Execute as a sub-process, so we don't have to look at the output.
$(git clone "https://github.com/prisonersDilemma/orionscripts.git")
#
# Activate the virtual environment.
printf "%b\n" "\033[32;1mActivating the virtual environment.\033[0m"
source "${WHOIS_HOME}"/bin/activate
#
# Make sure we're using the distribution in the venv, first!
# If we're using the proper distribution, then wherever we put the venv dir
# should prefix the path of python ('../bin/python') and pip ('../bin/pip').
path_to_python=$(which python)
if [[ ! -e "${WHOIS_HOME}/bin/python" ]]; then
    printf "%b\n" "ERROR: I don't seem to be operating within the context of the virtual environment. Exiting."
    exit
else
    printf "%b\n" "\033[31mThe Python executable exists in the virtual environment.\033[0m"
fi
#===============================================================================
# Install the dependencies.
#===============================================================================
# Add some tests to only install/upgrade if necessary.
printf "%b\n" "\033[32;1mInstalling dependencies.\033[0m"
pip install -r requirements.txt
#
# Install the package, linked symbolically (-e), so that changes are reflected
# automatically.
printf "%b\n" "\033[32;1mInstalling ${PKGNAME}\033[0m"
pip install -e ../whois
#===============================================================================
# Clean up.
#===============================================================================
# Remove the contents of orionscripts.
#
# Deactivate the virtual environment.
deactivate
# Add an alias to run the distribution from the "virtual environment".
echo "alias whois=${path_to_python} -m whois" >> "${HOME}/.bashrc"
#
# Make __main__.py executable. Not even necessary with the alias, using Python
# to run the program.
#[[ -e ./whois/__main__.py ]] && chmod 744 ./whois/__main__.py
#===============================================================================
