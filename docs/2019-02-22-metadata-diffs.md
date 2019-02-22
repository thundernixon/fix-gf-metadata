# Metadata differences

Running `gftools add-font` on the entire google/fonts collection results in changes to more than just subset metadata. In this document, I'll make notes of what other metadata has been affected, by looking at Git diffs.

## Script

make log of diffs

for family in dir:
    add family path to log
    git diff commitHash vs newCommitHash
    for line in diff:
        if line doesn't contain '+subsets: "latin-ext"':
            add line to log