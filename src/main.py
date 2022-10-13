# I did not use pyton to code this by choice. I absolutely hate python. It doesn't make sense to me when I read it, and in my opinion
# using indents as syntax is the most idiotic thing ever. But, it was the most suitable language to solve the problem I have, and thus
# my hand is forced.
#
# Reluctantly written by Sheer Curiosity

from clipper.merger import mergeClips
from clipper.extractor import getAVUrls
from clipper.downloader import *
from clipper.misc import *
from utils.info import *
from utils.misc import *

import argparse
import os
import sys

ffmpeg_path = resource_path('bin/ffmpeg/ffmpeg', os.path.abspath(__file__))
tempdir_parent_path = '.'

argParser = argparse.ArgumentParser(prog='tool', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=120), usage="vcdl2 -v [VIDEO LINKS] -ts [TIMESTAMPS] [options]")
argParser.add_argument('-v', '--video-links', nargs='*', help='link(s) to download from')
argParser.add_argument('-ts', '--timestamps', nargs='*', help='timestamp set(s). see documentation for formatting guide')
argParser.add_argument('-ot', '--output-title', default='output', help='name of outputted video file or zip archive')
argParser.add_argument('-p', '--padding', default=5, type=int, choices=range(0, 31), metavar='[0-30]', help='see documentation')
argParser.add_argument('-dm', '--download-method', default='DPAMRE', type=str, choices=['DPAMRE', 'DWACFF'], metavar='[DPAMRE, DWACFF]', help='see documentation')
out_type = argParser.add_mutually_exclusive_group()
out_type.add_argument('-m', '--merge-clips', action='store_true', help='merge clips into one video file')
out_type.add_argument('-arc', '--output-archive', action='store_true', help='outputs all clips to a single zip file')
argParser.add_argument('-cf', '--cookiefile', default=None, help='Netscape cookie file for downloading private and members only videos')
argParser.add_argument('--debug', action='store_true', help='print more detailed runtime information for debugging')
args = argParser.parse_args()

if args.debug:
	print(versionInfo())
	print(buildInfo())

def runClipper(video_links: list, timestamps: list):
	urlLinks = []
	timestampSets = []

	if len(video_links) > 1 or len(timestamps) > 1:
		print('[ERROR]: Multi-link functionality not yet implemented')
		sys.exit()
	
	for link in video_links:
		urlLinks.append(getAVUrls(args.debug, link, args.cookiefile))
	
	for set in timestamps:
		timestampSets.append(parseTimestamps(args.debug, set, args.padding))

	clip_dict = downloadClips(args.debug, timestampSets, urlLinks, ffmpeg_path, tempdir_parent_path, args.download_method)

	if clip_dict > 1:
		if args.merge_clips:
			mergeClips(args.debug, clip_dict, args.output_title, ffmpeg_path, tempdir_parent_path)
		elif args.output_archive:
			compat_convert(tempdir_parent_path, ffmpeg_path)
			packupClips(args.output_title)
		else:
			for f in os.listdir(f"{tempdir_parent_path}/vcdl_temp"):
				if f.startswith('clip'):
					os.rename(os.path.join(f"{tempdir_parent_path}/vcdl_temp", f), os.path.join('./', f"{args.output_title}-{f}"))
	else:
		if os.path.exists(f"./{args.output_title}.mp4"):
			os.remove(f"./{args.output_title}.mp4")
		output_convert(args.output_title, tempdir_parent_path, ffmpeg_path)
	cleanup()

def main():
	try:
		if args.video_links != None and args.timestamps != None:
			if args.debug:
				print(f"[DEBUG]: Inputted Video Link(s): {args.video_links}")
				print(f"[DEBUG]: Inputted Timestamp Set(s): {args.timestamps}")
			runClipper(args.video_links, args.timestamps)
		else:
			argParser.print_help()
	except KeyboardInterrupt:
		print("\033[K", end="\r")
		print("[INFO]: Keyboard Interrupt recieved, exiting program...")
		cleanup()
	sys.exit(0)

if __name__ == '__main__':
	main()
