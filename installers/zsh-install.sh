#!/bin/bash
set -e

###################################################################
###################################################################
# Author	:	Roger Delgado
###################################################################
###################################################################

packages=(zsh zsh-syntax-highlighting zsh-completions zsh-lovers neofetch)

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


function getOhMyZSH {
# Installation of OH-MY-ZSH from the github (best way to install!!)

echo "################################################################"
echo "downloading Oh-My-Zsh from github"
echo "################################################################"

wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | sh

# changing the theme to random so you can enjoy tons of themes.

sudo sed -i 's/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"random\"/g' ~/.zshrc

# If above line did not work somehow. This is what you should do to enjoy the many themes.
# go find the hidden .zshrc file and look for ZSH_THEME="robbyrussell" (CTRL+H to find hidden files)
# change this to ZSH_THEME="random"

echo '
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
neofetch
' >>  ~/.zshrc

}




for item in "${packages[@]}"
do
	getPackage $item
done

if [ -d ~/.oh-my-zsh ]
then
	echo "Oh-My-ZSH is already installed!"
else
	getOhMyZSH

fi




echo $SHELL

if [ "$zsh" == "/usr/bin/zsh" ]
then
	echo "ZSH is already set!"
else
	chsh -s /usr/bin/zsh
	sudo chsh -s /bin/zsh
	echo "ZSH is now set! Logout to apply settings!"
fi









