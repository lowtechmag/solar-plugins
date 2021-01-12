#Page Meta-Data

A Pelican plugin to add the total page size to each generated page of your site.

It calculates the weight of the HTML page including all image media and returns that in a human readable format (B, KB, MB).

## Caveats:
it currently is tailored to https://solar.lowtechmagazine.com and needs work in the following areas:

* add options to show file name and generation time
* properly handle subsites plugin (currently it only works for dither+subsites)
* make sure it works with --relative-urls flag
* handle static assets


## Use:
To enable the plugin add it to the `PLUGINS` list in `pelicanconf.py`.

Add a div with id `page-size` to your template and `page_metadata` will place the result there.

have fun!


## in case we add generation time:

To use this plugin first import `strftime` at the top of `pelicanconf.py`:

`from time import strftime`

Then add `NOW = strftime('%c')` somewhere in that document as well. This saves the time of generation as a variable that is usable by the `page_metadata` plugin. 


