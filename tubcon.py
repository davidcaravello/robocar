import json
import os
import shutil
import sys

outdir = 'out/'
JSON_KEY = 'cam/image_array'

def get_tubs_to_process(indir):
    tubs = {}
    # Process all dirs that start with Tub
    for root, dirs, files in os.walk(indir):
        if not os.path.basename(root).startswith('tub'):
            print("Skipping files in [{}] (doesn't start with 'tub')".format(root))
            continue

        print('Discovering files in [{}]'.format(root))
        records = []
        for file in files:
            if file == 'meta.json':
                # Assumption, is a meta.json per tub, and they are all exactly the same
                continue

            elif file.endswith(".jpg"):
                # Will get jpg file details from json records
                continue

            elif file.endswith('.json'):
                with open(root + os.path.sep + file, 'rt') as f:
                    json_contents = json.loads(f.read())

                records.append((file, json_contents))
        
        tubs[root] = records

    return tubs
        
def consolidate(tubs, outdir):
    record_count = 0
    for tub_dir in tubs.keys():
        records = tubs[tub_dir]
        # This lambda will extract the digits from the record_####.json filename, and then sort the filenames
        # based on the int representation of the digits (as opposed to alphabetically)
        records.sort(key=lambda x: int(x[0][:-5].split('_')[1]))
        record_count += len(records)

    print('Found [{}] records in the tubs'.format(record_count))

    max_digits = len(str(record_count)) + 1
    record_filename_template = 'record_{:0>' + str(max_digits) + '}.json'
    image_filename_template = '{:0>' + str(max_digits) + '}_cam-image_array_.jpg'
    progress_template = '\r[{:>7.2f}%][{:>' + str(max_digits-1) + '}/{}] Processing [{}]       '

    record_index = 0
    for tub_dir in tubs.keys():
        # Lets create our meta file if it doesn't exist
        dst_metafile = os.path.join(outdir, 'meta.json')
        if not os.path.exists(dst_metafile):
            print('Creating meta.json')
            src_metafile = os.path.join(tub_dir, 'meta.json')
            shutil.copy(src_metafile, dst_metafile)

        records = tubs[tub_dir]
        # print('\nProcessing [{}] records in [{}] - beginning index [{}]'.format(len(records), tub_dir, record_index+1))

        for i, record in enumerate(records):
            record_index += 1

            record_filename = record[0]
            record_json = record[1]

            image_filename = record[1][JSON_KEY]

            new_record_filename = record_filename_template.format(record_index)
            new_image_filename = image_filename_template.format(record_index)

            record_json[JSON_KEY] = new_image_filename
            with open(outdir + os.path.sep + new_record_filename, 'wt') as f:
                f.write(json.dumps(record_json))

            src_img_filename = os.path.join(tub_dir, image_filename)
            dst_img_file = os.path.join(outdir, new_image_filename)
            shutil.copy(src_img_filename, dst_img_file)
            # print('[{}] -> [{}] and [{}] -> [{}]'.format(record_filename, new_record_filename, image_filename, new_image_filename))
            print(progress_template.format((record_index / record_count)*100, record_index, record_count, os.path.join(tub_dir, record_filename)), end='')
    
    print('\nFinished creating records in [{}]'.format(os.path.abspath(outdir)))

def main():
    # Ensure the output directory exists
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    indir = '.'
    if len(sys.argv) > 1:
        indir = sys.argv[1]

    tubs = get_tubs_to_process(indir)
    consolidate(tubs, outdir)

if __name__ == '__main__':
    main()