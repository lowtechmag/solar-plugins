# Dither plugin for Pelican

A plugin which creates dithered versions of all your images. To save on space and gain on cool. 

The dithering algorithm used is Bayer Ordered dithering. The default settings convert the images to six-tone greyscale but it is possible to configure one's own color palette. 

The plugin copies all images into a folder called dithers and replaces all image paths of the resulting html to show the dithered images.  

## dependencies & installation
depends on [Pillow](https://pillow.readthedocs.io), [hitherdither](https://github.com/hbldh/hitherdither) and [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

`pip install Pillow bs4 git+https://www.github.com/hbldh/hitherdither`

Set it up like other plugins: make sure to set `PLUGIN_PATH` and add `thumbnailer` to the `PLUGINS` list.

## configuration

* `IMAGE_PATH` Path where all images are located, defaults to `images`
* `DITHER_DIR` The subdirectory where all dithered versions of your images are stored, defaults to `dithers`
* `THRESHOLD` this essentially sets the contrast on the final image. Defaults to `[96, 96, 96]`, make sure it is a list of three numbers ranging from 0-255.
* `RESIZE_OUTPUT` Whether the dithered images should be resized. Defaults to `True`
* `MAX_SIZE`  Max size to resize to. Uses the largest value (width or height) and preserves aspect ratio. Defaults to `(800,800)` 
* `DITHER_PALETTE` What palette to use for dithering.  Needs a list of RGB tuples. Defaults to a six tone greyscale palette: `[(25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)]` See [hitherdither](https://github.com/hbldh/hitherdither) for more info.
