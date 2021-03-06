#!/usr/bin/env python

import sys
import os
import zipfile
import argparse

dirs = ("", "chest", "colormap", "blocks")
files = {
	"chest/normal.png" : "assets/minecraft/textures/entity/chest/normal.png",
	"chest/ender.png" : "assets/minecraft/textures/entity/chest/ender.png",
	"chest/normal_double.png" : "assets/minecraft/textures/entity/chest/normal_double.png",
	"colormap/foliage.png" : "assets/minecraft/textures/colormap/foliage.png",
	"colormap/grass.png" : "assets/minecraft/textures/colormap/grass.png",
}

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Extracts from a Minecraft Jar file the textures required for mapcrafter.")
	parser.add_argument("-f", "--force", 
					help="forces overwriting eventually already existing textures",
					action="store_true")
	parser.add_argument("jarfile",
					help="the Minecraft Jar file to use",
					metavar="<jarfile>")
	parser.add_argument("outdir",
					help="the output texture directory",
					metavar="<outdir>")
	args = vars(parser.parse_args())
	
	jar = zipfile.ZipFile(args["jarfile"])
	
	for dir in dirs:
		if not os.path.exists(os.path.join(args["outdir"], dir)):
			os.mkdir(os.path.join(args["outdir"], dir))
	
	print "Extracting block images:"
	found, extracted, skipped = 0, 0, 0
	for info in jar.infolist():
		if info.filename.startswith("assets/minecraft/textures/blocks/"):
			filename = info.filename.replace("assets/minecraft/textures/", "")
			filename = os.path.join(args["outdir"], filename)
			found += 1
			
			if os.path.exists(filename) and not args["force"]:
				skipped += 1
				continue
			
			fin = jar.open(info)
			fout = open(filename, "w")
			fout.write(fin.read())
			fin.close()
			fout.close()
			extracted += 1
	
	print " - Found %d block images." % found
	print " - Extracted %d." % extracted
	print " - Skipped %d (Use -f to force overwrite)." % skipped
	
	print ""
	print "Extracting other textures:"
	
	for filename, zipname in files.items():
		try:
			print " - Extracting" , filename , "...",
			info = jar.getinfo(zipname)
			filename = os.path.join(args["outdir"], filename)
			if os.path.exists(filename) and not args["force"]:
				print "skipped."
			else:
				fin = jar.open(info)
				fout = open(filename, "w")
				fout.write(fin.read())
				fin.close()
				fout.close()
				print "extracted."
		except KeyError:
			print "not found!"
