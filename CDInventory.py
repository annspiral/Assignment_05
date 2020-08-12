#------------------------------------------#
# Title: CDInventory.py
# Desc: Starter Script for Assignment 05
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AAllen, 2020-Aug-7, replace lists with
#                     dictionaries inside
#                     main list, lstTbl
# AAllen, 2020-Aug-7, added code to save to
#                     file
# AAllen, 2020-Aug-7, added loading from file
# AAllen, 2020-Aug-7, added second table list to 
#                     manage loaded and new data
#                     separately
# AAllen, 2020-Aug-9, removed deeply nested loops
#------------------------------------------#

# Declare variables

strChoice = '' # User input
lstTbl = []  # list of dicts to hold saved data
lstNewInv = [] # list of new dicts added by user since last save
dictRow = {}  # dictionary data row: ID, CD Title, Artist
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object

# Get user Input
print('The Magic CD Inventory\n')
while True:
    # 1. Display menu allowing the user to choose:
    print('[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
    print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit')
    strChoice = input('l, a, i, d, s or x: ').lower()  # convert choice to lower case at time of input
    print()

    if strChoice == 'x':
        # 5. Exit the program if the user chooses so
        break
    
    if strChoice == 'l':
        try:
            objFile = open(strFileName, 'r')
        except:
            print('Could not find file to load.\n')
            continue
        
            # if inventory file was loaded successfully
        if objFile != None and objFile == []:
            # check if file is empty for good user message
            print('Inventory File is empty.\n')
            # or proceed to load file contents into lstTbl
        elif objFile != None:
            # start with empty table in case user has already loaded
            lstTbl.clear()
            for fileRow in objFile:
                lstRow = fileRow.strip().split(sep=',')
                dictRow = {'id':int(lstRow[0]), 'CD Title':lstRow[1], \
                           'Artist':lstRow[2]}
                lstTbl.append(dictRow)
            print('Inventory loaded from file.\n')
        else:
            print("---- No CD Inventory has been saved yet.----\n")
        objFile.close()
    
    elif strChoice == 'a':  # no elif necessary, as this code is only reached if strChoice is not 'exit'
        # 2. Add data to the table (2d-list) each time the user wants to add data
        strID = input('Enter an ID: ')
        strTitle = input('Enter the CD\'s Title: ')
        strArtist = input('Enter the Artist\'s Name: ')
        intID = int(strID)
        dictRow = {'id':intID, 'CD Title':strTitle, 'Artist':strArtist}
        lstNewInv.append(dictRow)
        
    elif strChoice == 'i':
        # 3. Display the current data to the user each time the user wants to display the data
        
        # display header
        print('ID, CD Title, Artist')
        
        # display items from file if user has loaded them
        # if the CD Inventory is empty, confirm that to user
        if lstTbl == []:
            print('---- No CDs loaded from saved File Inventory ----\n')
        # for each row from the file, display the inventory
        for dictRow in lstTbl:
            # add error catching in case key names incorrect
            try:
                print(dictRow['id'], dictRow['CD Title'], dictRow['Artist'], \
                      sep=',', end='\n')
            except:
                print('! Error printing row from CD Inventory File !\n')
                
        # display items the user has added, but not saved in this session    
        # if new CD Inventory is empty, confirm that to user
        if lstNewInv == []:
            print('---- No new CDs added to New Inventory ----\n')
        for dictRow in lstNewInv:
            # add error catching in case key names incorrect
            try:
                print(dictRow['id'], dictRow['CD Title'], dictRow['Artist'], \
                      sep=',', end='\n')
            except:
                print('! Error printing row in new CD Inventory\n')
        print()
        
    elif strChoice == 'd':
        # ask user which CD ID they want to delete (or if they want to cancel)
        strDelCD = input('Which CD ID would you like to'+
                          ' delete? (enter x to cancel): ')
        
        # if user wants to cancel, return to menu
        if strDelCD.lower() == 'x':
            continue
        
        # or check for valid entry and find entry to delete
        try:
            intDelCD = int(strDelCD)
        # if user entry is not an integer, exit to menu
        except:
            print('Not a valid CD ID entry\n')
            continue
        
        # if user entered a number for CD ID
        if intDelCD:
            boolFound = False
            
            # Look in all the rows in the new list inventory first
            for row in lstNewInv:
                if row.get('id') == intDelCD:
                    lstNewInv.remove(row)
                    boolFound = True
                    print('CD entry with ID=', strDelCD, 'was deleted.\n')
                    continue
                
            # if ID row was removed, return to main menu
            if boolFound == True:
                continue

            # if CD ID has not been found, look in the loaded file table 
            # and delete from file
            for row in lstTbl:
                if row.get('id') == intDelCD:
                    lstTbl.remove(row)
                    boolFound = True
                    # replace file contents with new lstTbl
                    for dictRow in lstTbl:
                        strDictRow = ''
                        for key, value in dictRow.items():
                            strDictRow += str(value) + ','
                        # remove last , and add newline
                        strDictRow = strDictRow[:-1] + '\n'
                        objFile = open(strFileName, 'w')
                        objFile.write(strDictRow)
                        objFile.close()
          
                    print('CD entry with ID= ', strDelCD, ' was',
                          ' deleted from the file.\n')
                    continue
            if boolFound == True:
                continue
                
            # if ID was not found, code reaches here and shows
            # message that ID was not found
            print('Cound not find CD with ID= ', strDelCD,'.\n')
        
    elif strChoice == 's':
        # 4. Save the data to a text file CDInventory.txt if the user chooses so
        # if there is no new inventory, do not access file
        if lstNewInv == []:
            print('\n---- No new inventory to save.----\n')
            
        # open file and save new inventory if there are additions
        else:
            for dictRow in lstNewInv:
                strDictRow = ''
                for key, value in dictRow.items():
                    strDictRow += str(value) + ','
                # remove last , and add newline
                strDictRow = strDictRow[:-1] + '\n'
                objFile = open(strFileName, 'a')
                objFile.write(strDictRow)
                objFile.close()
            print('New inventory additions saved to file.\n')
            
            # add saved inventory to file inventory, user will expect this 
            #content for display option or delete option
            lstTbl += lstNewInv
            
            # reset new inventory to empty
            lstNewInv.clear()
    else:
        print('Please choose either l, a, i, d, s or x\n')