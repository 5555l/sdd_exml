# This will encrypt / decrypt SDD EXML / XML
# To use this you must provide one of --encrypt or --decrypt and the --file to process
# If an output file is not specified then it goes to stdout as an ascii string

from Crypto.Cipher import DES3
import sys
import getopt
import os

# This is the magic key
cipher_key_binary = b"YmZwZlQrQ3V4dVltNTArWE9s"

# setup the 3DES cipher and options
cipher_3des_key = DES3.adjust_key_parity(cipher_key_binary)
des3_cipher = DES3.new(cipher_3des_key, DES3.MODE_ECB)

# How to encrypt
def encrypt(sdd_xml,des3_cipher):
    sdd_exml = des3_cipher.encrypt(sdd_xml)
    return sdd_exml

# How to decrypt
def decrypt(sdd_exml,des3_cipher):
    sdd_xml = des3_cipher.decrypt(sdd_exml)
    return sdd_xml

# set some defaults
encrypt_xml = decrypt_exml = False
sdd_input_file_name = output_file_name = None

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
        encrypt_xml = True
    elif current_argument in ("-d", "--decrypt"):
        decrypt_exml = True
    elif current_argument in ("-o", "--output"):
        output_file_name = current_value
    elif current_argument in ("-f", "--file"):
        sdd_input_file_name = current_value
        if os.path.isfile(sdd_input_file_name) == False:
            print('file not found at', sdd_input_file_name)
            sys.exit(2)

# Check we don't have conflicting options set
if encrypt_xml == True and decrypt_exml == True:
    print("Both encrypt and decrypt options are set, I've no idea what you want to do")
    print(help_text)
    sys.exit(2)

# Check we have at least one valid option set
if encrypt_xml == False and decrypt_exml == False:
    print("Neither encrypt nor decrypt options are set, I've no idea what you want to do")
    print(help_text)
    sys.exit(2)

# Check there is a file to process
if sdd_input_file_name == None:
    print("No file was provided")
    print(help_text)
    sys.exit(2)

# Looks like we have everything we need, lets crack on

# read in the file - must be read in as a binary file
input_file = open(sdd_input_file_name,"rb")
input_binary_data = input_file.read()
input_file.close()

# If asked, lets go decrypt a file
if decrypt_exml == True:
    data_to_output = decrypt(input_binary_data,des3_cipher)
# if asked, encrypt the file
elif encrypt_xml == True:
    data_to_output = encrypt(input_binary_data,des3_cipher)

# If an output filename is given then write it to the file
if output_file_name != None:
    print('Writing to', output_file_name)
    # Lets get rid of any old files from previous runs
    if os.path.exists(output_file_name): os.remove(output_file_name)
    # write it out - must be written out as a binary file
    output_file = open(output_file_name, "wb")
    output_file.write(data_to_output)
    output_file.close()
else:
    # otherwise output to stdout
    print(data_to_output.decode('ascii'))
