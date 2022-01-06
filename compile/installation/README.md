# Compile - Installation Guide <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

* [1. Overview](#1-overview)
* [2. Download from Official PyPI server](#2-download-from-official-pypi-server)
* [3. Update the oframe bash profile](#3-update-the-oframe-bash-profile)
* [4. Offline installation](#4-offline-installation)

## 1. Overview

This document gives the few steps required for oftools_compile installation. 

Prerequisites:
- Python 3.6 or higher
- pip3, package installer for Python

## 2. Download from Official PyPI server

Installing oftools_compile is very simple. Just run the following commands:
```bash
su - oframe
# <enter password>

# Local install, just for oframe user
pip3 install oftools_compile --user

# Global install
sudo pip3 install oftools_compile
```

## 3. Update the oframe bash profile

**a.** Open oframe user bash profile:
```bash
su - oframe
# <enter password>
vi ~/.bash_profile
```

**b.** Add the following lines  (if not already in the profile), the most important being the `export PATH` line. All the rest is optional depending on your environment:

```bash
#===============================================================#
#                   VERSION CONTROL                             #
#===============================================================#
export GIT_HOME=${TMAX_HOME}/git_repositories

#===============================================================#
#                   OFTOOLS_COMPILE - ENVIRONMENT VARIABLES     #
#===============================================================#
export COMPILE_WORK_DIR=${TMAX_HOME}/tmaxapp/compile
export SOURCE_DIR=${TMAX_HOME}/source
export PROFILE_DIR=${GIT_HOME}/compilation-configuration/profiles
export PATH=${PATH}:${GIT_HOME}/compilation-configuration/scripts

#===============================================================#
#                   OFTOOLS_COMPILE - PROFILES                  #
#===============================================================#
export DEV_PROFILES=${PROFILE_DIR}/developer
export CICD_PROFILES=${PROFILE_DIR}/cicd

export COBOL_PROFILE=${DEV_PROFILES}/cbl.prof
export ASM_PROFILE=${DEV_PROFILES}/asm.prof
export CPY_PROFILE=${DEV_PROFILES}/cpy.prof
export JCL_PROFILE=${DEV_PROFILES}/jcl.prof
export PROC_PROFILE=${DEV_PROFILES}/prc.prof
export ASM_INT_PROFILE=${DEV_PROFILES}/asm_interface.prof
export C_PROFILE=${DEV_PROFILES}/c.prof
export CPP_PROFILE=${DEV_PROFILES}/cpp.prof
export SQL_PROFILE=${DEV_PROFILES}/sql.prof
export RDBMS_PROFILE=${DEV_PROFILES}/rdbms.prof
export BMS_MAP_PROFILE=${DEV_PROFILES}/bms.prof
export CSD_PROFILE=${DEV_PROFILES}/csd.prof
export CTL_PROFILE=${DEV_PROFILES}/ctl.prof
export EASYTRIEVE_PROFILE=${DEV_PROFILES}/esy.prof
export EASYTRIEVEP_PROFILE=${DEV_PROFILES}/esyp.prof

#===============================================================#
#                   OFTOOLS_COMPILE - ALIASES                   #
#===============================================================#
alias compile='cd ${COMPILE_WORK_DIR}'
alias compwd='cd ${COMPILE_WORK_DIR}'
alias src='cd ${SOURCE_DIR}'
alias profiles='cd ${GIT_HOME}/compilation-configuration/profiles'

alias srccob='cd ${SOURCE_DIR}/COBOL'
alias srcasm='cd ${SOURCE_DIR}/ASM'
alias srccpy='cd ${SOURCE_DIR}/COPYBOOK'
alias srcjcl='cd ${SOURCE_DIR}/JCL'
alias srcproc='cd ${SOURCE_DIR}/PROC'
alias srcasmint='cd ${SOURCE_DIR}/ASM_INTERFACE'
alias srcc='cd ${SOURCE_DIR}/C'
alias srcc++='cd ${SOURCE_DIR}/C++'
alias srcsql='cd ${SOURCE_DIR}/SQL'
alias srcrdbms='cd ${SOURCE_DIR}/RDBMS'
alias srcbms='cd ${SOURCE_DIR}/BMS_MAP'
alias srccsd='cd ${SOURCE_DIR}/CICS-CSD'
alias srcctl='cd ${SOURCE_DIR}/Control'
alias srcprot='cd ${SOURCE_DIR}/EASYTRIEVE'
alias srcc++='cd ${SOURCE_DIR}/C++'

#===============================================================#
#                   OFTOOLS_COMPILE - FUNCTIONS                 #
#===============================================================#
function compilation-fn { oftools_compile $@; }
function compilation-cobol-fn { oftools_compile -p $COBOL_PROFILE -s $1 -l INFO; }
function compilation-asm-fn { oftools_compile -p $ASM_PROFILE -s $1 -l INFO; }

alias comp=compilation-fn
alias compcbl=compilation-cobol-fn
alias compasm=compilation-asm-fn

# With the same idea it is possible to create as many function as you need
```

**c.** Adapt the previous parameters to your environment. Save the bash profile and execute it:
```bash
source ~/.bash_profile
```

**d.** Try to run the command `oftools_compile -h` to double check that everything is correctly set up.

## 4. Offline installation

If for any reason the installation command in the section above is not working because of a firewall or network issue in your environment, please contact a TmaxSoft engineer so that we can help you to install it manually.

To manually install oftools_compile, run these commands:
```bash
su - oframe
# <enter password>

# Local install, just for oframe user
pip3 install --user --no-index --find-links . oftools-compile-1.2.1.dev9.tar.gz

# Global install
sudo pip3 install --no-index --find-links . oftools-compile-1.2.1.dev9.tar.gz
```
