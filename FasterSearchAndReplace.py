
########################################################################################################################

def loop_on_directory(directory,find):
#Purpose: To loop on the given directory, and find a specific value in the directory (i.e. Universe or Ring)
#Arguments:
#   directory: directory to loop on
#   find: what to look for in the directory's path
    i = 0
    Z = []
    arr = []
    arr = os.listdir(directory)
    for X in arr:
        if find:
            if find in X:
                i += 1
                Z.append(X)
        else:
            i += 1
            Z.append(X)
    return Z

def ask_choice(arg):
#Purpose: To ask what your choice is, returns the chosen number minus 1
#Argument: What you want the user to choose    
    print()
    return int(input('What ' + arg + "? "))-1

########################################################################################################################

import os

#counters
total=0
i=0
numsrcs = 0

#arrays to hold
unv = []
rings = []
apps = []
sources = []

numunvs = []
numrings = []
numapps = []
counter=[]
sourcelist=[]

unvlist=[]
ringlist=[]
applist=[]

uniqueunv1=[]
uniquerings1=[]
uniqueapps1=[]
listOfPrograms=[]
results=[]

print(),print('Populating Statistics...'),print()

#get the list of universes to loop on later
unv = loop_on_directory('C:\ProgramData\MEDITECH','Universe')

search = input('Search for? ')

#this populates the lists of universes, apps, rings, and sources
#this should be updated to get the stuff we care about as opposed
#to everything
for X in unv:
    rings = loop_on_directory('C:\ProgramData\MEDITECH\\'+X,'Ring')
    for Y in rings:
        if os.path.isdir('C:\ProgramData\MEDITECH\\'+X+'\\'+Y+'\\!AllUsers\Sys\PgmCache\Ring\PgmSource'):
            apps = loop_on_directory('C:\ProgramData\MEDITECH\\'+X+'\\'+Y+'\\!AllUsers\Sys\PgmCache\Ring\PgmSource','')
        for Z in apps:
            if Z != '.svn':
                if os.path.isdir('C:\ProgramData\MEDITECH\\'+X+'\\'+Y+'\\!AllUsers\Sys\PgmCache\Ring\PgmSource\\'+Z):
                    sources = loop_on_directory('C:\ProgramData\MEDITECH\\'+X+'\\'+Y+'\\!AllUsers\Sys\PgmCache\Ring\PgmSource\\'+Z,'focus')
                    for source in sources:
                        unvlist.append(X)
                        applist.append(Z)
                        ringlist.append((X+'\\'+Y))
                        sourcelist.append((X+'\\'+Y+'\\'+Z+'\\'+source))
                        if source.startswith(Z):
                            numapps.append(Z)

#create dictionaries - this seems the fastest way
#to create a list of non-duplicates
uniqueunv=dict.fromkeys(unvlist)
uniquerings=dict.fromkeys(ringlist)
uniqueapps=dict.fromkeys(numapps)

# these create arrays so they can
# easily be numbered (i.e. uniquerings1[1]
# instead of using a dictionary that would
# be more complicated to do later on
for X in uniqueunv:
    uniqueunv1.append(X)

for X in uniquerings:
    uniquerings1.append(X)

for X in uniqueapps:
    uniqueapps1.append(X)

# all does not work yet
#   the programDirectory will need to be updated to search all apps
#   instead of the one chosen
print(1,"-","All") 
i=1
for X in uniqueapps1:
    i+=1
    print(i,"-",X)
appToSearch = uniqueapps1[ask_choice('application')-1]

i=0
for X in uniquerings1:
    i+=1
    print(i,"-",X)
ringToSearch = uniquerings1[ask_choice('ring')]    

print(search)
print(appToSearch)
print(ringToSearch)

programDirectory = ('C:\ProgramData\MEDITECH\\'+ringToSearch+'\!AllUsers\Sys\PgmCache\Ring\PgmSource\\'+appToSearch+'\\')
listOfPrograms = loop_on_directory(programDirectory,'')

print('\n*************\n')

resultsFile = open('C:\ProgramData\MEDITECH\SearchResults.txt','w')
resultsFile.write('=====================================================================\n')
resultsFile.write('Ring:\t\t'+ringToSearch+'\n')
resultsFile.write('Application:\t'+appToSearch+'\n')
resultsFile.write('Searching:\t'+search+'\n')
resultsFile.write('=====================================================================\n\n')

##
#loop on the list of programs in the directory
for program in listOfPrograms:
    if "UT.focus" not in program:
        # open the program to read each line
        programToRead = open((programDirectory+program), "r")
        # search for the line in the program by reading each line
        for line in programToRead:
            # case insensitive search (make search and line all uppercase)
            # maybe this can be an option? (case sensitive or not)
            if "//" not in line:
                if search.upper() in line.upper():
                    results.append([program,line.strip()])
                    printLine=(program+'\t\t\t\t'+line.strip())
                    print(printLine)
                    resultsFile.write(printLine+'\n')
        programToRead.close()
##
# for some reason, the program doesn't write to the file if it's not flushed before it's closed    
resultsFile.flush()
resultsFile.close()

# open the file in notepad to display the results
osCommandString = ('notepad.exe C:\ProgramData\MEDITECH\SearchResults.txt')
os.system(osCommandString)




