@echo off

REM Set the starting and ending values for the loop
set startValue=1337
set endValue=1346

REM Start CMD instances in a loop
for /l %%i in (%startValue%, 1, %endValue%) do (
    REM cmd.exe /k start wsl python3 /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/main.py --port %%i
    REM cmd.exe /k start wsl python3 /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/profiler.py --write-files=True --client %%i
    
    echo wsl python3 /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/main.py --port %%i
    echo wsl python3 /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/profiler.py --write-files=True --client %%i
    echo

    REM echo cmd.exe /c start wsl py-spy record -o /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/profiled/%%i-s.svg -- python3 /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/main.py --port %%i
    REM echo cmd.exe /c start wsl py-spy record -o /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/profiled/%%i-c.svg -- python3 /mnt/c/cph/Composabl/examples.composabl.io/simulators/mujoco/src/profiler.py --client %%i
    REM echo
)


echo "CMD instances started from %startValue% to %endValue%."

REM You can add more commands or code here if needed

REM Script exits without waiting for CMD instances to close
REM exit
