#!/usr/bin/python3

# Import the os module, for the os.walk function
import os
from shutil import copyfile
import PTN
import sys, re

from tqdm import tqdm
from progressbar import Percentage, Bar, ETA, ProgressBar
from time import sleep
import threading
import multiprocessing

rootDir = '/home/logan/Downloads'
backupDir = '/home/logan/Videos'

# ==========================================================================================================
# ==========================================================================================================
# ==========================================================================================================

def handleSeason(name):
	return 'S' + str(name).zfill(2)

def handleEpisode(name):
	return 'E' + str(name).zfill(2)

def handleName(name):
	flags = ['ncis', 'dcs']
	newName = name.title().split(' ')
	if newName[0].lower() in flags:
		newName[0] = newName[0].upper() + '_'
	return ''.join(newName)


def parseName(name, extension):
	newName = PTN.parse(name)
	
	if "episode" in newName:
		# print(str(newName['season']).zfill(2))
		season = handleSeason(newName['season'])
		episode = handleEpisode(newName['episode'])
		# print(newName['title'] + season + episode)
		title = handleName(newName['title'])
		fileName = title + '-' + season + episode + '.' + extension
		# os.rename(name, fileName)
		return fileName.replace('_-', '_')
	else:
		flags = '!@#$%^*()_+-. '
		newName = newName['title'].title()
		for c in flags:
			if c in newName:
				newName = stringReplace(newName, c)
		return newName + '.' + extension
	# return name + extension

def stringReplace(name, flag):
	# return re.sub(flag, "", string)
	return name.replace(flag, "")
	# return re.sub(flag, "", string)

# ==========================================================================================================
# ==========================================================================================================
# ==========================================================================================================


def walk_directory_tree2():
	flag_list = ['.mkv', '.avi', '.mp4']
	# Set the directory you want to start from
	rootDir = '.'
	for dirName, subdirList, fileList in os.walk(rootDir):
	    for fname in fileList:
	    	filename, file_extension = os.path.splitext(fname)
	    	if file_extension in flag_list:
	    		newName = parseName(filename, file_extension.replace('.', ''))
		    	# print('Copying file -- {} --'.format(newName))
		    	copyMovies(os.path.join(dirName, fname), os.path.join(backupDir, newName))
		    	print('\n-------------------------------------\n')
		    	# print(os.path.join(dirName, fname), os.path.join(backupDir, newName))
		    	# print('{}'.format(newName))

def startCopy(src, dest):
	# print('Copying file -- {}'.format(dest))
	copyfile(src, dest)

def startProgress(src, dest):
	fileSize = os.path.getsize(src)
	progress, progress_max_value = 0, fileSize
	pbar = ProgressBar(widgets=[dest + ' --- ', Percentage(), Bar(), ' ', ETA(), ], maxval = progress_max_value).start()

	# flag = os.path.getsize(dest)
	while progress <= progress_max_value-2048:
		progress = os.path.getsize(dest)
		pbar.update(progress)
	pbar.finish()


def copyMovies(src, dest):
	processes = [multiprocessing.Process(target=startCopy, args=(src, dest)), 
			     multiprocessing.Process(target=startProgress, args=(src, dest))]

	for t in processes:
		t.start()
		sleep(.05)
	
	for t in reversed(processes):
		t.join()

def copyMovies2(src, dest):
	threads = [threading.Thread(target=startCopy, args=(src, dest)), 
			threading.Thread(target=startProgress, args=(src, dest))]

	for t in threads:
		t.start()
		sleep(.05)
	
	for t in reversed(threads):
		t.join()

def printFileNames(file_names):
	for name in file_names:
		print('{}'.format(name))
	print('{}'.format(len(file_names)))

def main():
	os.chdir(rootDir)
	walk_directory_tree2()
	print('\n', '*************** COPY COMPLETED!!! ***************', '\n\n\n')
	# printFileNames(paths)

if __name__ == '__main__':
	main()
