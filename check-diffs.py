#!/usr/bin/env python

"""
Use to check git diffs across the METADATA.pb file of one or more font families at once.

Usage: Go into google/fonts directory, then run:

check-diffs --dir <directory_of_font_dirs>

"""

import os
import argparse
import subprocess


def check_diffs(dir):

    # make log file with current date
    logFile = open(f"git-diffs-{str(dir)}.txt", "w+")

    logFile.write(
        f"Git Diffs for fonts in google/fonts/{str(dir)} directory after re-running gftools add-font \n \n")

    for path, dirs, files in os.walk(dir):

        for dirname in sorted(dirs):
            metadata = str(dir) + "/" + dirname + "/METADATA.pb"
            command = "git diff -- " + metadata
            print(command)
            try:
                gitDiff = subprocess.check_output(command, shell=True)

                if gitDiff is not b'':
                    if str(dirname) is not str(dir):
                        logFile.write(str(dirname) + "\n")

                    for line in gitDiff.split(b'\n'):
                        # logFile.write(str(line)[:3] + '\n')
                        lineStart = str(line)[:3]
                        if '+' in lineStart or '-' in lineStart:
                            if b'---' not in line and b'+++' not in line:
                                logFile.write('    ' + str(line).replace(
                                    "b'", "'").replace("'\n", "\n") + "\n")
                    logFile.write(
                        "----------------------------------\n")
            except subprocess.CalledProcessError:
                continue

    logFile.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True)
    args = parser.parse_args()
    check_diffs(args.dir)

    # # you could easily add specific commit hashes, if you want to
    # parser.add_argument("--commits", nargs="2", required=False)
    # args = parser.parse_args()
    # if args.commits[0] is not None:
    #     check_diffs(args.dir, args.commits[0], args.commits[1])
    # else:
    #     check_diffs(args.dir)


if __name__ == "__main__":
    main()
