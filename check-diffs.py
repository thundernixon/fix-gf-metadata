#!/usr/bin/env python

"""
Use to check git diffs across the METADATA.pb file of one or more font families at once.

Usage:

check-diffs --dir <directory_of_font_dirs>

"""

import os
import argparse
import subprocess


# add to log: compared git hashes

# def check_diffs(dir, *commits):


def check_diffs(dir):

    # make log file with current date
    logFile = open("git-diffs.txt", "w+")

    logFile.write("hello \n")

    logFile.write(str(dir))
    for subdir in os.walk(dir):  # might need OS walk
        #     gitDiff = subprocess.check()
        logFile.write("\n")

        gitDiff = subprocess.check_output(
            ["git diff", str(subdir[0])], shell=True)
        logFile.write(str(subdir[0]) + "\n")
        logFile.write(str(gitDiff))

    logFile.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True)
    # parser.add_argument("--commits", nargs="2", required=False)
    args = parser.parse_args()

    # if args.commits[0] is not None:
    #     check_diffs(args.dir, args.commits[0], args.commits[1])
    # else:
    #     check_diffs(args.dir)

    check_diffs(args.dir)


if __name__ == "__main__":
    main()
