# Purpose of Fork
Implement two features that could be seen in the branches. They have been submitted as pull requests in the original repo

## osu!cat
This is a python application that tracks the cursor position and key inputs to create a Bongo Cat window which can be used as an overlay for streaming/recording applications.
## [Latest version](https://github.com/ZeCryptic/osu-cat/releases/tag/v1.1.1)
* Greatly improved application performance and key tap logic (thanks CCpersonguy)
* Added an option for smaller application window
* Changed cat image resolution (from 757 x 753 to 640 x 640 )
* Fixed wrong version displayed
## Changing the cat images
It is entirely possible to edit the png files to make the cat look different (totally understandable, they look bad). However, when doing so you need to make sure that the new picture files have a color depth of 32 bits. Otherwise the program will not work. One way of doing this is by just re-saving the images in a program like paint.net and select the [32-bit color depth option](http://puu.sh/ByjvT/8023ae8252.png). I plan on fixing this bug in the future

