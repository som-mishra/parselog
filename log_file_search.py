#!/usr/bin/python

import argparse
import datetime
import gzip
import os
import re
import sys

DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')


# input format: "yyyy-mm-dd hh:mm:ss" (not necessarily all these fields) and a string (uuid for example)
# program takes in the format, and is run inside of a directory with .txt.gz files. 
# output is all lines in all of these .txt.gz files that contain the inputs above
# ex: findLines.py 2016-03-07 02:34
# output: 
        # 2016-03-07 02:34...<uuid>...
        # 2016-03-07 02:34...<uuid>...
        # 2016-03-07 02:34...<uuid>...
        # 2016-03-07 02:34...<uuid>...
        # 2016-03-07 02:34...<uuid>...
        # 2016-03-07 02:34...<uuid>...

def read_file (myinputfile):
    if myinputfile.endswith('.gz'):
        with gzip.open(myinputfile, 'rb') as f:
            filecontent = f.readlines()
    else:
        with open(myinputfile, 'rb') as f:
            filecontent = f.readlines()

    return filecontent

	
def process_file2(content, mydate=None, mytime=None, mystring=None):

    pattern = "%Y-%m-%d %H:%M:%S.%f"

    input_datetime = datetime.datetime.strptime("{} {}".format(mydate, mytime) , pattern)

    output = []
    match = 0
    for line in content:
        line = line.rstrip()

        if not match: #until we reach a match point in the file in terms of date/time
            if mystring and mystring not in line:
                continue

            line_datetime = get_line_datetime(line)

            if line_datetime is not None:
                if line_datetime >= input_datetime:
                    output.append(line)
                    match = 1
        else:
            # At this point we have found a date/time match and now we print all future lines that match our string search parameter, if specified
            if mystring:
                if mystring in line:
                    output.append(line)
            else:
                # mystring not set, therefore output the line
                output.append(line)

        #if you have reached here, this is one of your output line
    return output
		
		
def get_line_datetime(line):
    """Given a logfile line, determine the datetime of the line

    :param line: logfile line to parse
    :returns: datetime.datetime() object if datetime found
    :returns: None if no datetime found
    """
    if not DATETIME_RE.search(line):
        return None
    
    splitline = line.split(' ', 2) #collect for just the date and time parts
    filedatetime = splitline[0] + ' ' + splitline[1]
    pattern = "%Y-%m-%d %H:%M:%S.%f"
    try:
        parsed_datetime = datetime.datetime.strptime(filedatetime, pattern)
    except ValueError:
        parsed_datetime = None
    return parsed_datetime
    
 
def process_all_input_files(myfiles, mydate, mytime, mystring):
    for myfile in myfiles:
        content = read_file (myfile)
        result = process_file2(content, mydate, mytime, mystring)
        print "\n"
        print "Found in file: ", myfile
        print "\n"
        for line in result:
            print line



def get_all_input_files(mypath):
    files = [f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath, f)) and f.endswith(('.txt', '.txt.gz')))]

    return files

def validate_inputs(date_val, time_val):

    if date_val:
        dateparts = date_val.split('-')
        if len(dateparts) == 3:
            pass
        elif len(dateparts) == 2:
		    date_val = date_val + '-01'
        elif len(dateparts) == 1:
            date_val = date_val + '-01-01'

    if time_val:
        timeparts = time_val.split(':')
        if len(timeparts) == 3:
            if (re.search('\.', timeparts[2])):
                pass
            else:
                time_val = time_val + '.000'
        elif len(timeparts) == 2:
            time_val = time_val + ':00.000'
        elif len(timeparts) == 1:
            time_val = time_val + ':00:00.000'
    else:
        time_val = "00:00:00.001"

    try:
        datetime.datetime.strptime(date_val, '%Y-%m-%d')
    except ValueError:
        date_val = None

    try:
        datetime.datetime.strptime(time_val, '%H:%M:%S.%f')
    except ValueError:
        time_val = None

    return date_val, time_val



def parse_inputs():

    parser = argparse.ArgumentParser(description="log_file_search.py")

    parser.add_argument("-p", "--path", dest="PATH", help="Enter the full path to the location of the files that need to be queried' dir", required=True, default=".")
    parser.add_argument("-d", "--date", dest="DATE", help="Enter a search date in the format YYYY-MM-DD. Ex: 2016-09-23", required=True, default="")
    parser.add_argument("-t", "--time", dest="TIME", help="Enter a search time (24hr time) in the format hh-mm-ss.ffff. Ex: 16:23:43.231", default=None)
    parser.add_argument("-s", "--string", dest="STRING", help="Enter a search string", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", dest="VERBOSE", help="Verbose mode", default=False)

    args = parser.parse_args()
    return args

def main():
    
    if args.VERBOSE:	
        print "args:", args

    if args.PATH:
        if not os.path.exists(args.PATH):
            print ("Path:[%s] does not exist. Check your input." % args.PATH)
            sys.exit(1)

    date_val, time_val = validate_inputs(args.DATE, args.TIME)
    if date_val is None:
        print "Invalid date value supplied: {}".format(args.DATE)
        print "Date should be in the format YYYY-MM-DD for example 2016-01-22"
        sys.exit(1)

    if time_val is None:
        print "Invalid date value supplied: {}".format(args.TIME)
        print "Time should be in the format HH:MM:SS.FFF for example 15:23:43.123"
        sys.exit(1)
	
    inputfiles = get_all_input_files(args.PATH)

    process_all_input_files(inputfiles, date_val, time_val, args.STRING)
	


if __name__ == '__main__':
    #Use 2.7 version of python
    ver = (2, 7)
    if sys.version_info[:2] != ver:
        print("ERROR: Use Python Version: 2.7")
        sys.exit()

    args = parse_inputs()

    main()



