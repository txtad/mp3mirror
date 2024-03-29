# mp3mirror

FLAC and OGG to MP3 mirroring script.

## About

mp3mirror is a small collection of Python scripts I initially wrote as my 
first Python project around 2003. The need for it arose from my desire to rip
my entire 1,000 CD music collection into a high quality format, .ogg at the 
time, more lately .flac, while also having a moderate bit-rate .mp3 version of
each album as well for use on the memory constrained music players of the 
time. Now that there are music players with 160GB capcity or more, the need 
for the moderate bitrate version no longer exists, but I still find that it is
nice to have a .flac "master" copy and a more portable .mp3 version as well.

mp3mirror simply makes a recursive descent into the specified master 
repository, creating an mp3 copy in the mirror directory of each .ogg or .flac
file encountered in the master. The directory and filename structure of the 
master directory are maintained in the mirror.

## Current State of mp3mirror as of Late 2012

I am releasing mp3mirror as an open source project mostly as an exercise of
creating an open source project. The need for this project was very specific
to me and I'm not sure if anyone else has the same need. However, it is 
possible that someone does and if so, I hope they find it helpful. Its current
state is not very polished, as it was my first Python project and as soon as 
it was "good enough" I stopped working on it and moved on to other things.

### Current Shortcomings

* Lack of documentation.
* Lack of configurability and no configuration tool. Configuration requires
some programming skills.
* Miminal error handling.

### Planned Features

* Support mp3 master files.
* Some sort of configuration tool or at least configuration file.
* Multi-threaded generation.

## License

Copyright (C) 2003-2012 Tad Marko (tad@markoland.net)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
