#!/bin/bash
set -e

###################################################################
###################################################################
# Author	:	Roger Delgado
###################################################################
###################################################################

packages=(neovim python-neovim)

echo "${packages[@]}"

function printItem {
	echo $1
}

function getPackage {
#------------------------------------------------------------------

#checking if application is already installed or else install with aur helpers
if pacman -Qi $1 &> /dev/null; then

		echo "################################################################"
		echo "################## "$1" is already installed"
		echo "################################################################"

else

	#checking which helper is installed
	if pacman -Qi yay &> /dev/null; then

		echo "################################################################"
		echo "######### Installing with yay"
		echo "################################################################"
		yay -S --noconfirm $1

	elif pacman -Qi trizen &> /dev/null; then

		echo "################################################################"
		echo "######### Installing with trizen"
		echo "################################################################"
		trizen -S --noconfirm --needed --noedit $1

	elif pacman -Qi yaourt &> /dev/null; then

		echo "################################################################"
		echo "######### Installing with yaourt"
		echo "################################################################"
		yaourt -S --noconfirm $1

	elif pacman -Qi pacaur &> /dev/null; then

		echo "################################################################"
		echo "######### Installing with pacaur"
		echo "################################################################"
		pacaur -S --noconfirm --noedit  $1

	elif pacman -Qi packer &> /dev/null; then

		echo "################################################################"
		echo "######### Installing with packer"
		echo "################################################################"
		packer -S --noconfirm --noedit  $1

	fi

	# Just checking if installation was successful
	if pacman -Qi $1 &> /dev/null; then

		echo "################################################################"
		echo "#########  "$1" has been installed"
		echo "################################################################"

	else

		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		echo "!!!!!!!!!  "$1" has NOT been installed"
		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

	fi

fi

####################################################################################
}



for item in "${packages[@]}"
do
	getPackage $item
done

