definition = """
// wordlist allowed for parameter's types

default                      #a simple parameter
boolean                      #can be true or false
text                         #free text

numeric                      #a numeric value
+ int                        #an integer
+ float                      #a float

file                         #a simple file
+ image                      #a simple graphic
+ + png                      #a png
+ + pdf                      #a pdf

+ track                       #a file describing genomic files
+ + txt                      #a text file
+ + bed                      #a bed file
+ + wig                      #a wig file

assembly                     #a list of assemblies
"""

FILE = 'file'

wordlist = {}
inclusions = {}

for line in definition.split('\n'):
    if not line.find('#') == -1:
        word, comment = line.split('#')
        word_stripped, comment = ''.join(c for c in word if c not in '+').strip(), comment.strip()
        wordlist[word_stripped] = comment
        if not word.count('+') > 0:                         # we have a root element
            parents = [word_stripped]
            count = 0

        else :
            c = word.count('+')
            if c > count :                                   # we have a deeper child element

                cur_parent = parents[-1]
                if not inclusions.has_key(cur_parent) : inclusions[cur_parent] = []
                inclusions[cur_parent].append(word_stripped)
                parents.append(word_stripped)
                count += 1

            elif c == count :                                 # we have a child for same previous parent
                if len(parents) > count : parents.pop()
                cur_parent = parents[-1]
                inclusions[cur_parent].append(word_stripped)
                parents.append(word_stripped)

            else :                                            # (c < count) we go back one step
                parents.pop()
                parents.pop()
                cur_parent = parents[-1]
                if not inclusions.has_key(cur_parent) : inclusions[cur_parent] = []
                inclusions[cur_parent].append(word_stripped)
                parents.append(word_stripped)
                count -= 1




def is_of_type(obj, oftype):
    if not inclusions.has_key(oftype) : return False
    types = inclusions.get(oftype)
    if obj in types : return True
    for ty in types :
        if is_of_type(word, ty) : return True
    return False

