#Importing Packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import shutil
import time

#establishing Variables
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","#"] #list of letters to cycle through
tableCount = 1 #var for counting each game in a table in the vimms vault
downloading = True
loading = True #var for waiting until a file is downloaded or a site is loaded
forcedLetter = False
gameSearch = False #var for starting a download at the most recently downloaded game

#get user input to choose what consoles are to be downloaded
print("Choose console game library to download:\nNES\nSMS\nGenesis\nSNES\nSaturn\nPS1\nN64\nDreamcast\nPS2\nXbox\nGameCube\nXbox360\nPS3\nWii\nWiiWare\nGB\nVB\nGBC\nGBA\nDS\nPSP\n\nTo select multiple consoles add a ',' then another console (eg. NES,SNES,Genesis)")
input = input("") #gets user input

#puts each console selected into a list
if "," in input:

    consoles = input.split(",") #split the selected consoles into a list
    print(consoles) #print the selected consoles

else:

    consoles = [input] #put the one selected console into a list
    print(consoles) #print the selected console

#loop for downloading each game for each console in each letter
for items in consoles: #loops for each console selected

    #establishes a web connection
    driver = webdriver.Chrome() #create a google chrome webdriver
    driver.get("about:blank") #open chrome to a blank page

    forcedLetter = False
    gameSearch = False #sets var to false
    lastGame = os.listdir(f"//TRUENAS/Games/Vimmslair_Archive/{items}")[-1] #gets the most recently downloaded game for the current console

    if lastGame != "": #testing to see if any games have actually been downloaded

        forcedLetter = True
        gameSearch = True #if games have been previously downloaded, set these to True
        
    #loop for selecting each letter (plus #)    
    for letter in letters:

        #tests to see if the current letter is the selected letter
        if letter == lastGame[0].upper():

            forcedLetter = False #stops loop waiting for the selected letter

        #if it doesn't have any games previously downloaded then run
        if forcedLetter == False:

            print(f"\n{letter}\n") #print the current letter
            tableCount = 1 #reset the tableCount variable

            #if the letter "#" is selected then run
            if letter == "#":

                driver.execute_script(f"window.open('https://vimm.net/vault/?p=list&system={items}&section=number', '{letter}');") #open a new window
                driver.switch_to.window(f"{letter}") #switch to the new window
            
            #if the letter "#" is not selected then run
            else:

                driver.execute_script(f"window.open('https://vimm.net/vault/{items}/{letter}', '{letter}');") #open a new window
                driver.switch_to.window(f"{letter}") #switch to the new window

            #loops for the selected letter
            while True:

                #loop that waits for the site to fully load
                while loading:

                    #try to get a html element from the site
                    try:
                        loadElement = driver.find_element(By.CLASS_NAME, "active") #get html element
                        loading = False #break the loop
                    except:
                        pass
                
                loading = True #sets var to True so it loads for the next opened webpage

                #if there are no previously downloaded games then run
                if gameSearch == False:

                    #try to get a table element
                    try:
                        table = driver.find_element(By.XPATH, f'//*[@id="main"]/div[2]/div/div[3]/table/tbody/tr[{tableCount}]/td[1]/a') #get table element

                    except:
                        break #break loop if no table elements left

                    link = table.get_attribute("href") #get the link from the table element
                    gameName = table.get_attribute("outerText") #gets the name of the game from the table element

                #if games have been downloaded previously then run
                while gameSearch:

                    table = driver.find_element(By.XPATH, f'//*[@id="main"]/div[2]/div/div[3]/table/tbody/tr[{tableCount}]/td[1]/a') #get table element

                    #if the current element is the last game downloaded then run
                    if (str(table.get_attribute("outerText")) + ".zip" == str(lastGame)) or (str(table.get_attribute("outerText")) + ".7z" == str(lastGame)):

                        link = table.get_attribute("href") #get the link form the table element
                        gameSearch = False #var for search for the last game is set to False
                        break #breaks the loop

                    else:
                        tableCount += 1 #moves to the next table element

                driver.execute_script(f"window.open('about:blank', '{tableCount}');") #open new blank chrome page
                driver.switch_to.window(f"{tableCount}") #switches to the new page
                driver.get(link) #goes to the selected link

                button = driver.find_element(By.XPATH, '//*[@id="download_form"]/button') #find the download button
                button.click() #clicks the download button

                #tests to see if there is a screen popup
                try:

                    contButton = driver.find_element(By.XPATH, '//*[@id="tooltip4"]/tbody/tr/td/div/input') #find continue button on popup
                    contButton.click() #click the continue button

                except:
                    pass

                #loop that wait for the file to finish downloading
                while downloading:

                    #gets the file being downloaded
                    for files in os.listdir("//TRUENAS/Games/Downloads"):

                        #if the file ends with a .zip or .7z then run
                        if files.endswith(".zip") or files.endsiwth(".7z"):

                            fileName = files #save the file name
                            downloading = False #stop the loop
                
                #tries to move the downloaded file from the download folder to the folder for its respective console
                try:

                    shutil.move(f"//TRUENAS/Games/Downloads/{fileName}", f"//TRUENAS/Games/Vimmslair_Archive/{items}") #moves the file to a different folder

                #if the file can't be transfered
                except:

                    downloading = True #reset downloading loop variable
                    driver.close() #close the selected webpage
                    driver.switch_to.window(f"{letter}") #switch to webpage with the table of games
                    tableCount += 1 #increase tableCount (moves to next table element)

                downloading = True #reset downloading loop variable

                driver.close() #close the selected webpage
                driver.switch_to.window(f"{letter}") #switch to the webpage with the table of games
                tableCount += 1 #increase tableCount (moves to the next table element)

        #if the current letter isnt the selected letter        
        else:
            pass
    
    driver.quit()
    time.sleep(1)