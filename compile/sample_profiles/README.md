# OpenFrame Tools Compile - Sample Profiles <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

* [1. Overview](#1-overview)
* [2. COBOL](#2-cobol)
  * [2.1 Default profile](#21-default-profile)
  * [2.2 Advanced profile](#22-advanced-profile)
  * [2.3 Other profiles](#23-other-profiles)
* [3. Assembler](#3-assembler)
  * [3.1 Default profile](#31-default-profile)
  * [3.2 Advanced profile](#32-advanced-profile)
  * [3.3 Other examples](#33-other-examples)
* [4. Copybook](#4-copybook)
* [5. JCL](#5-jcl)
* [6. Proc](#6-proc)
* [7. Assembler Interface](#7-assembler-interface)
* [8. C Language](#8-c-language)
* [9. C++ Language](#9-c-language)
* [10. SQL](#10-sql)
* [11. BMS Map](#11-bms-map)
  * [11.1 Default profile](#111-default-profile)
  * [11.2 Other examples](#112-other-examples)
* [12. CICS CSD](#12-cics-csd)
* [13. Control](#13-control)
* [14. Easytrieve](#14-easytrieve)
* [15. Easytrieve Plus](#15-easytrieve-plus)
* [16. Environment variables resources](#16-environment-variables-resources)

## 1. Overview

This document lists some profiles that can be used with oftools_compile, with a detailed description of each division and section. It is divided in multiple sections, one for each programming language.

- First, it gives the default profile that every project should start with, which is the most basic profile.
- Then, it gives multiple advanced profiles that can also be used as a baseline for any project, but this time these are profiles that can cover many scenarios at once.

## 2. COBOL

<a href="#top">Back to top</a>

### 2.1 [Default profile](./cobol/cobol_default.prof)

```ini
[setup]
workdir = /opt/tmaxapp/compile

[ofcbpp]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.cbl
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT

[ofcob]
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT
# OFCOB DEBUG OPTION: --enable-debug
```

This one is very simple, there are only 3 sections:

- `[setup]` section: mandatory section to specify the working directory.
- `[ofcbpp]` section: OpenFrame COBOL pre-compilation, for any COBOL program.
- `[ofcob]` section: OpenFrame COBOL compilation.

### 2.2 [Advanced profile](cobol/cobol_advanced.prof)

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/cobol
#mandatory = dos2unix:ofcbpp:ofcob

# Environment variables
$SOURCECPY = /opt/source/copybook
$OFCOBCPY = $OFCOBCPY:$OFCOB_HOME/copybook:$OPENFRAME_HOME/osc/copybook:$OPENFRAME_HOME/osc/region/OSCOIVP1/map/symbolic:$SOURCECPY/COPYBOOK.COMMON:$SOURCECPY/COPYBOOK.CICS:$SOURCECPY/COPYBOOK.DDL:$SOURCECPY/COPYBOOK.UPDATED:$SOURCECPY/MSTR.COPYLIB:$SOURCECPY/COPYBOOK.MSTRTSS:/opt/source/MAPSETS/MAPSET.COPYBOOK.MSTR:/opt/source/MAPSETS/MAPSET.COPYBOOK.MSTRBDS

# Filter variables

# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always
?cics = grep -av "^......\*" $OF_COMPILE_IN | grep -aE "EXEC.*CICS|USING.*DFHEIBLK|USING.*DFHCOMMAREA"
?day_of_week = grep -a "FROM DAY-OF-WEEK" $OF_COMPILE_IN
?online = grep -av "^......\*" $OF_COMPILE_BASE.ofcbpp | grep -a "EXEC.*CICS"
?rw = grep -av "^......\*" $OF_COMPILE_IN | grep -a "REPORT" | grep -aE "SECTION|ARE" | grep -av "-"
?sql = grep -av "^......\*" $OF_COMPILE_IN | grep -a "EXEC.*SQL"
?title = grep -av "^......\*" $OF_COMPILE_IN | grep -a " TITLE '"

#=====#

[dos2unix]
$OF_COMPILE_OUT= $OF_COMPILE_IN
args = $OF_COMPILE_IN

#---

[python3]
args = check_copy.py $OF_COMPILE_IN $OF_COMPILE_OUT

#---

[ofcbpp?title]
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare

[ofcbpp?rw]
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare --enable-osvs --enable-rw

[ofcbpp]
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare --enable-osvs

#---

[tbdb2cblcv?sql]
args = $OF_COMPILE_IN > $OF_COMPILE_OUT

#---

[ofcbppe?rw]
args= -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-close-on-commit --enable-end-of-fetch-100 --enable-varchar --enable-rw
# OFCBPPE DEBUG OPTION: --enable-loglvl-debug

[ofcbppe?sql]
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-close-on-commit --enable-end-of-fetch-100 --enable-varchar
# OFCBPPE DEBUG OPTION: --enable-loglvl-debug

#---

[osccblpp?cics]
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -ne

#---

[cp]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.cob
args = $OF_COMPILE_IN $OF_COMPILE_OUT

#---

[ofcob?day_of_week]
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L$TB_HOME/client/lib -lclientcommon -ltbertl -ltbertl_odbc -L$OPENFRAME_HOME/lib/DSNTIAR.so -L$OPENFRAME_HOME/lib/DSNTIAC.so -g --notrunc --enable-ofasm
# OFCOB DEBUG OPTION: --enable-debug

[ofcob?title]
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L$TB_HOME/client/lib -lclientcommon -ltbertl -ltbertl_odbc -L$OPENFRAME_HOME/lib/DSNTIAR.so -L$OPENFRAME_HOME/lib/DSNTIAC.so -g --notrunc --enable-ofasm
# OFCOB DEBUG OPTION: --enable-debug

[ofcob?rw]
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L$TB_HOME/client/lib -ltbertl_odbc -lclientcommon -ltbertl -L$OPENFRAME_HOME/lib/DSNTIAR.so -L$OPENFRAME_HOME/lib/DSNTIAC.so -g --notrunc --enable-ofasm --enable-osvs --enable-rw
# OFCOB DEBUG OPTION: --enable-debug

[ofcob]
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L$TB_HOME/client/lib -ltbertl_odbc -lclientcommon -ltbertl -L$OPENFRAME_HOME/lib/DSNTIAR.so -L$OPENFRAME_HOME/lib/DSNTIAC.so -g --notrunc --enable-ofasm --enable-osvs
# OFCOB DEBUG OPTION: --enable-debug

#=====#

[deploy]
file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1
#tdl = 
```

This profile is the advanced profile, there are 16 sections:

- `[setup]` section: mandatory section to specify the working directory. It is also interesting to specify in this section all the environment and filter variables that are going to be used in the profile. At the time oftools_compile reads an environment variable (denoted with a `$`), it captures its value and execute the corresponding command. And this is possible to use an environment variable to define another, as it is used in this profile. For a filter variable (denoted with a `?`), this is different: oftools_compile only stores in its memory the filter variable name and value, and executes it only when it appears in one of the following sections' name. These filters are grep commands that will be executed before a section is executed. If the grep command receives a match, the return code will be set to 0 which will trigger the section using the filter variable.
  
- `[dos2unix]` section: just in case the program being compiled has been manipulated/developed on Windows before uploading and compiling in the Linux environment, it is interesting to have a [dos2unix](https://linux.die.net/man/1/dos2unix) command to converts plain text files in DOS/MAC format to UNIX format. And more specifically change the line termination character, from CRLF to LF.
  
- `[python]` section:
  
- `[ofcbpp?title]` section: OpenFrame COBOL pre-compilation, for any COBOL program. This one will be executed under the condition of the filter `?title` being **True**.
  
- `[ofcbpp?rw]` section: OpenFrame COBOL pre-compilation, for any COBOL program. This one will be executed under the condition of the filter `?rw` being **True**. If a match is found for 'REPORT' and 'SECTION', then the program enables the report writer option `(--enable-rw)` which is why the `[ofcbpp?rw]` section has the `--enable-rw` option while the normal `[ofcbpp]` section does not. If there is no match, the default section will be executed without the filter variable.
  
- `[ofcbpp]` section: OpenFrame COBOL pre-compilation, for any COBOL program. This one will be executed if the filters above for the other ofcbpp sections are **False**.
  
- `[tbdb2cblcv?sql]` section:
  
- `[ofcbppe?rw]` section:
  
- `[ofcbppe?sql]`:
  
- `[osccblpp?cics]` section: Online COBOL programs pre-compilation. This one will be executed under the condition of the filter `?cics` being **True**.
  
- `[cp]` section: many of the above sections have filters that condition their execution. Therefore, it is not possible to know in advance which section will run, and the ofcob section requires the input program to have a **.cbl** or **.cob** extension. Thus, this cp section is necessary to handle any scenario and update the file extension.
  
- `[ofcob?day_of_week]` section: OpenFrame COBOL compilation. This one will be executed under the condition of the filter `?day_of_week` being **True**.
  
- `[ofcob?title]` section: OpenFrame COBOL compilation. This one will be executed under the condition of the filter `?title` being **True**.
  
- `[ofcob?rw]` section: OpenFrame COBOL compilation. This one will be executed under the condition of the filter `?rw` being **True**.
  
- `[ofcob]` section: OpenFrame COBOL compilation. This one will be executed if the filters above for the other ofcob sections are **False**.
  
- `[deploy]` section: this section lists the target resources where the program can be deployed. It currently supports the following options:
  - **file**: rename the file and move it to a given location if specified.
  - **dataset**: move the file to the given dataset, running the command `dlupdate`.
  - **region**: move the file to the given region, running the command `osctdlupdate`.
  - **tdl**: move the file to the given region, running the command `tdlupdate`.


This profile use an additional script: [check_copy.py](../additional_scripts/check_copy.py)

### 2.3 Other profiles

These profiles are listed in chronological order of their creation date:

<details>
  <summary>Profile 1</summary>

  [Link to profile](cobol/cobol_1.prof)

  ```ini
  [setup]
  workdir = /opt/tmaxapp/compile

  # Environment variables
  $SYSVOL = /opt/tmaxapp/OpenFrame/volume/SYSVOL
  $DB2INCLUDE = $SYSVOL/DB2.INCLUDE:$SYSVOL/DB2.INCLUDE2
  $OFCOBCPY = $OFCOBCPY:$SYSVOL/OFRAME.COPYLIB:$SYSVOL/OFRAME.DCLGNLIB:$DB2INCLUDE

  # Filter variables
  ?rw = grep -av "^......\*" $OF_COMPILE_IN | grep -a "REPORT" | grep -aE "SECTION|ARE" | grep -av "-"
  ?sqlca  = grep -av "^......\*" $OF_COMPILE_IN | grep -a "01.* SQLCA "

  [dos2unix]
  $OF_COMPILE_OUT = $OF_COMPILE_IN
  args = $OF_COMPILE_IN

  [ofcbpp?rw]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-declare --enable-declare2 --collating-seq-ebcdic --enable-rw

  [ofcbpp]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-declare --enable-declare2 --collating-seq-ebcdic

  [tbpcb]
  $OF_COMPILE_OUT = $OF_COMPILE_BASE.cob
  args = INAME=$OF_COMPILE_IN ONAME=$OF_COMPILE_OUT

  [sed?sqlca]
  $OF_COMPILE_OUT = $OF_COMPILE_BASE.cob
  args  = -i 's/\(^......\) \(.*COPY \"SQLCA\"\.\)/TMAX  *\2/g' $OF_COMPILE_IN

  [ofcob?rw]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -U -L$OPENFRAME_HOME/lib -lofcee -ltextfh -ltextsm -lhidbdli -ltsys -L$TB_HOME/client/lib/ -ltbertl --enable-ofasm --enable-cbltdli --notrunc --cpm-name ASCEBCUS --init-space --enable-rw
  # OFCOB DEBUG OPTION: --enable-debug

  [ofcob]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -U -L$OPENFRAME_HOME/lib -lofcee -ltextfh -ltextsm -lhidbdli -ltsys -L$TB_HOME/client/lib/ -ltbertl --enable-ofasm --enable-cbltdli --notrunc --cpm-name ASCEBCUS --init-space
  # OFCOB DEBUG OPTION: --enable-debug

  [deploy]
  file = $OF_COMPILE_BASE.so
  ```

</details>

<details>
  <summary>Profile 2 - Batch</summary>

  [Link to profile](cobol/cobol_2.prof)

  ```ini
  [setup]
  workdir = /opt2/tmaxapp/compile

  # Environment variables
  $SOURCECPY = /opt2/tmaxwork/WORK/conv/copybook
  $OFCOBCPY = $OFCOBCPY:$OFCOB_HOME/copybook:$OPENFRAME_HOME/osc/copybook:$OPENFRAME_HOME/osc/region/OSCOIVP1/map/symbolic:$SOURCECPY/db:$SOURCECPY/fixedcopy:$SOURCECPY/rdbms:$SOURCECPY/ws-copy:$SOURCECPY/map:$SOURCECPY/msg:$SOURCECPY/pd:$TB_HOME/client/include:/opt2/tmaxwork/demosrc/copybook:/opt2/tmaxwork/YSW/NEXT_VALUE_FOR_20210218

  # Filter variables
  ?cics = grep -av "^......\*" $OF_COMPILE_IN | grep -aE "EXEC.*CICS|USING.*DFHEIBLK|USING.*DFHCOMMAREA"
  ?rw = grep -av "^......\*" $OF_COMPILE_IN | grep -a "REPORT" | grep -aE "SECTION|ARE" | grep -av "-"
  ?sql = grep -av "^......\*" $OF_COMPILE_IN | grep -a "EXEC.*SQL"

  [dos2unix]
  $OF_COMPILE_OUT= $OF_COMPILE_IN
  args = $OF_COMPILE_IN

  [ofcbpp?rw]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare --enable-rw

  [ofcbpp]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --enable-declare --enable-include

  #[tbdb2cblcv]
  #args = $OF_COMPILE_IN

  [sed]
  args = -i -e 's/\([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\)-\([0-9][0-9]\)\.\([0-9][0-9]\)\.\([0-9][0-9]\)\.\([0-9][0-9][0-9][0-9][0-9][0-9]\)/\1 \2:\3:\4.\5/g' -e 's/05  SQL-DUP-REC                   PIC S999 COMP VALUE -803./05  SQL-DUP-REC                 PIC S999 COMP VALUE +2627./g;s/ 05  SQL-DUP-REC                          PIC S999\+/05  SQL-DUP-REC                          PIC S9999/g;s/ COMP VALUE -803/COMP VALUE +2627/g' $OF_COMPILE_IN

  [ofcbppe?rw]
  args= -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-end-of-fetch-100 --enable-mssql --enable-runtime-odbc --enable-unsafe-null --enable-varchar --enable-rw
  # DEBUG OPTION: --enable-loglvl-debug

  [ofcbppe?sql]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-end-of-fetch-100 --enable-mssql --enable-runtime-odbc --enable-unsafe-null --enable-varchar
  # DEBUG OPTION: --enable-loglvl-debug

  [osccblpp?cics]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT

  [cp]
  $OF_COMPILE_OUT = $OF_COMPILE_BASE.cob
  args = $OF_COMPILE_IN $OF_COMPILE_OUT

  [ofcob?rw]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -lconcli -ladjust -lofcee -lcicsexci -L$OFCOB_HOME/lib -lcli -L$ODBC_HOME/lib -lodbc -L$OPENFRAME_HOME/lib/PSIGSFC.so -L$OPENFRAME_HOME/lib/ILBOABN0.so -L$OPENFRAME_HOME/core/lib64 -g --notrunc -O0 --enable-asa-byte -U --enable-cbltdli --save-temps --ptr-redef  --expanded --trace --force-trace --enable-rw
  # OFCOB DEBUG OPTION: --enable-debug

  [ofcob] 
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L$TB_HOME/client/lib -lclientcommon -lofcee -ltbertl -ltbertl_odbc -L$OPENFRAME_HOME/lib/DSNTIAR.so -L/opt2/tmaxwork/demosrc/copybook --notrunc -O0 --enable-asa-byte --trace --force-trace --enable-ofasm
  # OFCOB DEBUG OPTION: --enable-debug

  [deploy]
  file = $OF_COMPILE_BASE.so
  ```

</details>

<details>
  <summary>Profile 3 - Online</summary>

  [Link to profile](cobol/cobol_3.prof)

  ```ini
  [setup]
  workdir = /opt2/tmaxapp/compile

  # Environment variables
  $SOURCECPY = /opt2/tmaxwork/WORK/conv/copybook
  $OFCOBCPY = $OFCOBCPY:$OFCOB_HOME/copybook:$OPENFRAME_HOME/osc/copybook:$OPENFRAME_HOME/osc/region/OSCOIVP1/map/symbolic:$SOURCECPY/db:$SOURCECPY/fixedcopy:$SOURCECPY/rdbms:$SOURCECPY/ws-copy:$SOURCECPY/map:$SOURCECPY/msg:$SOURCECPY/pd:$TB_HOME/client/include:/opt2/tmaxwork/demosrc/copybook:/opt2/tmaxwork/YSW/NEXT_VALUE_FOR_20210218

  # Filter variables
  ?cics = grep -av "^......\*" $OF_COMPILE_IN | grep -aE "EXEC.*CICS|USING.*DFHEIBLK|USING.*DFHCOMMAREA"
  ?rw = grep -av "^......\*" $OF_COMPILE_IN | grep -a "REPORT" | grep -aE "SECTION|ARE" | grep -av "-"
  ?sql = grep -av "^......\*" $OF_COMPILE_IN | grep -a "EXEC.*SQL"


  [ofcbpp?rw]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --enable-declare --conv-stop-run --enable-rw

  [ofcbpp]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --enable-declare --enable-include

  #[tbdb2cblcv]
  #option = $OF_COMPILE_IN

  [sed]
  args = -i -e 's/\([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\)-\([0-9][0-9]\)\.\([0-9][0-9]\)\.\([0-9][0-9]\)\.\([0-9][0-9][0-9][0-9][0-9][0-9]\)/\1 \2:\3:\4.\5/g' -e 's/05  SQL-DUP-REC                   PIC S999 COMP VALUE -803./05  SQL-DUP-REC                 PIC S999 COMP VALUE +2627./g;s/ 05  SQL-DUP-REC                          PIC S999\+/05  SQL-DUP-REC                          PIC S9999/g;s/ COMP VALUE -803/COMP VALUE +2627/g' $OF_COMPILE_IN

  [ofcbppe?sql?rw]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-end-of-fetch-100 --enable-mssql --enable-runtime-odbc --enable-unsafe-null --enable-varchar --enable-close-on-commit --enable-rw
  # OFCBPPE DEBUG OPTION: --enable-loglvl-debug

  [ofcbppe?sql]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-end-of-fetch-100 --enable-mssql --enable-runtime-odbc --enable-unsafe-null --enable-varchar --enable-close-on-commit
  # OFCBPPE DEBUG OPTION: --enable-loglvl-debug

  [osccblpp?cics]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT

  [cp]
  $OF_COMPILE_OUT = $OF_COMPILE_BASE.cob
  args = $OF_COMPILE_IN $OF_COMPILE_OUT

  [ofcob?rw]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -lconcli -ladjust -lofcee -lcicsexci -L$OFCOB_HOME/lib -lcli -L$ODBC_HOME/lib -lodbc -L$OPENFRAME_HOME/lib/PSIGSFC.so -L$OPENFRAME_HOME/lib/ILBOABN0.so -L$OPENFRAME_HOME/core/lib64 -g --notrunc -O0 --enable-asa-byte -U --enable-cbltdli --save-temps --ptr-redef  --expanded --enable-rw
  # OFCOB DEBUG OPTION: --enable-debug

  [ofcob] 
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L$TB_HOME/client/lib -lclientcommon -lofcee -ltbertl -ltbertl_odbc -L$OPENFRAME_HOME/lib/DSNTIAR.so -L/opt2/tmaxwork/demosrc/copybook --notrunc -O0 --enable-asa-byte --enable-ofasm --force-trace
  # OFCOB DEBUG OPTION: --enable-debug

  [deploy]
  file = $OF_COMPILE_BASE.so
  ```

</details>

<details>
  <summary>Profile 4</summary>

  [Link to profile](cobol/cobol_4.prof)

  ```ini
  [setup]
  workdir = /opt/tmaxapp/compile

  # Environment variables
  $OFCOBCPY = $OFCOBCPY:$TB_HOME/client/include

  # Filter variables
  ?cics = grep -av "^......\*" $OF_COMPILE_IN | grep -aE "EXEC.*CICS|USING.*DFHEIBLK|USING.*DFHCOMMAREA"
  ?rw = grep -av "^......\*" $OF_COMPILE_IN | grep -a "REPORT" | grep -aE "SECTION|ARE" | grep -av "-"
  ?sql = grep -av "^......\*" $OF_COMPILE_IN | grep -a "EXEC.*SQL"

  [ofcbpp?rw]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare --enable-rw

  [ofcbpp]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare

  [osccblpp?cics]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT

  [tbpcb?sql]
  args = INAME=$OF_COMPILE_IN ONAME=$OF_COMPILE_OUT INCLUDE=$COPY_HOME END_OF_FETCH=100 COMP5=NO CODE=COBOL UNSAFE_NULL=YES VARCHAR=YES IGNORE_ERROR=YES DB2_SYNTAX=YES

  [cp]
  $OF_COMPILE_OUT = $OF_COMPILE_BASE.cob
  args = $OF_COMPILE_IN $OF_COMPILE_OUT

  [ofcob?rw]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -lconcli -ladjust -lofcee -lcicsexci -L$OFCOB_HOME/lib -lcli -L$ODBC_HOME/lib -lodbc  -L$OPENFRAME_HOME/lib/PSIGSFC.so -L$OPENFRAME_HOME/lib/ILBOABN0.so -L$OPENFRAME_HOME/core/lib64 -U --enable-cbltdli --save-temps --ptr-redef --notrunc --expanded --enable-rw
  # OFCOB DEBUG OPTION: --enable-debug

  [ofcob]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -lconcli -ladjust -lofcee -lcicsexci -L$OFCOB_HOME/lib -lcli -L$ODBC_HOME/lib -lodbc -L$OPENFRAME_HOME/lib/PSIGSFC.so -L$OPENFRAME_HOME/lib/ILBOABN0.so -L$OPENFRAME_HOME/core/lib64  -U --enable-cbltdli --save-temps --ptr-redef --notrunc --expanded
  # OFCOB DEBUG OPTION: --enable-debug

  [deploy]
  file = $OF_COMPILE_BASE.so
  dataset = SYS1.USERLIB
  #region = OSCOIVP1
  ```

</details>

<details>
  <summary>Profile 5</summary>

  [Link to profile](cobol/cobol_5.prof)

  ```ini
  [setup]
  workdir = /opt/tmaxapp/compile

  # Environment variables
  $SOURCECPY = /opt/source/copybook
  $OFCOBCPY = $OFCOBCPY:$OFCOB_HOME/copybook:$OPENFRAME_HOME/osc/copybook:$OPENFRAME_HOME/osc/region/OSCOIVP1/map/symbolic:$SOURCECPY/COPYBOOK.COMMON:$SOURCECPY/COPYBOOK.CICS:$SOURCECPY/COPYBOOK.DDL:$SOURCECPY/COPYBOOK.UPDATED:$SOURCECPY/MSTR.COPYLIB:$SOURCECPY/COPYBOOK.MSTRTSS:/opt/source/MAPSETS/MAPSET.COPYBOOK.MSTR:/opt/source/MAPSETS/MAPSET.COPYBOOK.MSTRBDS

  # Filter variables
  ?cics = grep -av "^......\*" $OF_COMPILE_IN | grep -aE "EXEC.*CICS|USING.*DFHEIBLK|USING.*DFHCOMMAREA"
  ?day_of_week = grep -a "FROM DAY-OF-WEEK" $OF_COMPILE_IN
  ?online = grep -av "^......\*" $OF_COMPILE_BASE.ofcbpp | grep -a "EXEC.*CICS"
  ?sql = grep -av "^......\*" $OF_COMPILE_IN | grep -a "EXEC.*SQL"
  ?title = grep -av "^......\*" $OF_COMPILE_IN | grep -a " TITLE '"

  [python3]
  args = check_copy.py $OF_COMPILE_IN $OF_COMPILE_OUT

  [dos2unix]
  $OF_COMPILE_OUT= $OF_COMPILE_BASE
  args = $OF_COMPILE_BASE.python

  [ofcbpp?title]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare

  [ofcbpp]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT -copypath $OFCOBCPY --add-miss-period --conv-stop-run --enable-declare --enable-osvs

  [tbdb2cblcv?sql]
  args = $OF_COMPILE_IN > $OF_COMPILE_OUT

  [ofcbppe?sql]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-close-on-commit --enable-end-of-fetch-100 --enable-varchar

  [osccblpp?cics]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -ne

  [ofcob?day_of_week]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L${TB_HOME}/client/lib -lclientcommon -ltbertl -ltbertl_odbc -L$OPENFRAME_HOME/lib/DSNTIAR.so -L$OPENFRAME_HOME/lib/DSNTIAC.so --enable-ofasm -g --notrunc
  # OFCOB DEBUG OPTION: --enable-debug

  [ofcob?title]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L${TB_HOME}/client/lib -lclientcommon -ltbertl -ltbertl_odbc -L$OPENFRAME_HOME/lib/DSNTIAR.so -L$OPENFRAME_HOME/lib/DSNTIAC.so --enable-ofasm -g --notrunc
  # OFCOB DEBUG OPTION: --enable-debug

  [ofcob]
  args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -L$OPENFRAME_HOME/lib -ltextfh -ltextsm -L${TB_HOME}/client/lib -ltbertl_odbc -lclientcommon -ltbertl -L$OPENFRAME_HOME/lib/DSNTIAR.so -L$OPENFRAME_HOME/lib/DSNTIAC.so --enable-ofasm -g --notrunc --enable-osvs
  # OFCOB DEBUG OPTION: --enable-debug

  [sh?online]
  args = deploy_online.sh $OF_COMPILE_BASE

  [sh]
  args = deploy_batch.sh $OF_COMPILE_BASE SYS1.NONIDMS.COBLIB

  #[deploy?online]
  #file = $OF_COMPILE_BASE.so
  #region = $REGION_NAME

  #[deploy]
  #file = $OF_COMPILE_BASE.so
  #dataset = SYS1.NONIDMS.COBLIB
  ```

This profile use additional scripts: 
- [check_copy.py](../additional_scripts/check_copy.py)
- [deploy_online.sh](../additional_scripts/deploy_online.sh)
- [deploy_batch.sh](../additional_scripts/deploy_batch.sh)

</details>

## 3. Assembler

<a href="#top">Back to top</a>

### 3.1 Default profile

```ini
[setup]
workdir = /opt/tmaxapp/compile

[ofasmpp]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.asmi
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT

[ofasma]
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT 
```

This one is very simple, there are only 3 sections:

- `[setup]` section: mandatory section to specify the working directory.
- `[ofasmpp]` section: OpenFrame ASM pre-compilation execution.
- `[ofasma]` section: OpenFrame ASM assembly execution.

### 3.2 Advanced profile

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/asm
#mandatory = ofasmpp:ofasma

# Environment variables
$SOURCEMACROS = /opt/source/MACROS
$OFASM_MACLIB = $OFASM_HOME/maclib/ofmac:$SOURCEMACROS/maclib_38:$SOURCEMACROS/MACROS.CICS:$SOURCEMACROS/MACROS.COMMON:$SOURCEMACROS/MODIFIED.MACROS.CICS:$SOURCEMACROS/MODIFIED.MACROS.COMMON:$SOURCEMACROS/CICSVS.SOFT.MACLIB:$SOURCEMACROS/MACROS.SOFTQPR30

# Filter variables

# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always
?cics = grep -av "\*" $OF_COMPILE_IN | grep -a "EXEC[]*CICS"

#=====#

[dos2unix]
$OF_COMPILE_OUT= $OF_COMPILE_IN
args = $OF_COMPILE_IN

#---

[cp]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.asm
args = $OF_COMPILE_IN $OF_COMPILE_OUT

#---

# Preprocessing
[ofasmpp?cics]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.asmi
args = -i $OF_COMPILE_IN -o  $OF_COMPILE_OUT --enable-cics

[ofasmpp]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.asmi
args = -i $OF_COMPILE_IN -o  $OF_COMPILE_OUT

#---

# Assembly
[ofasma]
args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT

#---

[sh]
args =  create_json.sh $OF_COMPILE_BASE

#---

[ofasmif]
args = -i $OF_COMPILE_BASE.json

#---

[g++]
args = ${OF_COMPILE_BASE}_OFASM_VM_ENTRY.cpp -o $OF_COMPILE_BASE.so -m32 -shared -fPIC -L$OFASM_HOME/lib -lofasmVM -L$TMAXDIR/lib -lcli

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.asmo
#dataset = SYS1.USERLIB 
#region = OSCOIVP1
#tdl =
```

This profile is the advanced profile, there are 16 sections:

- `[setup]` section: mandatory section to specify the working directory. It is also interesting to specify in this section all the environment and filter variables that are going to be used in the profile. At the time oftools_compile reads an environment variable (denoted with a `$`), it captures its value and execute the corresponding command. And this is possible to use an environment variable to define another, as it is used in this profile. For a filter variable (denoted with a `?`), this is different: oftools_compile only stores in its memory the filter variable name and value, and executes it only when it appears in one of the following sections' name. These filters are grep commands that will be executed before a section is executed. If the grep command receives a match, the return code will be set to 0 which will trigger the section using the filter variable.
  
- `[dos2unix]` section: just in case the program being compiled has been manipulated/developed on Windows before uploading and compiling in the Linux environment, it is interesting to have a [dos2unix](https://linux.die.net/man/1/dos2unix) command to converts plain text files in DOS/MAC format to UNIX format. And more specifically change the line termination character, from CRLF to LF.
  
- `[cp]` section: the following sections require the input program to have a **.asm** extension. Thus, this cp section is necessary to handle any scenario and update the file extension.
  
- `[ofasmpp?cics]` section: OpenFrame ASM pre-compilation execution. This one will be executed under the condition of the filter `?cics` being **True**.
  
- `[ofasmpp]` section: OpenFrame ASM pre-compilation execution. This one will be executed if the filters above for the other ofasmpp sections are **False**.
  
- `[ofasma]` section: OpenFrame ASM assembly execution.
  
- `[sh]` section:
  
- `[ofasmif]` section:
  
- `[g++]` section: GCC C++ compilation.
  
- `[deploy]` section: this section lists the target resources where the program can be deployed. It currently supports the following options:
  - **file**: rename the file and move it to a given location if specified.
  - **dataset**: move the file to the given dataset, running the command `dlupdate`.
  - **region**: move the file to the given region, running the command `osctdlupdate`.
  - **tdl**: move the file to the given region, running the command `tdlupdate`.

This profile use an additional script: [create_json.sh](../additional_scripts/create_json.sh)

### 3.3 Other examples

<details>
  <summary>Profile 1</summary>

  ```ini
  [setup]
  workdir = /opt/tmaxapp/compile

  # Filter variables
  ?cics = grep -av "^\*|^\.\*" $OF_COMPILE_IN | grep -a "EXEC.*CICS"

  [ofasmpp?cics]
  $OF_COMPILE_OUT = $OF_COMPILE_BASE.asmi
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT --enable-cics

  [ofasmpp]
  $OF_COMPILE_OUT = $OF_COMPILE_BASE.asmi
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT

  [ofasma]
  args = -i $OF_COMPILE_IN -o $OF_COMPILE_OUT 

  [deploy]
  file = $OF_COMPILE_BASE.asmo
  ```

</details>

## 4. Copybook

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/cpy
#mandatory = 

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

## 5. JCL

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/jcl
#mandatory = 

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

## 6. Proc

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/proc
#mandatory = 

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

## 7. Assembler Interface

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/asm_int
#mandatory = g++

# Environment variables
$pgm = $(echo $OF_COMPILE_IN | cut -d'_' -f 1)

# Filter variables

# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always
?entry = grep -a 'OFASM_VM_ENTRY' $OF_COMPILE_IN
?exit = grep -a 'OFASM_VM_EXIT' $OF_COMPILE_IN
?load = grep -a 'OFASM_VM_LOAD' $OF_COMPILE_IN

#=====#

[dos2unix]
$OF_COMPILE_OUT= $OF_COMPILE_IN
args = $OF_COMPILE_IN

#---

[g++?entry]
$OF_COMPILE_OUT = ${pgm}.so
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -fPIC -shared -g -L$OFASM_HOME/lib -lofasmVM -L$TMAXDIR/lib -lcli

[g++?exit]
$OF_COMPILE_OUT = ${pgm}_VM_EXIT.so
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -fPIC -shared -g -L$OFASM_HOME/lib -lofasmVM -L$TMAXDIR/lib -lcli

[g++?load]
$OF_COMPILE_OUT = ${pgm}_VM_LOAD.so
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -fPIC -shared -g -L$OFASM_HOME/lib -lofasmVM -L$TMAXDIR/lib -lcli

#=====#

[deploy]
file = $OF_COMPILE_IN
dataset = SYS1.USERLIB 
#region = OSCOIVP1
#tdl =
```

There are 6 sections in this profile:

- `[setup]` section: mandatory section to specify the working directory. It is also interesting to specify in this section all the environment and filter variables that are going to be used in the profile. At the time oftools_compile reads an environment variable (denoted with a `$`), it captures its value and execute the corresponding command. And this is possible to use an environment variable to define another, as it is used in this profile. For a filter variable (denoted with a `?`), this is different: oftools_compile only stores in its memory the filter variable name and value, and executes it only when it appears in one of the following sections' name. These filters are grep commands that will be executed before a section is executed. If the grep command receives a match, the return code will be set to 0 which will trigger the section using the filter variable.
  
- `[dos2unix]` section: just in case the program being compiled has been manipulated/developed on Windows before uploading and compiling in the Linux environment, it is interesting to have a [dos2unix](https://linux.die.net/man/1/dos2unix) command to converts plain text files in DOS/MAC format to UNIX format. And more specifically change the line termination character, from CRLF to LF.
  
- `[g++?entry]` section: GCC C++ compilation. This one will be executed under the condition of the filter `?entry` being **True**.
  
- `[g++?exit]` section: GCC C++ compilation. This one will be executed under the condition of the filter `?exit` being **True**.
  
- `[g++?load]` section: GCC C++ compilation. This one will be executed under the condition of the filter `?load` being **True**.
  
- `[deploy]` section: this section lists the target resources where the program can be deployed. It currently supports the following options:
  - **file**: rename the file and move it to a given location if specified.
  - **dataset**: move the file to the given dataset, running the command `dlupdate`.
  - **region**: move the file to the given region, running the command `osctdlupdate`.
  - **tdl**: move the file to the given region, running the command `tdlupdate`.

## 8. C Language

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/c
#mandatory = gcc

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

[dos2unix]
$OF_COMPILE_OUT= $OF_COMPILE_IN
args = $OF_COMPILE_IN

#---

[gcc]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.so
args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -fPIC -shared -g -v -Wall -trigraphs -I${GIT_HOME}/src/INCLUDE  
#args = $OF_COMPILE_IN -o $OF_COMPILE_OUT -g -v -Wall -fPIC -shared -trigraphs -Ddig="unsigned char"

#=====#

[deploy]
file = $OF_COMPILE_BASE.so
dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl = 
```

There are 4 sections in this profile:

- `[setup]` section: mandatory section to specify the working directory. It is also interesting to specify in this section all the environment and filter variables that are going to be used in the profile. At the time oftools_compile reads an environment variable (denoted with a `$`), it captures its value and execute the corresponding command. And this is possible to use an environment variable to define another, as it is used in this profile. For a filter variable (denoted with a `?`), this is different: oftools_compile only stores in its memory the filter variable name and value, and executes it only when it appears in one of the following sections' name. These filters are grep commands that will be executed before a section is executed. If the grep command receives a match, the return code will be set to 0 which will trigger the section using the filter variable.
  
- `[dos2unix]` section: just in case the program being compiled has been manipulated/developed on Windows before uploading and compiling in the Linux environment, it is interesting to have a [dos2unix](https://linux.die.net/man/1/dos2unix) command to converts plain text files in DOS/MAC format to UNIX format. And more specifically change the line termination character, from CRLF to LF.
  
- `[gcc]` section: GCC C compilation.
  
- `[deploy]` section: this section lists the target resources where the program can be deployed. It currently supports the following options:
  - **file**: rename the file and move it to a given location if specified.
  - **dataset**: move the file to the given dataset, running the command `dlupdate`.
  - **region**: move the file to the given region, running the command `osctdlupdate`.
  - **tdl**: move the file to the given region, running the command `tdlupdate`.

## 9. C++ Language

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/cpp
#mandatory = g++

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

[dos2unix]
$OF_COMPILE_OUT= $OF_COMPILE_IN
args = $OF_COMPILE_IN

#---

[g++]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.so
option = $OF_COMPILE_IN -o $OF_COMPILE_OUT -fPIC -shared -m32 -L$OPENFRAME_HOME/lib -ltcfh -I$OPENFRAME_HOME/include -std=c++11

#=====#

[deploy]
file = $OF_COMPILE_BASE.so
dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

There are 4 sections in this profile:

- `[setup]` section: mandatory section to specify the working directory. It is also interesting to specify in this section all the environment and filter variables that are going to be used in the profile. At the time oftools_compile reads an environment variable (denoted with a `$`), it captures its value and execute the corresponding command. And this is possible to use an environment variable to define another, as it is used in this profile. For a filter variable (denoted with a `?`), this is different: oftools_compile only stores in its memory the filter variable name and value, and executes it only when it appears in one of the following sections' name. These filters are grep commands that will be executed before a section is executed. If the grep command receives a match, the return code will be set to 0 which will trigger the section using the filter variable.
  
- `[dos2unix]` section: just in case the program being compiled has been manipulated/developed on Windows before uploading and compiling in the Linux environment, it is interesting to have a [dos2unix](https://linux.die.net/man/1/dos2unix) command to converts plain text files in DOS/MAC format to UNIX format. And more specifically change the line termination character, from CRLF to LF.
  
- `[g++]` section: GCC C++ compilation.
  
- `[deploy]` section: this section lists the target resources where the program can be deployed. It currently supports the following options:
  - **file**: rename the file and move it to a given location if specified.
  - **dataset**: move the file to the given dataset, running the command `dlupdate`.
  - **region**: move the file to the given region, running the command `osctdlupdate`.
  - **tdl**: move the file to the given region, running the command `tdlupdate`.

## 10. SQL

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/sql
#mandatory = 

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

## 11. BMS Map

### 11.1 Default profile

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/bms_maps

# Filter variables

# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always
?copy = grep -a "^=COPY DPUNCHK4|^=COPY DFHMDFK4|^=COPY DFHMDIK4|^=COPY QCAMDFK4" $OF_COMPILE_IN

#=====#

[dos2unix]
$OF_COMPILE_OUT= $OF_COMPILE_IN
args = $OF_COMPILE_IN

#---

[sed?copy]
$OF_COMPILE_OUT = $OF_COMPILE_IN
args = -i -e 's/^=COPY DPUNCHK4/*=COPY DPUNCHK4/g;s/^=COPY DFHMDFK4/*=COPY DFHMDFK4/g;s/^=COPY DFHMDIK4/*=COPY DFHMDIK4/g' -e 's/^=COPY /         COPY /g' $OF_COMPILE_IN

#---

[cp]
$OF_COMPILE_OUT = $OF_COMPILE_BASE.org
args = $OF_COMPILE_IN $OF_COMPILE_BASE.org

#---

[asmapgen]
$OF_COMPILE_OUT = $OF_COMPILE_BASE
args = -i $OF_COMPILE_IN -o $OF_COMPILE_BASE

#---

[mscasmc]
args = $OF_COMPILE_IN

#---

[mscmapc]
args = $OF_COMPILE_IN
#args = $OF_COMPILE_IN -r REGION_NAME
#args = -s $OF_COMPILE_IN $OF_COMPILE_BASE.atm

#[sh]
#option = deploy_map.sh $OF_COMPILE_IN

#=====#
```

There are 8 sections in this profile:

- `[setup]` section: mandatory section to specify the working directory. It is also interesting to specify in this section all the environment and filter variables that are going to be used in the profile. At the time oftools_compile reads an environment variable (denoted with a `$`), it captures its value and execute the corresponding command. And this is possible to use an environment variable to define another, as it is used in this profile. For a filter variable (denoted with a `?`), this is different: oftools_compile only stores in its memory the filter variable name and value, and executes it only when it appears in one of the following sections' name. These filters are grep commands that will be executed before a section is executed. If the grep command receives a match, the return code will be set to 0 which will trigger the section using the filter variable.
  
- `[dos2unix]` section: just in case the program being compiled has been manipulated/developed on Windows before uploading and compiling in the Linux environment, it is interesting to have a [dos2unix](https://linux.die.net/man/1/dos2unix) command to converts plain text files in DOS/MAC format to UNIX format. And more specifically change the line termination character, from CRLF to LF.
  
- `[sed?copy]` section:
  
- `[cp]` section:
  
- `[asmapgem]` section:
  
- `[mscasmc]` section:
  
- `[mscmapc]` section:
  
- `[deploy]` section: this section lists the target resources where the program can be deployed. It currently supports the following options:
  - **file**: rename the file and move it to a given location if specified.
  - **dataset**: move the file to the given dataset, running the command `dlupdate`.
  - **region**: move the file to the given region, running the command `osctdlupdate`.
  - **tdl**: move the file to the given region, running the command `tdlupdate`.

This profile use an additional script: [deploy_map.sh](../additional_scripts/deploy_map.sh)

### 11.2 Other examples

<details>
  <summary>Profile 1</summary>

```ini
[setup]
workdir = /opt/tmaxapp/compile

# Environment variables

# Filter variables

[mscasmc]
$OF_COMPILE_OUT = OF_COMPILE_BASE.atm
args = $OF_COMPILE_IN -o OF_COMPILE_BASE.atm

[mscmapc]
args = -r OSCOIVP1 $OF_COMPILE_IN

[mscmapupdate] 
args = OSCOIVP1 -l $OF_COMPILE_BASE
```

## 12. CICS CSD

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/cics_csd
#mandatory = 

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#
```

</details>

## 13. Control

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/ctl
#mandatory = 

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

## 14. Easytrieve

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/easytrieve

# Environment variables
$SOURCE_EASYTRIEVE = /opt/source/EASYTRIEVE/EASYPLUS

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

[dos2unix]
$OF_COMPILE_OUT= $OF_COMPILE_IN
args = $OF_COMPILE_IN

#---

[protp]
args = -i $OF_COMPILE_IN -l $SOURCE_EASYTRIEVE

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

There are 4 sections in this profile:

- `[setup]` section: mandatory section to specify the working directory. It is also interesting to specify in this section all the environment and filter variables that are going to be used in the profile. At the time oftools_compile reads an environment variable (denoted with a `$`), it captures its value and execute the corresponding command. And this is possible to use an environment variable to define another, as it is used in this profile. For a filter variable (denoted with a `?`), this is different: oftools_compile only stores in its memory the filter variable name and value, and executes it only when it appears in one of the following sections' name. These filters are grep commands that will be executed before a section is executed. If the grep command receives a match, the return code will be set to 0 which will trigger the section using the filter variable.
  
- `[dos2unix]` section: just in case the program being compiled has been manipulated/developed on Windows before uploading and compiling in the Linux environment, it is interesting to have a [dos2unix](https://linux.die.net/man/1/dos2unix) command to converts plain text files in DOS/MAC format to UNIX format. And more specifically change the line termination character, from CRLF to LF.
  
- `[protp]` section: Protrieve compilation.
  
- `[deploy]` section: this section lists the target resources where the program can be deployed. It currently supports the following options:
  - **file**: rename the file and move it to a given location if specified.
  - **dataset**: move the file to the given dataset, running the command `dlupdate`.
  - **region**: move the file to the given region, running the command `osctdlupdate`.
  - **tdl**: move the file to the given region, running the command `tdlupdate`.

## 15. Easytrieve Plus

<a href="#top">Back to top</a>

```ini
[setup]
workdir = $COMPILE_WORK_DIR
#workdir = /opt/tmaxapp/compile
#workdir = /opt/tmaxapp/compile/easytrieve_plus
#mandatory = 

# Environment variables

# Filter variables
# If you want to manually test the filters, you can add to the first grep the
# following options: -nH --color=always

#=====#

#[deploy]
#file = $OF_COMPILE_BASE.so
#dataset = SYS1.USERLIB
#region = OSCOIVP1 
#tdl =
```

## 16. Environment variables resources

<a href="#top">Back to top</a>

```ini
$VOLUME_DEFAULT = /opt/tmaxapp/OpenFrame/volume_default
```
