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

    logFile.write("Git Diffs for fonts \n \n")

    logFile.write(str(dir))
    for subdir in os.walk(dir):  # might need OS walk
        metadata = subdir[0] + "/METADATA.pb"
        command = "git diff -- " + metadata
        print(command)
        try:
            gitDiff = subprocess.check_output(command, shell=True)

            if gitDiff is not b'':
                if str(subdir[0]) is not "ofl":
                    logFile.write(str(subdir[0]) + "\n")

                for line in gitDiff.split(b'\n'):
                    # logFile.write(str(line)[:3] + '\n')
                    lineStart = str(line)[:3]
                    if '+' in lineStart or '-' in lineStart:
                        if b'---' not in line and b'+++' not in line:
                            logFile.write(str(line).replace(
                                "b'", "'").replace("'\n", "\n") + "\n")
                logFile.write(
                    "----------------------------------\n")
        except subprocess.CalledProcessError:
            continue

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
