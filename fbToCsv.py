from facebookDataConverter import FacebookPostDataConverter

import os
import sys

# Query for Graph API
# me/posts?limit=5000&fields=message,story,created_time,reactions.limit(1000)

def run(argument):
    print('Script Start.')

    converter = FacebookPostDataConverter(argument)

    files = converter.convertToCsv()

    if files:
        for f in files:
            print('[SUCCESS] Data has been saved to: ' + str(f))
    else:
        print('[UNEXPECTED ERROR] Something might have go wrong.')

def validate_arguments():
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
        return arg # Just return the arg if it exists
        #if os.path.isfile(arg):
        #    return arg
        #else:
        #    print('[Error] The file "{}" does not exist!'.format(arg))
    else:
        print('[Error] 1 Argument is missing. You must give the path of the file containing the Facebook data.')
    
    return None

if __name__ == '__main__':
    argument = validate_arguments()
    
    if argument:
        run(argument)