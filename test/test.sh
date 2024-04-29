#!/bin/bash
source /absolute/path/to/your/env/activate
echo 1 - KVaC	2 - Pointproof	3 - CF on CDH	4 - CF on RSA
read -p "Enter choice: " choice
read -p "Enter number of message: " dim
if [ $choice = 1 ]; then
	echo ------KVaC Scheme-------
	python3 KVaC.py $dim
elif [ $choice = 2 ]; then
	echo ------Pointproof Scheme-------
	python3 pointproof.py $dim
elif [ $choice = 3 ]; then
	echo ------CF Based on CDH Scheme-------
	python3 vccdh_charm.py $dim
elif [ $choice = 4 ]; then
	echo ------CF Based on RSA Scheme-------
	python3 vccrsa.py $dim
else
	echo "No such schemes for this choice"
fi
