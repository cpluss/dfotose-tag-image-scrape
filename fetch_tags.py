#!/usr/bin/env python
import requests
import os
import shutil
import optparse

def download_image_to_directory(image_uuid, directory):
    save_path = os.path.join(directory, '%s.jpg' % image_uuid)

    res = requests.get('https://dfoto.se/v1/image/%s/fullsize' % image_uuid, stream=True)
    with open(save_path, 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)


def fetch_all_from_tag(tag, save_directory):
    req = requests.get('https://dfoto.se/v1/image/tags/%s/search' % tag)
    images = req.json()
    print('Found %d images, downloading ..' % len(images))

    current = 0
    for img in images:
        print('Processed [%d/%d]' % (current, len(images)), end="\r")
        download_image_to_directory(img[u'_id'], save_directory)
        current = current + 1

    print('All images processed.')


def main():
    parser = optparse.OptionParser(usage='usage: %prog [options] tag', version='%prog 1.0')
    parser.add_option("-d", "--directory", action="store", default="./results",
            dest="save_directory", help="directory to save images to")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('wrong number of arguments')

    tag = args[0]
    if not os.path.exists(options.save_directory):
        os.makedirs(options.save_directory)

    fetch_all_from_tag(tag, options.save_directory)


if __name__ == '__main__':
    main()
