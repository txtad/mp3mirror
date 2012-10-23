#!/usr/bin/python -O
#
# 

import os
import sys
import re
import tempfile
import stat
import musicfile
import subprocess
import posix
import ansi

# This is where all of your high quality music master files live.
MUSICDIR = '/net/nas/c/flac/'

# This is where they will all be replicated as moderate bitrate MP3
# files suitable for portable devices.
MP3MIRROR = '/net/nas/c/mp3/'

# Niceness to run the file encoding parts of this process under. This
# is very CPU intensive stuff and without nice, the machine will be
# noticeably slow for interactive use.
NICE_LEVEL = 0

reOGG     = re.compile('\.ogg$')
reFLAC    = re.compile('\.flac$')
reRIP     = re.compile('^' + MUSICDIR + 'rip')
reMP3Root = re.compile('^' + MP3MIRROR)

def fileExists(file):
    """Simply returns true of the specified file exists"""
    return os.access(file, os.F_OK)

def whichIsNewer(file1, file2):

    """
    Determines which file is newer. Both files must exist.

    Return of 0, files are same age.
    Return of -1, file1 is newer than file2.
    Return of 1, file2 is newer than file1.
    """
   
    rc = 0
    
    f1stats = os.stat(file1)
    f2stats = os.stat(file2)

    if f1stats[stat.ST_MTIME] > f2stats[stat.ST_MTIME]:
        rc = -1
    elif f1stats[stat.ST_MTIME] < f2stats[stat.ST_MTIME]:
        rc = 1
    return rc
        
def makeMP3Mirror(master, mirror):

    """Called once by main. This pretty much IS main."""
    
    print 'Examining music archive for new files'
    print 'Master music files in        %s%s%s' % (ansi.GREEN, MUSICDIR, ansi.NORM)
    print 'will be replicated as MP3 in %s%s%s' % (ansi.GREEN, MP3MIRROR, ansi.NORM)

    created = 0
    updated = 0
    filecount = 0
    queue = []

    try:
        for root, dirs, files in os.walk(master):
        
            if reRIP.search(root) != None:
                continue

            currentMirrorDir = root.replace(MUSICDIR, MP3MIRROR)
            files.sort()

            # Walk the entire directory tree looking for files that
            # exist in the master archive but are either nonexistant
            # or out of date in the mirror. They will be created or
            # updated as necessary.
            
            for file in files:
                filecount += 1
                if filecount % 5 == 0:
                    os.write(0, '%s%s files checked%s' % (ansi.SAVE_CURSOR, filecount, ansi.UNSAVE_CURSOR))
                
                fqmasterfile = "%s/%s" % (root, file)

                # Sorry, Python doesn't have a switch statement and below
                # is the recommended Pythonic idiom.
                try:
                    mp3file = {
                        'ogg' : lambda: reOGG.sub('.mp3', file),
                        'flac': lambda: reFLAC.sub('.mp3', file)}[findFileType(file)]()
                except KeyError:
                    print "%sUnknown file type for: %s%s%s" % (ansi.RED, ansi.BLUE, fqmasterfile, ansi.NORM)
                    continue
            
                fqmp3file = "%s/%s" % (currentMirrorDir, mp3file)
                
                needMakeMP3 = False
                
                if fileExists(fqmp3file) == False:
                    print "%s %sdoes not exist%s" %  (reMP3Root.sub('/.../', fqmp3file), ansi.RED, ansi.NORM)
                    completestr = 'created'
                    created += 1
                    needMakeMP3 = True
                elif whichIsNewer(fqmasterfile, fqmp3file) != 1:
                    print '%s %sexists, but is out of date%s' % (reMP3Root.sub('/.../', fqmp3file), ansi.YELLOW, ansi.NORM)
                    completestr = 'updated'
                    updated += 1
                    needMakeMP3 = True
                    
                if needMakeMP3:
                    # Queue the file creation information.
                    sys.stdout.flush()
                    queue.append((fqmasterfile, fqmp3file, currentMirrorDir, completestr))

        if len(queue):
            # build any files that need creating or updating.
            
            cword = ''
            if len(queue) != 1:
                cword = 'files need'
            else:
                cword = 'file needs'
                
            print "\n%s MP3 %s to be created or updated:" % (len(queue), cword)
            while len(queue):
                (fqmasterfile, fqmp3file, currentMirrorDir, workType) = queue.pop(0)
                print '%s: %s...' % (len(queue) + 1, reMP3Root.sub('/.../', fqmp3file)),
                sys.stdout.flush()
                makeMP3(fqmasterfile, fqmp3file, currentMirrorDir)
                print '%s' % workType
                        
    finally:
        print 'Done updating mirror'
        
        cword = 'file'
        if created != 1:
            cword += 's'

        uword = 'file'
        if updated != 1:
            uword += 's'
            
        print '\n%s files checked, %s %s created, %s %s updated.' % (filecount, created, cword, updated, uword)


def findFileType(file):
    
    """Returns a short string representing the file type of the    
    specified file. If the file type is unknown, None is returned."""
    
    if reOGG.search(file) != None:
        filetype = 'ogg'        
    elif reFLAC.search(file) != None:
        filetype = 'flac'
    else:
        filetype = None
            
    return filetype
    
    
def makeMP3(masterfile, mp3file, currentMirrorDir):

    """
    Builds the MP3 file"mp3file" in "currentMirrorDir" from the
    master file "masterfile".
    """
    
    if fileExists(currentMirrorDir) == False:
        os.makedirs(currentMirrorDir)

    # Using tempfile.mkstemp() because it is newer and better (well,
    # it's not deprecated).
    (tmpWAVfd, tmpWAV) = tempfile.mkstemp('.wav')

    # Create the temporary MP3 file in the destination directory to
    # save any copying time.
    (tmpMP3fd, tmpMP3) = tempfile.mkstemp('.mp3', '', currentMirrorDir)

    # But, only the file name is needed, not an open file with a
    # descriptor. Using mkstemp creates the file in the file system
    # for us, making thing theoretically safer, even if we are closing
    # the file descriptor created.
    os.close(tmpWAVfd)
    os.close(tmpMP3fd)

    filetype = findFileType(masterfile)
    if (filetype == 'ogg'):
        tags = musicfile.getOGGTags(masterfile)
    else:
        tags = musicfile.getFLACTags(masterfile)
        
    # the filehandling parts of this process are very CPU heavy. Up
    # the nice level to make the machine bearable.
    posix.nice(NICE_LEVEL)
    
    try:
        if filetype == 'flac':
            tags = musicfile.getFLACTags(masterfile)
            rc = subprocess.call(['flac',
                                  '--silent',
                                  '-f',
                                  '-d', '%s' % masterfile,
                                  '-o', '%s' % tmpWAV],
                                 stdout = open('/dev/null', 'w'))
            if (rc != 0):
                raise Exception, 'Could not create WAV file from FLAC file'
        
        if filetype == 'ogg':
            tags = musicfile.getOGGTags(masterfile)
            rc = subprocess.call(['oggdec',
                                  '--quiet',
                                  '%s' % masterfile,
                                  '-o', '%s' % tmpWAV],
                                 stdout = open('/dev/null', 'w'))
            if (rc != 0):
                raise Exception, 'Could not create WAV file from OGG file'

        rc = subprocess.call(['lame',
                              '--quiet',
                              '--tt', '%s' % tags['title'],
                              '--ta', '%s' % tags['artist'],
                              '--tg', '%s' % tags['genre'],
                              '--ty', '%s' % tags['date'],
                              '--tl', '%s' % tags['album'],
                              '--tn', '%s' % tags['track'],
                              '-V7',
                              '--vbr-new',
                              '-q2',
                              '-b56',
                              '-B112',
                              '--lowpass', '15.4',
                              '--athaa-sensitivity', '1',
                              tmpWAV,
                              tmpMP3],
                             stdout = open('/dev/null', 'w'))
        if (rc != 0):
            raise Exception, 'Could not create MP3 file'

        # Copy the newly created MP3 to it's final name.
        os.rename(tmpMP3, mp3file)

        os.chmod(mp3file, 0644)

        # And delete the intermediate file.
        if fileExists(tmpWAV):
            os.unlink(tmpWAV)
            tmpWAV = None

    finally:
        # On the way out, delete any undeleted temporary wav files and
        # unfinished mp3 files. When these files are processed
        # normally, mp3file and wavfile are set to None. If they have
        # values, it can be assumed they haven't been handled
        # properly.
        
        if tmpWAV != None and os.path.isfile(tmpWAV):
            print 'Attempting to delete lingering WAV file %s' % (tmpWAV)
            unlinkNoError(tmpWAV)
                
        if tmpMP3 != None and os.path.isfile(tmpMP3):
            print 'Attempting to delete incomplete MP3 file %s' % (tmpMP3)
            unlinkNoError(tmpMP3)

        posix.nice(0)
        

def unlinkNoError(filename):
    try:
        os.unlink(filename)
    except os.error:
        pass
        
                
def domain():
    try:
        makeMP3Mirror(MUSICDIR, MP3MIRROR)
    except KeyboardInterrupt:
        print "Control-C"



def main():
    print os.umask(022)
    domain()

if __name__ == '__main__':
    sys.exit(main())
