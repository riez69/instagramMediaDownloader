import requests
import re
import json
#siteurl = str(input(("masukkan link post instagram: ")))
#siteurl = "https://www.instagram.com/p/CMNyruLARPg/?utm_source=ig_web_copy_link"
link = "testinstagram.html"

# download seluruh isi website
def downloader(link):
    list = []
    param = {"property":"og:image"}
    parse = link
    req = requests.get(parse, headers = {'user-agent' : 'your bot 0.1'}, stream=True)
    for i in req.iter_lines():
        if i: list.append(i)
    with open("testinstagram.html", "w") as file:
        for i in list:
            file.write(str(i)+"\n")
    return ("testinstagram.html")

# buka file html
def htmlfile(link):
    list =[]
    with open(link, "r")as file:
        for i in file.readlines():
            list.append(i.replace("b\'", ""))
    return(list)

# mendapatkan caption dalam bentuk mentah
def rawCaption(list):
    for i in list:
        if "<script type=\"application/ld+json\">" in i:
            indextag = list.index(i) 
            rawcaption = list[indextag+1]
    return(rawcaption)

#jangan diubah !!!
# memproses caption mentah
def caption(rawcaption):
    string = ""
    stringrev1 = ""
    data = str(rawcaption).split("\\n")
    for i in data:
        # menangani awal dan akhir caption
        if "\"representativeOfPage\":" in i:
            listakhir = i.split(",")
            for x in listakhir:
                if "representativeOfPage" in x:
                    break
                else:
                    string += x+ ""
        elif "{\"@context\"" in i:
            listawal = i.split()
            for y in listawal:
                if (re.search("\"caption\":",y)):
                    string += (y.split(":")[-1])+" "
                else:
                    string += y+ " "               
        else:
            string += i

    for i in string.split():
        if re.search(r"\\ud\w{3}", i):
            jsonstring = ""
            val = re.findall(r"\\ud\w{3}", i)
            notval = re.split(r"\\ud\w{3}", i)
            for y in notval:
                for xy in y:
                    stupidstring = ""
                    if "\\" not in xy:
                        stupidstring += y
            jsonstring+=(stupidstring.replace("\\", ""))

            for x in val:
                jsonstring += x
            stringrev1 += (json.loads(r'"{}"'.format(jsonstring)))+" "
        else:
            stringrev1+= i+" "
    return (stringrev1.replace("\\", "\n").replace("/", "").replace("&quot;", "\""))

# dapatkan url media
def imageUrl(list):
    list1 = []
    urllist = []
    # jika struktur wesite berubah tinggal cari key nya di javascript
    for i in list:
        if "display_resource" in i:
            for x in i.split(","):
                if "display_resource" in x:
                    list1.append(x)
   
    for row in list1:
         head = re.search(r"https", row)
         end = re.finditer(r"\"", row)
         httphead = (head.span()[0])

         for finish in end:
            httpend = (finish.span()[0])

         urllist.append(row[httphead:httpend].replace("\\u0026", "&").replace("\\", ""))
    return urllist

def videoUrl(list):
    list1 = []
    urllist = []
    # jika struktur website berubah tinggal  cari "video_url atau sejenisnya"
    for i in list:
        if "video_url" in i:
            #print(i)
            for x in i.split(","):
                if "video_url" in x:
                    list1.append(x)
    # mengurai string untuk mendapatkan url bersih
    for row in list1:
        httphead = re.search(r'https', row)
        httpend = re.finditer(r'\"', row)
        firsindex = httphead.span()[0]
        for y in httpend:
            lastindex = y.span()[0]
        urllist.append(row[firsindex:lastindex].replace("\\u0026", "&").replace("\\", ""))
    return (urllist)

# downloader ubah bagian judul
def downloadFile(list):
    # memulai request ke link kemudian menulis bytenya ke file
    # NOTE! nama file sama dengan nama link sesudah tanda khusus dibuang
    index = 0
    for link in list:
        newlink = re.sub('[^a-zA-Z0-9 \n\.]', '', link)+str(index)
        judul = str(newlink+ ".mp4" if "mp4" in link else newlink+ ".jpg")
        index +=1
        param = {"property":"og:image"}
        parse = link
        req = requests.get(parse, headers = {'user-agent' : 'your bot 0.1'}, stream=True)
        if req.status_code== 200:
            with open("{}".format(judul), "wb") as file:
                file.write(req.content)
                print("{} terunduh".format(judul))
        else:
            print("gagal mengunduh {}".format(link))

# simplifikasi alur program
def downloadAsset(link):
    fileHtml = htmlfile(downloader(link))

    captionDownloader = caption(rawCaption(fileHtml))
    photosUrl = imageUrl(fileHtml)
    videosUrl = videoUrl(fileHtml)
    photoDownloader = downloadFile(photosUrl)
    videoDownloader = downloadFile(videosUrl)
    print((videosUrl))
   

siteurl= "https://www.instagram.com/p/CMk0voUJrws/?igshid=hcfgjbeum61q"


downloadAsset(siteurl)
