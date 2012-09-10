#!/bin/bash

export DJANGO_SETTINGS_MODULE=footy.settings 

echo 'Clearing DB'
#python2.7 manage.py sqlclear footy | python2.7 manage.py dbshell
echo 'Recreating DB'
#python2.7 manage.py sqlall footy | python2.7 manage.py dbshell
echo 'Creating drawn team'
#python2.7 create_drawn.py

for year in `seq 2000 2012`; do
	echo "Loading season $Year"
	start=`date -d "01/01/${year}" "+%y"`
	end=`date -d "01/01/$((${year}+1))" "+%y"`
	for x in data-files/E?-${start}${end}.csv; do
		# echo $x $year
		python2.7 load.py $x $year
		if [[ $? -ne 0 ]]; then
			echo "Exiting..."
			exit 1;
		fi
	done
done
