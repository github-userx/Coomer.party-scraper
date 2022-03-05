from bs4 import BeautifulSoup
import requests 
import time
    
scrapeVideos = False

def coom():
    number = 0
    file = open("Entry List.txt", "r+").readlines()
    #For Every Entry
    for entry in file:
        print("\nNew Entry Started: "+entry+"\n")
        #open page of entry
        result = requests.get("https://coomer.party"+str(entry).strip())
        postpage = BeautifulSoup(result.content, "html.parser")
        #find the img links
        try:
            postfiles = postpage.find("div", class_="post__files")
            images = postfiles.find_all("img")
        except:
            print("\nNo images found in this entry\n")

        #if get videos is selected, then also find video links
        if scrapeVideos == True:
            try:
                entryattachments = postpage.find("ul", class_="post__attachments")
                videos = entryattachments.find_all("a")

                for video in videos:
                    try:
                        video_src = video["href"]
                        print(video_src)
                    except:
                        print("\nError in ripping a video\n")
                        continue
                    video_data = requests.get("https://data1.coomer.party"+video_src).content
                    with open(str(number)+'.mp4', 'wb') as handler:
                        handler.write(video_data)
                    number += 1

            except:
                print("No videos for entry")


        #save images to disk
        for image in images:
            try:
                image_src = image["src"]
                print(image_src)
            except:
                print("Error in ripping an image\n")
                continue
            img_data = requests.get("https://www.coomer.party"+image_src).content
            with open(str(number)+'.jpg', 'wb') as handler:
                handler.write(img_data)
            number += 1
    print("Cooming has finished, enjoy your files!")

def ScanningPosts(url):
    try:
        result = requests.get(url)
        mainpage = BeautifulSoup(result.content, "html.parser")
    except:
        print("URL brought an error, please check and make sure it is formatted correctly\neg. https://www.coomer.party + creator link with no extra characters or page identifiers")
    posts = []

#calculate amount of pages
    try:
        nextpagebutton = mainpage.find(title="Next page").parent
        maxpagelink = nextpagebutton.find_previous("li")
        lin = maxpagelink.find("a")
        link = lin["href"]
        lastPage = str(link).split("=")[-1]
        print("Successfully Calculated Amount of Pages as "+str((int(lastPage)/25)+1))
    except:
        print("Error Occured: Likely DDos Protection, wait a couple minutes then try again. (Or use a VPN)")

    #Finds all Entry links on current page
    def fetchPagesEntryLinks():
        #find the entry link html code
        tagOfPosts = mainpage.find_all("h2",class_="post-card__heading")
        for post_ in tagOfPosts:
            link = post_.find("a")
            #add said entry link to posts list
            posts.append(link["href"])
            print("Discovered entry: "+str(link["href"]))

    #fetch first page links then iterate through pages until last page
    pageNumber = 0
    while pageNumber <= int(lastPage):
        fetchPagesEntryLinks()
        pageNumber += 25
        print("Fetching posts on page "+str((pageNumber/25)))
        time.sleep(1)
        result = requests.get(url+"?o="+str(pageNumber))
        mainpage = BeautifulSoup(result.content, "html.parser")

    postlistFile = open("Entry List.txt", "w")
    for entry in posts:
        postlistFile.write(entry+"\n")
    postlistFile.close()
    continuetocoom = input("\nFinished gathering entries, begin scraping?\nY / N: ").lower().strip()
    if continuetocoom == "y":
        coom()
    else:
        print("Exiting...")
        exit
#START
print("\nWelcome to the coomer.party scraper made by EGirlEnthusiast")
try:
    testtoseeiffileexists = open("Entry List.txt", "r")
    print("\nEntries detected, skipping to rip, to recalculate posts delete Entry List.txt\n")
    includevidschoice = input("Include scraping of videos?\nY / N: ").lower().strip()
    if includevidschoice == "y":
        scrapeVideos = True
    else:
        scrapeVideos = False
    coom()
except:
    url = input("Please Enter URL of creator from coomper.party (Ensure no text exists after the creator's name, in the link)\nURL: ")
    ScanningPosts(url)
