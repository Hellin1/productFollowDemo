import json
from logging.handlers import TimedRotatingFileHandler
import requests
from bs4 import BeautifulSoup as Soup
import time
import sqlite3
import datetime


headers = {'user-agent':'my-app/0.0.1'}

# veriye elde etme

max_page = 50

link = 'https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98' 
linke = 'https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa='


# print(res)
liste = []

def appendToDB(liste):
    con = sqlite3.connect("d/aga.sqlite")

    titled, fiyat = liste[0], liste[1] 

    with con:

        c = con.cursor()

        now = datetime.datetime.now()
        deger = (fiyat, now)


        c.execute("SELECT pro_id FROM products where title=(?)",(str(titled),))
        if c.fetchone() == None:
            c.execute("INSERT OR IGNORE INTO products(title) VALUES (?)", (titled,))
            c.execute("SELECT MAX(pro_id) FROM products")
            sid = c.fetchone()[0]
            deger = (fiyat, now, sid)
            c.execute("INSERT INTO prices(price, time, pro_id) VALUES (?,?,?)",(deger))
        else:
            c.execute("SELECT pro_id FROM products where title=(?)",(str(titled),))
            sid = c.fetchone()[0]
            print(sid)
            deger = (fiyat, now, sid)
            c.execute("INSERT INTO prices(price, time, pro_id) VALUES (?,?,?)", (deger))


def findProducts():
    count = 0
    for i in range(max_page):
        if i+1==1:
            link = 'https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98' 
        else:
            link = linke + str(i+1)
        print(link)

        r = requests.get(link, headers=headers)
        soup = Soup(r.text, "lxml")

        res = soup.find_all("li", {"class":"productListContent-item"})


        # database ekle, listeye ekle
        for pro in res:
            title = (pro.find("h3").text)
            if title != '' or title != None:
                count +=1 
            price = (pro.find("div", {"data-test-id":"price-current-price"}).text)
            
            if [title, price] not in liste:
                liste.append([title, price])
                appendToDB([title, price])

            else:
                # liste.append([title, price])
                pass
            print(title)
            print(price)

        time.sleep(4)


    print(len(liste))

    # metin belgesine ekle
    f = open("products.txt","w",encoding="utf-8")
    for x in liste:
        f.write(x[0])
        f.write("\n")
        f.write(x[1])
        f.write("\n")
    f.close()

def grafikOlustur(gid):
    con = sqlite3.connect("d/aga.sqlite")
    gfiyats = []
    gtarihs = []

    with con:

        c = con.cursor()

        # now = datetime.datetime.now()


        c.execute(f"SELECT prices.pro_id, prices.price, prices.time FROM prices INNER JOIN products ON prices.pro_id = products.pro_id WHERE prices.pro_id={gid} ORDER BY prices.pro_id")
        res = c.fetchall()
        for i in range(len(res)):
            gfiyat = (res[i][1][:-3].replace(",",""))
            gtarih = (res[i][2])
            # print(gtarih)
            gfiyats.append(float(gfiyat))
            gtarihs.append(gtarih)
            print(res[i])
            
        c.execute("SELECT title FROM products WHERE pro_id=4")
        res = c.fetchone()[0]
        print(res)

    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    print(gfiyats)
    print(gtarihs)


    x = gtarihs
    y = gfiyats

    plt.plot(x,y)
    plt.xlabel('tarihler')
    plt.ylabel('fiyatlar')

    c.execute(f"SELECT title FROM products WHERE pro_id={gid}")
    tit = c.fetchone()[0]
    plt.title(tit)

    data = [go.Line(x=x,y=y,name=tit)]
    layout = go.Layout(yaxis=dict(tickformat=".3f"), title=tit)

    fig = go.Figure(data=data, layout= layout)


    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=x, y=y,mode='lines',name='lines'))


    fig.show()
    # plt.show()
    


        
# while True:
#     findProducts()
# databaseEkle()
for i in range(130,230):
    grafikOlustur(i+1)
    time.sleep(1)
