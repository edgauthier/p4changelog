#!/usr/bin/env python

import sys
import p4lib

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

        # if the ... wildard is found anywhere but the end, assume all files
        # match
        if fileFilter.find('...') != len(fileFilter) - 3: return True

        # get rid of any range (date/changelist) specifiers
        if '@' in fileFilter:
            fileFilter = fileFilter.split('@')[0]

        # if it ends in a directory wildcard, it's a match if f starts with the
        # filter (minus the ...)
        if fileFilter[-3:] == '...':
            if f.find(fileFilter[:-3]) == 0: return True
        else:
            # must be a specific file, which means an exact match
            if f == fileFilter: return True

    return False

def main():
    includeFiles = False
    if sys.argv[1] == '-f':
        includeFiles = True
        fileFilters = sys.argv[2:]
    else:
        fileFilters = sys.argv[1:]

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