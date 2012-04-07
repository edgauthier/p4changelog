Overview
========

Prints out a changelog for the commits identified by the \<filespec\>. Date and
changelist filters are supported within the \<filespec\>.

Usage
=====

    Usage: p4cl.py [-f] <filespec>

    -f          Include files from the changelist in the changelog output. Only
                files that match the <filespec> will be output. The only
                exception is if the <filespec> includes *, ?, or ... (in the
                middle of the path - ... at the end of the path works as
                expected). 

    <filespec>  A Perforce filespec supporting date/changelist filters. 
                E.g. //depot/project/...@2,@10
                E.g. //depot/project/...@2012-04-01,@now
