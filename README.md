# SDD EXML / XML decoder / encoder
Decode and encode SDD EXML files.

(the hard work on getting the key was done here: https://github.com/smartgauges/exml)

It needs a `--file` to decode/encode and the operation you want to do (`--decrypt` / `--encrypt`).

## Arguments

| Argument | Description |
|:------|:------------|
|`-e` / `--encrypt`|encrypt XML to EXML|
|`-d` / `--decrypt` |decrypt EXML to XML|
|`-f` / `--file <filename>`|file to encrypt or decrypt|
|`-o` / `--output <filename>`|file to write output to, if absent will write to stdout in ascii|
