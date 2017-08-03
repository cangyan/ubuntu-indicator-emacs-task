#!/bin/bash

if [ -e ~/.clockin_task ]; then
  task_name=`cat ~/.clockin_task | cut -f 2`
  start_time=`cat ~/.clockin_task | cut -f 1`

  elapsed=$(expr `date +%s` - $start_time)

  h=$(expr $elapsed / 3600)
  m=$(expr $elapsed % 3600 / 60)

  disph=`printf %02d $h`
  dispm=`printf %02d $m`

  ##echo ":hourglass_flowing_sand: [$disph:$dispm] $task_name"
  echo "[$disph:$dispm] $task_name"

else
  ##echo ":coffee: Break Time"
  echo "Break Time"
fi