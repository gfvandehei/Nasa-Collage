from NasaImageProfiler.keywordsearch import NasaMediaSearch
import sys


log_directory = sys.argv[1]
keyword = sys.argv[2]

nm = NasaMediaSearch([keyword])
print(len(nm.found_collections))

# log all of these collections to a file
with open(log_directory+"/"+keyword+"_collections.txt", 'w') as file:
    for i in nm.found_collections:
        file.write(i+"\n")
