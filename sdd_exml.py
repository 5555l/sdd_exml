# This will encrypt / decrypt SDD EXML / XML
# To use this you must provide one of --encrypt or --decrypt and the --file to process
# If an output file is not specified then it goes to stdout as an ascii string

from Crypto.Cipher import DES3
import sys
import getopt
import os

# This is the magic key
dkey = b"YmZwZlQrQ3V4dVltNTArWE9s"
key = DES3.adjust_key_parity(dkey)

# set the 3DES cipher and options
cipher = DES3.new(key, DES3.MODE_ECB)

# How to encrypt
def encrypt(sdd_xml,cipher):
    exml = cipher.encrypt(sdd_xml)
    return exml

# How to decrypt
def decrypt(exml,cipher):
    sdd_xml = cipher.decrypt(exml)
    return sdd_xml

enc = dec = False
sdd_file = out_file = None

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]

# set the command line options
short_options = "hno:eno:dno:f:o"
long_options = ["help", "encrypt=", "decrypt=", "file=", "output="]

help_text = ("\noptions:\n"
            "   -e / --encrypt...............  encrypt XML to EXML\n"
            "   -d / --decrypt...............  decrypt EXML to XML\n"
            "   -f / --file <filename>.......  file to encrypt or decrypt\n"
            "   -o / --output <filename>.....  file to write output to, if absent will write to stdout\n")

# test for command line options
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print(str(err))
    sys.exit(2)

# Evaluate given arguments
for current_argument, current_value in arguments:
    if current_argument in ("-h", "--help"):
        print(help_text)
        sys.exit(2)
    elif current_argument in ("-e", "--encrypt"):
        enc = True
    elif current_argument in ("-d", "--decrypt"):
        dec = True
    elif current_argument in ("-o", "--output"):
        out_file = current_value
    elif current_argument in ("-f", "--file"):
        sdd_file = current_value
        if os.path.isfile(sdd_file) == False:
            print('file not found at', sdd_file)
            sys.exit(2)

# Check we don't have conflicting options set
if enc == True and dec == True:
    print("Both encrypt and decrypt options are set, I've no idea what you want to do")
    print(help_text)
    sys.exit(2)

# Check we have a valid option set
if enc == False and dec == False:
    print("Neither encrypt nor decrypt options are set, I've no idea what you want to do")
    print(help_text)
    sys.exit(2)

# Check there is a file to process
if sdd_file == None:
    print("No file was provided")
    print(help_text)
    sys.exit(2)

# Looks like we have everything we need, lets crack on

# read in the file
file = open(sdd_file,"rb")
in_data = file.read()
file.close()

# If asked, lets go decrypt a file
if dec == True:
    out_data = decrypt(in_data,cipher)
# if asked, encrypt the file
elif enc == True:
    out_data = encrypt(in_data,cipher)

# If an output filename is given then write it to the file
if out_file != None:
    print('Writing to', out_file)
    # Lets get rid of any old files from previous runs
    if os.path.exists(out_file): os.remove(out_file)
    f = open(out_file, "wb")
    f.write(out_data)
    f.close()
else:
    # otherwise output to stdout
    print(out_data.decode('ascii'))
