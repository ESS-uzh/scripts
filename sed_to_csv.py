"""
This script takes a source directory with the .sed and generate relative
csv files in an 'out_csv' directory

NOTE: The first 26 lines of the .sed file contain metadata information
about the measuremnt. This information are stripped out in the csv file.
To see the metadata just open the relative .sed file with a text editor.

USAGE:

e.g. python3 sed_to_csv.py --path /home/diego/work/dev/SpecraEvol/2020_Jul_01

"""

import os
import argparse
import glob
import pandas as pd
import sys


def collect_files(datadir):
    sedF = sorted([f for f in glob.glob(os.path.join(datadir, "*.sed"))])
    if not sedF:
        print(f"No .sed files found at {datadir}")
        return
    print(f"Found {len(sedF)} files to convert")
    return sedF

def sed_to_csv(filepath, outdir):
	file = os.path.basename(filepath)
	filename = os.path.splitext(file)[0]
	df = pd.read_csv(filepath, delimiter="\t", skiprows=26)
	df.columns = ["Wvl", "Reflect. %"]
	df.to_csv(os.path.join(outdir, filename+".csv"))

def cli():
    parser = argparse.ArgumentParser(
        description="Convert sed files from SpectraEvolution to csv"
    )
    parser.add_argument("--path", required=True)

    return parser

def main():
    parser = cli()
    args = parser.parse_args()
    sourcedir = args.path

    # check whether sourcedir exist 
    if not os.path.isdir(sourcedir):
         print("Source directory was not found")
         sys.exit()

    outdir = os.path.join(sourcedir, "out_csv")
    if not os.path.isdir(outdir):   
	    os.mkdir(outdir)
    
    files = collect_files(sourcedir)
    for filepath in files:
        sed_to_csv(filepath, outdir)
    print("done")

if __name__ == "__main__":
	main()
    


	


