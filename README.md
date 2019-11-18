# Nasa-Collage
An script for creating a collage from images on nasas database

## Components

1. get all thumbnail asset URLs related to a keyword or group of keywords
2. download all assets
    1. Find color composition of all assets
    2. store this color composition in a hash

3. Analyse picture that collage will be made from
4. put pictures in correct position

## Installation:
### Requirements
- Python 3 must be installed
- In theory this should work on both linux and windows, but it was developed on a linux machine
### Installing python dependencies:
run the following commands in the base project directory
`python3 -m pip install opencv-python`
`python3 -m pip install numpy`
`python3 -m pip install requests`
### Installing the project
`python3 -m pip install .`

### IF YOU ARE HAVING ISSUES INSTALLING THIS REACH OUT TO gfvandehei@gmail.com ###

## How to use:

### To download images on a keyword from nasa's Images API run:

 *python3 bin/imagedownloader.py*

On running this a series of prompts asking for a keyword to look for images with, and a directory to save images to
will appear.

### Notes
The keyword should be somewhat specific, as nasa's image API refuses to serve results to general
searches. For example "Mars" refuses to serve, and will respond with a message to be more specific, however, Mars Rover
works just fine.

directory should be something along the lines of /home/downloads/large_image_directory or ./downloaded_images

### To create a collage from images in a directory run:

*python3 bin/createcollage.py {image to make collage from} {directory where sub images are} {scale for main image recommended = 10}
 {size to resize each sub image recommended=50} {final collage filename} {ram limit recommended=5.0}*

On running this a series of prompts will ask for the directory where images are, the location of the main image,
the resolution scaling of the main image, the resolution scaling of each inner picture, and the output collages
name

### Notes

images directory should be something like "~/Downloads/images" or "./downloaded_images"

main image location should be something like "~/Downloads/examplepicture.jpg"

main image resolution scaling is the amount that the resolution of the original image will be divided for

larger values consume less RAM and take less time, while larger values will do the opposite. For example a 1000*1000
original image size gets 10 input as the scaling value, the image will be viewed as a 100*100 image where each pixel will
be replaced with a child image

inner picture resolution scaling is the size that each child picture will be converted to before insertion. A value of
50 will lead to each child picture having a width and height of 50.

To find the final resolution of the collage use this formula:
width_new = (width_original/main_scaling_value)*inner_picture_resolution_scaling
height_new = (width_original/main_scaling_value)*inner_picture_resolution_scaling

Finally the output collages name is what the collage will be saved as, for example if I wanted to make a collage named
"Output_Collage.jpg" i would input "Output_Collage.jpg"

## Other Points of interest
- This program has the potential to be fairly memory intensive, if you find running it is eating too much ram, increase the
main scaling value, and decrease the inner picture resolution scaling value
- The resulting pictures will always be B/W this is by design
- Any errors that occur while running the createcollage program likely result from an incorrectly input path for the
image or image-directory




