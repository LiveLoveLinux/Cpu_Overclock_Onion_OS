#!/bin/sh

echo -ne "\n\n"
echo --------------------------------------------------------------------
echo ":: PYTHON APP LAUNCH"
echo --------------------------------------------------------------------

AppDir=$(pwd)
AppExecutable="app.py"
Arguments=""
KillAudioserver=0
PerformanceMode=0

echo --------------------------------------------------------------------
echo ":: APPLYING ADDITIONNAL CONFIGURATION"
echo --------------------------------------------------------------------

#if [ "$KillAudioserver" = "1" ]; then . /mnt/SDCARD/.tmp_update/script/stop_audioserver.sh; fi
if [ "$PerformanceMode" = "1" ]; then echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; fi

cd "$AppDir"
HOME="$AppDir"

ParasytePath="/mnt/SDCARD/.tmp_update/lib/parasyte"
export PYTHONPATH=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
export PYTHONHOME=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
export LD_LIBRARY_PATH=$ParasytePath:$ParasytePath/python2.7/:$ParasytePath/python2.7/lib-dynload:$LD_LIBRARY_PATH

echo --------------------------------------------------------------------
echo ":: RUNNING THE APP"
echo --------------------------------------------------------------------

echo running "$AppDir/$AppExecutable" ...

eval echo -ne "Command line : \\\n\"$ParasytePath/python2\" \"$AppExecutable\" $Arguments \\\n\\\n\\\n"
eval /mnt/SDCARD/.tmp_update/bin/parasyte/python2 \"$AppExecutable\" $Arguments

echo --------------------------------------------------------------------
echo ":: POST RUNNING TASKS"
echo --------------------------------------------------------------------

unset LD_PRELOAD

echo -ne "\n\n" 