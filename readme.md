# RoboCar Tub Consolidation
## Usage
`python -u tubcon.py <TUB_PATH>`

`tubcon.py` takes a single argument: the path that contains the `tub*` directories holding [donkeycar](http://www.donkeycar.com/) recorded data.

```
$ ls -l ~/d2/data
total 52488
drwxr-xr-x 1 David 197121        0 Apr 23 13:30 tub_11_18-04-23/
drwxr-xr-x 1 David 197121        0 Apr 23 16:56 tub_16_18-04-23/
drwxr-xr-x 1 David 197121        0 Apr 23 13:18 tub_8_18-04-23/
drwxr-xr-x 1 David 197121        0 Apr 23 13:21 tub_9_18-04-23/

$ python -u tubcon.py ~/d2/data
Skipping files in [data] (doesn't start with 'tub')
Discovering files in [~/d2/data/tub_1_18-04-24]
Discovering files in [~/d2/data/tub_2_18-04-24]
Discovering files in [~/d2/data/tub_3_18-04-24]
Discovering files in [~/d2/data/tub_4_18-04-24]
Discovering files in [~/d2/data/tub_5_18-04-24]
Found [10536] records in the tubs
Creating meta.json
[ 100.00%][10536/10536] Processing [data\tub_5_18-04-24\record_3599.json]
...
```

An `out/` directory will be created in the current working directory containing every file from the `tub*` directories (prefixed with the tub name).  The contents of all the .json files will also be modified to point to the new name of the associated file(s).

Numbers within filenames will also be left padded with `0`'s to fix any processing issues that may result in sorting the filenames alphabetically.
