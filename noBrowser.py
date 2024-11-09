import requests
from playwright.sync_api import sync_playwright
import os
import time

def download(link):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)

        with page.expect_download() as download_info:
            page.locator('xpath=/html/body/div[4]/div[2]/div/div[3]/div[2]/div[1]/table/tbody/tr[21]/td/table/tbody/tr[1]/td[2]/form/button').click(timeout=30000)

        try:
            page.locator('xpath=//*[@id="tooltip4"]/tbody/tr/td/div/input').click()
        except:
            pass

        download = download_info.value
        download.save_as('C:/Users/thetr/Documents/games/a.zip')

def renameFile(file):
    for character in file:
        if character == ":":
            file = list(map(lambda x: x.replace(":", ""), list(file)))
        elif character == "/":
            file = list(map(lambda x: x.replace("/", ""), list(file)))
        elif character == "?":
            file = list(map(lambda x: x.replace("?", ""), list(file)))
        elif character == "*":
            file = list(map(lambda x: x.replace("*", ""), list(file)))
        elif character == '"':
            file = list(map(lambda x: x.replace('"', ""), list(file)))
        elif character == "<":
            file = list(map(lambda x: x.replace("<", ""), list(file)))
        elif character == ">":
            file = list(map(lambda x: x.replace(">", ""), list(file)))
        elif character == "|":
            file = list(map(lambda x: x.replace("|", ""), list(file)))
        file = "".join(file)

    os.rename("C:/Users/thetr/Documents/games/a.zip", f"C:/Users/thetr/Documents/games/{file}.zip")

files = os.listdir(r"C:\Users\thetr\Documents\Python\Vimmslair\downloads")
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","#"]
skip = False
count = 1
backCount = -1
selectConsole = False
consoleStart = []
exitCount = 0
waitGame = ""

print("Choose console game library to download:\nNES\nSMS\nGenesis\nSNES\nSaturn\nPS1\nN64\nDreamcast\nPS2\nXbox\nGameCube\nXbox360\nPS3\nWii\nWiiWare\nGB\nVB\nGBC\nGBA\nDS\nPSP\n\nTo select multiple consoles add a ',' then another console (eg. NES,SNES,Genesis)")
consoleInput = input("") 
consoleStart = input('Enter the name of the last downloaded game for each selected console.\ntype the console followed by colon and the name of the game in quotes.\nTo add the last game for several consoles put a comma after the quotes with no space then repeat the process.\nThe name of the game must match how it is display on Vimmslair exactly (is not case sensitive).\nPress enter if you do not need to enter any games\n\nexample: NES:"Abadox: The Deadly Inner War",SNES:"Accele Brid"\n')
consoleStart = consoleStart.lower()

if "," in consoleInput:

    consoles = consoleInput.split(",")
    print(consoles)

else:

    consoles = [consoleInput] 
    print(consoles) 

if consoleStart != "":
    if "," in consoleStart:
        consoleStart = consoleStart.split(",")
        for i in range(len(consoleStart)):
            consoleStart[i] = consoleStart[i].split(":")
            delList = list(consoleStart[i][1])
            del delList[0]
            del delList[-1]
            consoleStart[i][1] = "".join(delList)
    else:
        consoleStart = consoleStart.split(":")
        delList = list(consoleStart[1])
        del delList[0]
        del delList[-1]
        consoleStart[1] = "".join(delList)
        consoleStart = [consoleStart]

print(consoleStart)

for items in consoles:
    selectConsole = False

    for i in range(len(consoleStart)):
        if items in consoleStart[i][0]:
            waitGame = consoleStart[i][1]
            selectConsole = True
            break
        else:
            waitGame = ""
            selectConsole = False

    for letter in letters:
        tableSite = requests.get(f"https://vimm.net/vault/{items}/{letter}").text
        tableSite = tableSite.split('</caption>')[1].split('</table>')[0].split("\n")

        for i in range(len(tableSite)):
            if "<tr><td" in tableSite[i]:
                #exitCount += 1
                #if exitCount == 5:
                #    exit(1)
                
                fileName = tableSite[i].split(')">')#[1].split('</a>')[0]
                if len(fileName) == 1:
                    fileName = fileName[0].split('">')[2].split('</a>')[0]
                else:
                    fileName = fileName[1].split('</a>')[0]

                if "&amp;" in fileName:
                    fileName = fileName.split("&amp;")
                    fileName = fileName[0] + "&" + fileName[1]

                if "&#039;" in fileName:
                    fileName = fileName.split("&#039;")
                    fileName = fileName[0] + "'" + fileName[1]

                print(fileName)

                if selectConsole == True:
                    if fileName == waitGame:
                        selectConsole = False

                        gameSiteLink = "https://vimm.net" + str(tableSite[i].split('href="')[1].split('" onmouseover=')[0])
                        gameSite = requests.get(gameSiteLink).text

                        for items in files:
                            if fileName in items:
                                skip = True

                        skip = True
                        if skip == False:
                            print("downloading")
                            #download(fileName)
                else:
                    selectConsole = False

                    gameSiteLink = "https://vimm.net" + str(tableSite[i].split('href="')[1].split('" onmouseover=')[0])
                    gameSite = requests.get(gameSiteLink).text

                    for items in files:
                        if fileName in items:
                            skip = True

                    if skip == False:
                        try:
                            print("downloading")
                            download(gameSiteLink)
                            renameFile(fileName)
                            
                        except:
                            pass
                            
                        
                        #time.sleep(.5)