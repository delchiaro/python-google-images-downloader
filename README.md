# Python Google Images Downloader
Python functions for 'searching' and 'downloading' Google images/image links.<br />
Download and process the standard html page of google images.<br />
This software is a modification of the original software: https://github.com/hardikvasa/google-images-download
## Summary
This is a Python program to search keywords/key-phrases on Google Images and then also optionally download all Images. 

## Compatability
Tested only on python 2.7

## Limitations
Can download max 100 images per query (html page retrived contains 100 images/links).

## Usage
```python
google_image_search(search_keyword='cat',               # string or list of strings
                    max_download_per_keyword=100,      
                    extension_whitelist=None,           # whitelist for file extensions
                    extension_blacklist=None,           # blacklist for file extensions
                    replace_extension_not_in_whitelist='.jpg', # whitelist behaviour

                    download_img_path="",               # where to download images 
                    image_file_prefix='google_',        # prefix for downloaded image names
                    links_file_output='gdownlinks.txt', # file with image links

                    verbose=True,
                    ignore_errors=False)
```

## Disclaimer
This program lets you download tons of images from Google. Please do not download any image without violating its copyright terms. Google Images is a search engine that merely indexes images and allows you to find them.  It does NOT produce its own images and, as such, it doesn't own copyright on any of them.  The original creators of the images own the copyrights.  
