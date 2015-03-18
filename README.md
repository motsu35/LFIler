This is a simple tool used to pull files off of a remote system with a local file inclusion vulnerability.

It was my first ever python script, so im sure its not the best, and not very python like, but it works!

to get started run with -h to see all the commands. you need to generate a word list, the best way to do this is check /etc/issue on the remote system though the LFI and see the system its running.
set up the same system with whatever web stack they are running. Then build a worklist using find which the tool will use to then find files.



ToDo:
	check files for paths, and append to the wordlist real time (ie, if there website isnt in /var/www which is what your wordlist uses, but their apache config gets picked up, the file path to the remote web dir would still be scaned)
