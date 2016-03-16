import argparse
import datetime
import gzip
import os
import re
import sys

DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
# import sys
# import gzip
# import argparse
# # from os import path, listdir
# # from os.path import isfile, join
# from datetime import datetime
# import os
# #import datetime

'''
opts = []
args = []
verbose = False
inputpath = ''
inputdate = ''
inputtime = ''
searchstring = ''
'''
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

	
		
# # arguemnts are passed in from the command line
# def process_file(content):
#     #content = read_file (myfile)
#     #for i in range(len(content)):
#     pattern = "%Y-%m-%d %H:%M:%S.%f"
#     print "DATE=%s"  % args.DATE
#     print "TIME=%s" % args.TIME

#     print "{} {}".format(args.DATE, args.TIME)
#     input_datetime = datetime.datetime.strptime("{} {}".format(args.DATE, args.TIME) , pattern)
#     print "input_datetime here=%s" % input_datetime
#     found_date = False
#     for line in content:
#         print "in the loop line=%s" % line
#         line = line.rstrip()
# #        if line.startswith('+') or line.startswith('Option'): # ignore first few lines
# #            continue
#         if found_date:
#             print "found_date printing"
#             print line
#             continue

#         if args.STRING and args.STRING not in line:
#             continue

#         print "line here %s" % line
#         line_datetime = get_line_datetime(line)
#         print "line_datetime= ", line_datetime
#         print "input_datetime= ", input_datetime
		
#         if line_datetime < input_datetime:
#             continue
#         found_date = True
#         #if you have reached here, this is one of your output line
#         print line

def process_file2(content, mydate=None, mytime=None, mystring=None):
    #content = read_file (myfile)
    #for i in range(len(content)):
    pattern = "%Y-%m-%d %H:%M:%S.%f"
    #print "DATE=%s"  % args.DATE
    #print "TIME=%s" % args.TIME

    #print "{} {}".format(args.DATE, args.TIME)
    input_datetime = datetime.datetime.strptime("{} {}".format(mydate, mytime) , pattern)
    #print "input_datetime here=%s" % input_datetime

    output = []
    match = 0
    for line in content:
        #print "in the loop line=%s" % line
        #print "match=%s" % match
        line = line.rstrip()

        if not match: #until we reach a match point in the file in terms of date/time
            #print "match in if=%s" % match
            if mystring and mystring not in line:
                #print "going back..."
                continue

            #print "line here %s" % line
            line_datetime = get_line_datetime(line)
            #print "line_datetime= ", line_datetime
            #print "input_datetime= ", input_datetime
            if line_datetime is not None:
                if line_datetime >= input_datetime:
                    #print "i am herererrere"
                    #print line
                    output.append(line)
                    match = 1
        else:
            # At this point we have found a date/time match and now we print all future lines that match our string search parameter, if specified
            #print "match in else=%s" % match
            # print "mystring", mystring
            if mystring:
                if mystring in line:
            # if str(mystring) in line:
                #print "printing final line"
                #print line
                    output.append(line)
            else:
                # mystring not set, therefore output the line
                output.append(line)

        #if you have reached here, this is one of your output line
        #print line
    return output
		
		
def get_line_datetime(line):
    """Given a logfile line, determine the datetime of the line

    :param line: logfile line to parse
    :returns: datetime.datetime() object if datetime found
    :returns: None if no datetime found
    """
    #print "line inside= ", line
    if not DATETIME_RE.search(line):
        return None
    
    splitline = line.split(' ', 2) #collect for just the date and time parts
    filedatetime = splitline[0] + ' ' + splitline[1]
    pattern = "%Y-%m-%d %H:%M:%S.%f"
    #print "filedatetime= ", filedatetime
    try:
        parsed_datetime = datetime.datetime.strptime(filedatetime, pattern)
        #print "parsed_datetime= ", parsed_datetime
    except ValueError:
        parsed_datetime = None
    return parsed_datetime
    
 
def process_all_input_files(myfiles, mydate, mytime, mystring):
    for myfile in myfiles:
        content = read_file (myfile)
        #print "ZZZZZZZZZZZ";
        result = process_file2(content, mydate, mytime, mystring)
        for line in result:
            print line



def get_all_input_files(mypath):
    files = [f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath, f)) and f.endswith(('.txt', '.txt.gz')))]

    return files

def validate_inputs(date_val, time_val):

	#add other validations here
	
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

    return date_val, time_val

def parse_inputs():

    parser = argparse.ArgumentParser("%prog")

    parser.add_argument("-p", "--path", dest="PATH", help="full path to the input files' dir", default="")
    parser.add_argument("-d", "--date", dest="DATE", help="Search date", required=True, default="")
    parser.add_argument("-t", "--time", dest="TIME", help="Search time", default=None)
    parser.add_argument("-s", "--string", dest="STRING", help="Search string", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", dest="VERBOSE", help="Verbose mode", default=False)

    args = parser.parse_args()
    return args

def main ():
    
    if args.VERBOSE:	
        print "args:", args

    # final_path = args.PATH
    # final_date = args.DATE
    # final_time = args.TIME
    if args.PATH:
        if not os.path.exists(args.PATH):
            print ("Path:[%s] does not exist. Check your input." % args.PATH)
            sys.exit(1)

    args.DATE, args.TIME = validate_inputs(args.DATE, args.TIME)
    # args.PATH = final_path
    # args.DATE = final_date
    # args.TIME = final_time
	
    inputfiles = get_all_input_files(args.PATH)
    #print "cccccccc"
    #print inputfiles
    process_all_input_files(inputfiles, args.DATE, args.TIME, args.STRING)
	


if __name__ == '__main__':
    #Use 2.7 version of python
    ver = (2, 7)
    if sys.version_info[:2] != ver:
        print("ERROR: Use Python Version: 2.7")
        sys.exit()

    args = parse_inputs()

    main()



