#!/usr/bin/env python

import sys
import p4lib
import getopt

def changeHeader(details):
    summary = changeSummary(details['description'])
    return "[%s|CL:%s (%s)] - %s" % (details['date'], details['change'], details['user'], summary) 

def changeSummary(description):
    summary = description
    if '\n' in description:
        summary = description.split('\n')[0]
    return summary

def changedFileList(files, fileFilters = []):
    fileList = ""
    filePaths = [f['depotFile'] for f in files]
    fileList = ["    %s" % f for f in filePaths if fileMatchesFilter(f,fileFilters)]
    return '\n'.join(fileList)

def fileMatchesFilter(f,fileFilters):
    for fileFilter in fileFilters:
        # not sure how to handle these globs - assume all files match
        if '*' in fileFilter: return True
        if '?' in fileFilter: return True

        # get rid of any range (date/changelist) specifiers
        if '@' in fileFilter:
            fileFilter = fileFilter.split('@')[0]

        # if the ... wildard is found anywhere but the end, assume all files
        # match
        if fileFilter.find('...') != len(fileFilter) - 3: return True

        # if it ends in a directory wildcard, it's a match if f starts with the
        # filter (minus the ...)
        if fileFilter[-3:] == '...':
            if f.find(fileFilter[:-3]) == 0: return True
        else:
            # must be a specific file, which means an exact match
            if f == fileFilter: return True

    return False

def _usage():
    print """
    Usage: p4cl.py [-f] <filespec>

    -f          Include files from the changelist in the changelog output. Only
                files that match the <filespec> will be output. The only
                exception is if the <filespec> includes *, ?, or ... (in the
                middle of the path - ... at the end of the path works as
                expected). 

    <filespec>  A Perforce filespec supporting date/changelist filters. 
                E.g. //depot/project/...@2,@10
                E.g. //depot/project/...@2012-04-01,@now

    """

def main():
    includeFiles = False

    try:
        opts, fileFilters = getopt.getopt(sys.argv[1:], 'f')
    except getopt.GetoptError, e:
        print str(e)
        _usage()
        sys.exit(2)

    for o,v in opts:
        if o in ('-f'):
            includeFiles = True

    if len(fileFilters) == 0:
        _usage()
        sys.exit(2)

    p4 = p4lib.P4()
    changes = p4.changes(files=fileFilters)
    changeNums = [c['change'] for c in changes]

    for change in changeNums:
        details = p4.describe(change=change, shortForm=True)
        print changeHeader(details)
        if includeFiles:
            print changedFileList(details['files'], fileFilters)
            print ""

if __name__ == '__main__':
    main()
