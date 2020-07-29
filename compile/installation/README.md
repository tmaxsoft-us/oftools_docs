# oftools_compile User Guide <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [1. Overview](#1-overview)
- [2. Download from Official PyPI Server](#2-download-from-official-pypi-server)
- [3. Update the oframe Bash Profile](#3-update-the-oframe-bash-profile)

## 1. Overview

This document gives the few steps required for oftools_compile installation. 

Prerequisites:
- Python 3.5 or higher
- pip, package installer for Python

## 2. Download from Official PyPI server

**a.** Installing oftools_compile is very simple. Just run the following commands:
```bash
su - oframe
# <enter password>

# Local install, just for oframe user
pip3 install oftools_compile --user

# Global install
sudo pip3 install oftools_compile
```

If the commands above are not working because of a firewall or network issue in your environment, please contact a TmaxSoft engineer so that we can help you to install it manually.

**b.** To manually install oftools_compile, run these commands:
```bash
tar -zxvf oftools_compile.tar.gz
cd oftools_compile
cp -r oftools oftools_egg* $HOME/.local/lib/python-xx/site-package
cp oftools_compile $HOME/.local/bin
```

TODO Review the commands above to see if it is working as it is or if it needs some modifications.

> **Note**: These commands correspond to a local installation.

## 3. Update the oframe Bash Profile

**a.** Open oframe user bash profile:
```bash
su - oframe
# <enter password>
vi ~/.bash_profile
```

**b.** Add the following lines, the most important being the `export PATH` line. All the rest is optional depending on your environment:
```bash
#===============================================================#
#                   VERSION CONTROL                             #
#===============================================================#
export GIT_HOME=${HOME_DIRECTORY}/git_repository

#===============================================================#
#                   COMPILATION WITH OFTOOLS_COMPILE            #
#===============================================================#
export COMPILE_WORK_DIR=${HOME_DIRECTORY}/tmaxapp/compile
export COPY_HOME=${GIT_HOME}/src/COPYBOOK
export COBOL_PROFILE=${GIT_HOME}/compile/cobol.prof
export ASM_PROFILE=${GIT_HOME}/compile/asm.prof
export C_PROFILE=${GIT_HOME}/compile/c.prof
export PATH=${PATH}:${HOME}/.local/bin

# Compilation
alias compile='cd ${COMPILE_WORK_DIR}'
alias prof='cd ${GIT_HOME}/compile'
alias src='cd ${GIT_HOME}/src'
alias srccob='cd ${GIT_HOME}/src/COBOL'
alias srccpy='cd ${GIT_HOME}/src/COPYBOOK'
alias srcasm='cd ${GIT_HOME}/src/ASM'
alias srcprot='cd ${GIT_HOME}/src/EazyTrieve'
alias srcc='cd ${GIT_HOME}/src/C'
```

**c.** Adapt the previous parameters to your environment. Save the bash profile and execute it:
```bash
source ~/.bash_profile
```

**d.** Try to run the command `oftools_compile -h` to double check that everyting is correctly set up.

