# Dataset Migration - Installation Guide <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

* [1. Overview](#1-overview)
* [2. Download from Official PyPI server](#2-download-from-official-pypi-server)
* [3. Update the oframe bash profile](#3-update-the-oframe-bash-profile)
* [4. Offline installation](#4-offline-installation)
* [5. Automatic login through ftp](#5-automatic-login-through-ftp)

## 1. Overview

This document gives the few steps required for oftools_dsmigin installation. 

Prerequisites:
- Python 3.6 or higher
- pip3, package installer for Python

## 2. Download from Official PyPI server

Installing oftools_dsmigin is very simple. Just run the following commands:
```bash
su - oframe
# <enter password>

# Local install, just for oframe user
pip3 install oftools_dsmigin --user

# Global install
sudo pip3 install oftools_dsmigin
```

## 3. Update the oframe bash profile

**a.** Open oframe user bash profile:
```bash
su - oframe
# <enter password>
vi ~/.bash_profile
```

**b.** Add the following lines (if not already in the profile), the most important being the `export PATH` line. All the rest is optional depending on your environment:

```bash
#===============================================================#
#                   VERSION CONTROL                             #
#===============================================================#
export GIT_HOME=${HOME_DIRECTORY}/git_repository

#===============================================================#
#                   OFTOOLS_DSMIGIN - ENVIRONMENT VARIABLES     #
#===============================================================#
export MIGRATION_WORK_DIR=${HOME_DIRECTORY}/tmaxapp/migration
export PATH=${PATH}:${HOME}/.local/bin

#===============================================================#
#                   OFTOOLS_DSMIGIN - ALIASES                   #
#===============================================================#
alias migration='cd ${MIGRATION_WORK_DIR}'
alias migcpy='cd ${MIGRATION_WORK_DIR}/copybooks'
alias migbckp='cd ${MIGRATION_WORK_DIR}/csv_backups'
alias migds='cd ${MIGRATION_WORK_DIR}/datasets'
alias miglog='cd ${MIGRATION_WORK_DIR}/logs'
alias dsgdg='cd ${MIGRATION_WORK_DIR}/datasets/GDG'
alias dspo='cd ${MIGRATION_WORK_DIR}/datasets/PO'
alias dsps='cd ${MIGRATION_WORK_DIR}/datasets/PS'
alias dsvsam='cd ${MIGRATION_WORK_DIR}/datasets/VSAM'

#===============================================================#
#                   OFTOOLS_DSMIGIN - FUNCTIONS                 #
#===============================================================#
function migration-fn { oftools_dsmigin $@ }
function migration-init-fn { oftools_dsmigin --csv $1 -w . --init }
function migration-listcat-fn { oftools_dsmigin --csv $1 -w . --listcat --ip-address 10.100.100.10 }
function migration-download-fn { oftools_dsmigin --csv $1 -w . --ftp --ip-address 10.100.100.10 }
function migration-migration-fn { oftools_dsmigin --csv $1 -w . --migration }

alias mig=migration-fn
alias miginit=migration-init-fn
alias miglist=migration-listcat-fn
alias migdl=migration-download-fn
alias migmig=migration-migration-fn

# With the same idea it is possible to create as many function as you need
```

**c.** Adapt the previous parameters to your environment. Save the bash profile and execute it:
```bash
source ~/.bash_profile
```

**d.** Try to run the command `oftools_dsmigin -h` to double check that everything is correctly set up.

## 4. Offline installation

If for any reason the installation command in the section above is not working because of a firewall or network issue in your environment, please contact a TmaxSoft engineer so that we can help you to install it manually.

To manually install oftools_compile, run these commands:
```bash
su - oframe
# <enter password>

# Local install, just for oframe user
pip3 install --user --no-index --find-links . oftools-dsmigin-0.0.1.dev36.tar.gz

# Global install
sudo pip3 install --no-index --find-links . oftools-dsmigin-0.0.1.dev36.tar.gz
```

## 5. Automatic login through ftp

This tool heavily use the FTP connection to the Mainframe, so it can be very interesting to automate the authentication.

**a.** Create the file *.netrc* in the home folder of the user running the `oftools_dsmigin` command:

```bash
cd ~
vi .netrc
```

**b.** Here is an example of what needs to be specified in the file:

  - IP address of the Mainframe
  - Username
  - Password

```txt
machine 192.168.200.1 login USERNAME password PASSWORD
```

**c.** Save the file and change the permissions:

```bash
chmod 600 .netrc
```