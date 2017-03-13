#!/usr/bin/python
# coding=UTF-8

# Searching and Downloading Google Images/Image Links

# This software is a modified version of: https://github.com/hardikvasa/google-images-download


import os
import time
import sys
import ssl
import urllib2


def download_html_page(url):
    # Downloading entire Web Document (Raw Page Content)

    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:  # If the Current Version of Python is 3.0 or above
        import urllib.request  # urllib library for Extracting web pages
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:  # If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except Exception as e:
            return "Page Not found"


def _find_next_image_link(google_img_html):
    # Finding 'Next Image' from the given raw page

    start_line = google_img_html.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = google_img_html.find('"class="rg_meta"')
        start_content = google_img_html.find('"ou"', start_line + 1)
        end_content = google_img_html.find(',"ow"', start_content + 1)
        content_raw = str(google_img_html[start_content + 6:end_content - 1])
        return content_raw, end_content


def google_images_links(html_page, max_items=100, extension_whitelist=None, extension_blacklist=None):
    # example: extension_whitelist = ['.jpg', '.jpeg', '.bmp', '.png']
    lower_whitelist = []
    if extension_whitelist is not None:
        for ext in extension_whitelist:
            lower_whitelist.append(ext.lower())

    lower_blacklist = []
    if extension_blacklist is not None:
        for ext in extension_blacklist:
            lower_blacklist.append(ext.lower())

    items = []
    i = 0
    while i < max_items:
        item, end_content = _find_next_image_link(html_page)
        html_page = html_page[end_content:]  # html - iteration
        if item == "no_links":
            break
        else:
            extension = os.path.splitext(item)[1]
            if (extension_whitelist is not None and extension.lower() not in lower_whitelist) or \
                    (extension_blacklist is not None and extension.lower() in lower_blacklist):
                pass  # excluded image, repeat te cycle i (i not incremented).
            else:
                items.append(item)  # Append all the links in the list named 'Links'
                # time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
                i += 1
    return items



def google_image_download(search_keyword=u'cat',

                          max_download_per_keyword=100,
                          extension_whitelist=None,
                          extension_blacklist=None,
                          replace_extension_not_in_whitelist='.jpg',

                          download_img_path="",
                          image_file_prefix='google_',
                          image_file_postfix="_",
                          links_file_output=None,

                          verbose=True,
                          ignore_errors=False,
                          if_error_download_another=True,
                          image_download_timeout=7,
                          link_download_retry=3,
                          link_download_retry_sleep=0.5):
    """

    :param search_keyword: string or list of queries for google image search (don't worry about spaces in keyword).

    :param max_download_per_keyword: limit of image to download. NB: max is 100 because downloaded html contains 100
                                    images.

    :param extension_whitelist: If an image has not one of the whitelist extension, the image will be saved with the
                                extension given by 'replace_extension_not_in_whitelist' parameter.
                                If 'replace_extension_not_in_whitelist' is None, than these images will not be saved.

    :param extension_blacklist: If an image has one of the blacklist extension, the image will not be saved.

    :param replace_extension_not_in_whitelist: all images with extension not in whitelist will be saved with this extension.
                                               Use None if you want to skip images with extensions not in whitelist.

    :param links_file_output: specify the output file for the download links. Use none value if you don't want to
                            output this file.

    :param download_img_path: specify the path where to save the images. If not specified save in current directory.
    :param image_file_prefix: prepend this prefix to downloaded image files.
    :param verbose: output on terminal (true or false)
    :param ignore_errors: don't print errors in terminal.
    :param if_error_download_another: always get 100 links for each query and then try to download max_download_per_keyword images.
                                    If an error occurs, simply download another image (obiously with a limit of 100 links, i.e.
    :return: list of links fetched.
    """
    t0 = time.time()

    if isinstance(search_keyword, str):
        search_keyword = search_keyword.decode('utf-8')
    if isinstance(search_keyword, unicode):
        search_keyword = [search_keyword]


    if links_file_output is not None:
        if os.path.exists(links_file_output):
            os.remove(links_file_output)

    if replace_extension_not_in_whitelist is None:
        filter_whitelist = extension_whitelist
    else:
        filter_whitelist = None

    i = 0
    total_img_links = []
    for sk in search_keyword:

        if verbose:
            print(u"Download using keyword: " + sk)

        if verbose:
            iteration = u"Item no.: " + unicode(i) + u" -->" + u" Item name = " + sk
            print (iteration)
            print ("Evaluating...")
        #search = sk.replace(' ', '%20')
        #search = iriToUri(sk)
        search = urllib2.quote(sk.encode('utf-8'))
        url = u'https://www.google.com/search?q=' + search \
              + u'&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

        query_img_links = []
        retry = 0
        while len(query_img_links) == 0:
            raw_html = download_html_page(url)
            max_items = max_download_per_keyword
            if if_error_download_another:
                max_items = 100

                query_img_links = google_images_links(raw_html, max_items=max_items,
                                             extension_whitelist=filter_whitelist, extension_blacklist=extension_blacklist)
            if len(query_img_links) == 0:
                time.sleep(link_download_retry_sleep)
                retry += 1
                if retry > link_download_retry:
                    break

        total_img_links += query_img_links

    if verbose:
        # print ("Image Links = "+str(items))
        print ("Total Image Links = " + str(len(total_img_links)))
        print ("\n")

        if links_file_output is not None:
            info = open(links_file_output, 'a')
            info.write(str(i) + ': ' + sk + ": " + str(total_img_links) + "\n\n\n")
            info.close()
        i += 1

    if verbose:
        t1 = time.time()
        total_time = t1 - t0
        print("Total time taken: " + str(total_time) + " Seconds")
        print ("Starting Download...")

    if download_img_path != "" and not os.path.isdir(download_img_path):
        os.mkdir(download_img_path)

    k = 0
    error_count = 0
    while k < len(total_img_links) and k-error_count < max_download_per_keyword:
        from urllib2 import Request, urlopen
        from urllib2 import URLError, HTTPError

        error = False
        try:
            req = Request(total_img_links[k], headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})

            response = urlopen(req, timeout=image_download_timeout)
            data = response.read()
            response.close()

            extension = os.path.splitext(total_img_links[k])[1].lower()
            if extension is None:
                extension = ""
            if replace_extension_not_in_whitelist and \
                    (extension_whitelist is None or extension not in extension_whitelist):
                extension = replace_extension_not_in_whitelist

            output_file = open(os.path.join(download_img_path, image_file_prefix + image_file_postfix + str(k-error_count)
                                            + extension), 'wb')

            output_file.write(data)
            output_file.close()
            if verbose:
                print("completed ====> " + str(k-error_count))

        # IN this saving process we are just skipping the URL if there is any error
        except IOError as e:  # If there is any IOError
            error = True
            if not ignore_errors:
                print("IOError on image: {}".format(k-error_count))

        except HTTPError as e:  # If there is any HTTPError
            error = True
            if not ignore_errors:
                print("HTTPError '{}'  on image: {}".format(e.message, k-error_count))
        except ssl.CertificateError as e:
            error = True
            if not ignore_errors:
                print("ssl.CertificateError '{}'  on image: {}".format(e.message, k-error_count))
        except URLError as e:
            error = True
            if not ignore_errors:
                print("URLError '{}' on image: {}".format(e.message, k-error_count))

        except Exception as e:
            error = True
            if not ignore_errors:
                print("Unknown Exception '{}' on image: {}".format(e.message, k-error_count))

        if error:
            error_count += 1
            if if_error_download_another:
                print("Trying another image.")

        k += 1

    if verbose:
        print("\n")
        print("All are downloaded")
    if verbose or not ignore_errors:
        print("\n" + str(error_count) + " ----> total Errors")

    return total_img_links


import re, urlparse
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)



# USE urllib2.quote instead
# def iriToUri(iri):
#     parts= urlparse.urlparse(iri)
#     return urlparse.urlunparse(
#         part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
#         for parti, part in enumerate(parts)
#     )

# Example of usage (white and black list):

# Download all images with the same extension found on the web:
# google_image_search("cat", 20,
#                     extension_whitelist=None,
#                     replace_extension_not_in_whitelist=None,
#                     extension_blacklist=None)
#
# Download all images and replace all extension with .jpg:
# google_image_search("cat", 20,
#                     extension_whitelist=['.jpg'],
#                     replace_extension_not_in_whitelist='.jpg',
#                     extension_blacklist=None)
#
#
# # Download all images not having .svg and .png extension, and replace all downloaded file's extension with .jpg:
# google_image_search("cat", 20,
#                     extension_whitelist=['.jpg'],
#                     replace_extension_not_in_whitelist='.jpg',
#                     extension_blacklist=['.svg', '.png'])
#
# # Download all images that doesn't have .svg or .png extension, also skip the files without extensions.
# # Keep the original extensions for other downloaded images:
# google_image_search("cat", 20,
#                     extension_whitelist=None,
#                     replace_extension_not_in_whitelist=None,
#                     extension_blacklist=['.svg', '.png', ''])
#
#
# Download only the images with .jpg or .jpeg extensions:
# google_image_search("cat", 20,
#                     extension_whitelist=['.jpg', '.jpeg'],
#                     replace_extension_not_in_whitelist=None,
#                     extension_blacklist=None)
#
#
# Also works with UTF-8 characters:
# google_image_search("perché", 20,
#                     extension_whitelist=['.jpg', '.jpeg'],
#                     # replace_extension_not_in_whitelist='_UNKNOWN.jpg',
#                     replace_extension_not_in_whitelist=None,
#                     extension_blacklist=[ '.png', '.gif', '.svg'],
#                     download_img_path='./downloaded_images', image_file_prefix='google_downloaded_', )
