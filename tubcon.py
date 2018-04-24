import json
import os
import shutil
import re
import sys

outdir = 'out/'
PAD_FORMAT = '{:0>10}'
JSON_KEY = 'cam/image_array'

# NUMS_REGEX = re.compile('([0-9]+)')

def pad_num_beg(filename):
    num = ''
    for char in filename:
        if char.isdigit():
            num += char
        else:
            break

    return PAD_FORMAT.format(num) + filename[len(num):]

def pad_num_mid(filename):
    num = ''
    started = False
    for char in filename:
        if char.isdigit():
            num += char
            started = True
        elif started:
            break

    return filename.replace(num, PAD_FORMAT.format(num))

def contruct_filename(root, filename, pad_func):
    newfilename = pad_func(filename)
    newfile = outdir + os.path.sep + os.path.basename(root) + '.' + newfilename
    newfile = os.path.abspath(newfile)

    return newfile

def handle_meta(root, file):
    curfile = os.path.abspath(root + os.path.sep + file)
    shutil.copy(curfile, outdir + os.path.sep + file)

def handle_image(root, file):
    curfile = os.path.abspath(root + os.path.sep + file)
    newfile = contruct_filename(root, file, pad_num_beg)
    shutil.copy(curfile, newfile)

def handle_json(root, file):
    curfile = os.path.abspath(root + os.path.sep + file)
    newfile = contruct_filename(root, file, pad_num_mid)

    with open(curfile, 'rt') as f:
        contents = f.read()
    
    json_parsed = json.loads(contents)
    new_json_val = os.path.basename(root) + '.' + pad_num_beg(json_parsed[JSON_KEY])

    if new_json_val.startswith('.\\'):
        new_json_val = new_json_val[2:]

    json_parsed[JSON_KEY] = new_json_val

    with open(newfile, 'wt') as f:
        f.write(json.dumps(json_parsed))

def main():
    # Ensure the output directory exists
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Process all dirs that start with Tub
    indir = '.'
    if len(sys.argv) > 1:
        indir = sys.argv[1]

    for root, dirs, files in os.walk(indir):
        if not os.path.basename(root).startswith('tub'):
            print('Skipping [{}]'.format(root))
            continue

        print('\nProcessing Files in [{}]'.format(root))
        for file in files:
            if file == 'meta.json':
                handle_meta(root, file)

            elif file.endswith(".jpg"):
                handle_image(root, file)

            elif file.endswith('.json'):
                handle_json(root, file)

            # printing and flushing may slow down processing
            print('.', end='')
            sys.stdout.flush()

if __name__ == '__main__':
    main()