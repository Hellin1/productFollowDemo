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



def databaseEkle():
    # vt = sqlite3.connect(r'd\pro.sqlite3')
    # im = vt.cursor()
    # degEkle = "INSERT INTO product(title, fiyatlar) VALUES (7, 8)"
    # im.execute(degEkle)

    # for i in im.execute("SELECT * FROM product"):
    #     print(i)

    import sqlite3

    con = sqlite3.connect("d/aga.sqlite")

    # with con:

    #     c = con.cursor()

    #     c.execute('''CREATE TABLE prices
    #                 (pro_id INTEGER PRIMARY KEY,
    #                 title varchar(20) NOT NULL,
    #                 price varchar(20) NOT NULL)''')

        

    sayac = 0
    sayaca = 0
    
    f = open("products.txt","r",encoding="utf-8")
    # print(f.readlines())
    for x in f.readlines():
        yap = False
        sayaca +=1
        print("sayaca:", sayaca)
        # print(x)
        if (x[-3:-1]) == 'TL':
            # fiyat = x[-3:-1]
            fiyat = x

            yap = True

            # print(x)
            
        elif x == "\n":
            pass
        else:
            titled = ((x[:-1]))

        

        if "fiyat" in locals() and yap:

            print(titled)
            print("fiyat: ", fiyat)

            deger = (TimedRotatingFileHandler, fiyat)
            deger = (fiyat, time)
            print(len(deger,))
            print(len(titled))

            with con:

                c = con.cursor()

                now = datetime.datetime.now()
                deger = (fiyat, now)

            #     c.execute("INSERT INTO table (name, id, datecolumn) VALUES (%s, %s, '%s')",
            #    ("name", 4, now))

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

                # pro = c.fetchone()[0]
                # print(pro)
                # print(type(pro))
                # print("titled: ",titled)
                # print(type(titled))

                # titlex = (pro, titled)

                # c.execute("SELECT pro_id FROM products where title=?", (titled,))

                # c.execute('INSERT OR IGNORE INTO products(pro_id, title) VALUES (?,?)', (pro,(titled)))
                # c.execute("SELECT MAX(pro_id) FROM products")
                # # print("fetc: ",c.fetchone())
                # # con.commit()
                # pro = c.fetchone()[0]
                # print("pro:",pro)
                # deger = (fiyat, now, pro)


                # c.executemany('INSERT INTO prices(price, time, pro_id) VALUES (?,?,?)', (deger,))

                # print(c.lastrowid)
                # c.execute("SELECT MAX(pro_id) FROM products")
                # print("fetc: ",c.fetchone())
                # print("sayac:",sayac)
                sayac += 1

                


                # c.execute('INSERT INTO products(title) VALUES (?)', (titled,))
                # c.executemany('INSERT INTO prices(price, time) VALUES (?,?)', (deger,))

            
            
        
    f.close()
    # # print(liste)
    # for pro in liste:
    #     # titlePrice = [(pro[0], pro[1]),
    #     #                     ('Adam', 2000),
    #     #                     ('Andrew', 300),
    #     #                     ('James', 450),
    #     #                     ('Eric', 500)]


    #     con = sqlite3.connect("aga.sqlite")

    #     with con:

    #         c = con.cursor()

    #         c.execute('''CREATE TABLE prices
    #                     (pro_id INTEGER PRIMARY KEY,
    #                     title varchar(20) NOT NULL,
    #                     price varchar(20) NOT NULL)''')
    #         c.executemany('INSERT INTO prices(title, price) VALUES (?,?)', (pro[0],pro[1]))

    #         print("asdas")

    #         for row in c.execute('SELECT * FROM prices'):
    #             print(row)
    #             print("row")


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
