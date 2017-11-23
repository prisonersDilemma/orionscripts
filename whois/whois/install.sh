#!/usr/bin/env bash

# Install script for Python package: `whois'
# version = '0.0.1'

PKGNAME = 'whois'

# Where to put the package.
WHOIS_HOME = "~/bin/whois"

# Create the package directory, and any parent directories.
printf "%s\n" "Creating an install path at: ${WHOIS_HOME}"
mkdir -p ${WHOIS_HOME}


# The "virtual environment" directory.
WHOIS_VENV = ${WHOIS_HOME}"-env"

# Create the "Virtual Environment".
printf "%s\n" "Creating the Python virtual environment for the package: $PKGNAME"
python -m venv "${WHOIS_VENV}"

# Activate the virtual environment.
printf "%s\n" "Activating the virtual environment."
source "${WHOIS_VENV}"/bin/activate

# Make sure we're using the distribution in the venv, first!
# If we're using the proper distribution, then wherever we put the venv dir
# should prefix the path of python ('../bin/python') and pip ('../bin/pip').
path_to_python=$(which python)
if [[ ! "${WHOIS_VENV}/bin/python" -eq "${path_to_python}" ]]; then
    return
fi


# Install the dependencies.
printf "%s\n" "Installing dependencies."
pip install -r requirements.txt

# Install the package, linked symbolically (-e), so that changes are reflected
# automatically.
printf "%s\n" "Installing ${PKGNAME}"
pip install -e whois


# Make __main__.py executable.
chmod +x "${WHOIS_HOME}/whois/__main__.py"

# Add some aliases, or add to PATH in ~/.bashrc.
echo 'export PATH="${HOME}/bin:${PATH}"' >> "~/.bashrc"
echo 'alias whois="python -m whois"' >> "~/.bashrc"
