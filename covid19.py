from tkinter import *
import requests
import mplcursors
import matplotlib.pyplot as plt
from tkinter import messagebox as msgbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import *
from pandastable import Table

def Table_It():
    All_Data = requests.get("https://api.covid19api.com/summary")
    All_Data = All_Data.json()
    All_Data = All_Data["Countries"]
    countries = []
    Tot_Case5 = []
    Tot_Case7 = []
    Tot_Case9 = []
    Tot_Case11 = []
    for i in All_Data:
        countries.append(i["Country"])
    for i in All_Data:
        Tot_Case5.append(i["TotalConfirmed"])
    for i in All_Data:
        Tot_Case7.append(i["TotalDeaths"])
    for i in All_Data:
        Tot_Case9.append(i["TotalRecovered"])
    for i in All_Data:
        Tot_Case11.append(i["Date"])
    frame = Frame(pencere)
    frame.place(x=1000, y=0, height=652, width=900)
    df1 = {"Country": countries, "Confirmed": Tot_Case5, "Deaths": Tot_Case7, "Recovered": Tot_Case9,
           "Date": Tot_Case11}
    df = DataFrame(df1)
    table = Table(frame, dataframe=df)

    table.columncolors["Confirmed"] = "#ff6666"
    table.columncolors["Deaths"] = "#8c8c8c"
    table.columncolors["Recovered"] = "#94ff9b"
    table.redraw()

    table.show()

def Searchfnk():
    listcntry.select_clear(0, END)
    search = False
    for i in range(0, 248):
        if entSearch.get() == listcntry.get(i):
            listcntry.select_set(i)
            listcntry.see(i)
            search = True
    if not search:
        msgbox.showwarning(title="Error", message="Please check the country name!!!")

def Showgraph(y, types, type, graphtype, colour,cname):
    data = {"Days": y, types: type}

    datafr = DataFrame(data, columns=["Days", types])
    fig = plt.Figure(figsize=(8.1, 6.5), dpi=100)
    Ax = fig.add_subplot(111)
    bar = FigureCanvasTkAgg(fig, pencere)
    bar.get_tk_widget().place(x=200, y=0)
    datafr = datafr[["Days", types]].groupby("Days").sum()
    datafr.plot(kind=graphtype, ax=Ax, legend=True, fontsize=7, color=colour )
    Ax.set_facecolor("#01132d")
    Ax.set_title(cname)

    mouse = mplcursors.cursor(Ax)
    mouse.connect("add", lambda sel: sel.annotation.set_text(
        ("%s : {} \n Days : {}" % (types)).format(int(sel.target[1]), int(sel.target[0]) + 1)))

def ShowgraphDaily(y, types, type, graphtype, colour, cname):
    data = {"Days": y, types: type}

    datafr = DataFrame(data, columns=["Days", types])
    fig = plt.Figure(figsize=(8.1, 6.5), dpi=100)
    Ax = fig.add_subplot(111)
    bar = FigureCanvasTkAgg(fig, pencere)
    bar.get_tk_widget().place(x=200, y=0)
    datafr = datafr[["Days", types]].groupby("Days").sum()
    datafr.plot(kind=graphtype, ax=Ax, legend=True, fontsize=7, color=colour)
    Ax.set_facecolor("#01132d")
    Ax.set_title(cname)
    mouse = mplcursors.cursor(Ax)
    mouse.connect("add", lambda sel: sel.annotation.set_text(
        ("%s :  {} \n Days : {}" % (types)).format(float(sel.target[1]), int(sel.target[0]) + 1)))

def Datas():
    slug = []
    for i in json1:
        slug.append(i["Slug"])
        slug = sorted(slug)

    for i in range(listcntry.size() - 1, -1, -1):
        if listcntry.select_includes(i):
            country_number = i
            cname = listcntry.get(i)
    for i in range(listdata.size() - 1, -1, -1):
        if listdata.select_includes(i):
            DataType = listdata.get(i)
    if cname == "China":
        response = requests.get("https://api.covid19api.com/total/country/China")
        countrydata = response.json()
    else:
        response = requests.get("https://api.covid19api.com/total/dayone/country/%s" % (slug[country_number]))
        countrydata = response.json()


    confirmed = []

    if DataType == "Confirmed":
        x = 1
        y = []
        for i in countrydata:
            confirmed.append(i["Confirmed"])
            x += 1
        for i in range(1, x):
            y.append(i)

        types = "Confirmed"
        graphtype = "line"
        colour = "red"
        Showgraph(y, types, confirmed, graphtype, colour, cname)

    deaths = []

    if DataType == "Deaths":
        x = 1
        y = []
        for i in countrydata:
            deaths.append(i["Deaths"])
            x += 1
        for i in range(1, x):
            y.append(i)
        types = "Deaths"
        graphtype = "line"
        colour = "black"
        Showgraph(y, types, deaths, graphtype, colour,cname)

    active = []
    if DataType == "Active":
        x = 1
        y = []
        for i in countrydata:
            active.append(i["Active"])
            x += 1
        for i in range(1, x):
            y.append(i)

        types = "Active"
        graphtype = "line"
        colour = "orange"
        Showgraph(y, types, active, graphtype, colour, cname)

    recovered = []
    if DataType == "Recovered":
        x = 1
        y = []
        for i in countrydata:
            recovered.append(i["Recovered"])
            x += 1
        for i in range(1, x):
            y.append(i)

        types = "Recovered"
        graphtype = "line"
        colour = "blue"

        Showgraph(y, types, recovered, graphtype, colour, cname)

    dailyconfirmed = []
    if DataType == "Daily-Confirmed":
        x = 1
        y = []
        dcnf = []
        for i in countrydata:
            dcnf.append(i["Confirmed"])
            x += 1
        for i in range(0, (x) - 2):
            if (dcnf[i + 1] - dcnf[i]) <= 0:
                dailyconfirmed.append(0)
            else:
                dailyconfirmed.append(dcnf[i + 1] - dcnf[i])
            y.append(i + 1)
        types = "Daily Confirmed"
        colour = "red"
        graphtype = "bar"
        Showgraph(y, types, dailyconfirmed, graphtype, colour, cname)

    dailydeaths = []
    if DataType == "Daily-Deaths":
        x = 1
        y = []
        ddts = []
        for i in countrydata:
            ddts.append(i["Deaths"])
            x += 1
        for i in range(0, (x) - 2):
            if (ddts[i + 1] - ddts[i]) <= 0:
                dailydeaths.append(0)
            elif (ddts[i + 1] - ddts[i]) > 0:
                dailydeaths.append(ddts[i + 1] - ddts[i])
            y.append(i + 1)

        types = "Daily Confirmed"
        colour = "black"
        graphtype = "bar"
        Showgraph(y, types, dailydeaths, graphtype, colour, cname)

    dailyrecovered = []
    if DataType == "Daily-Recovered":
        x = 1
        y = []
        drcv = []
        for i in countrydata:
            drcv.append(i["Recovered"])
            x += 1
        for i in range(0, (x) - 2):
            if (drcv[i + 1] - drcv[i]) <= 0:
                dailyrecovered.append(0)
            elif (drcv[i + 1] - drcv[i]) > 0:
                dailyrecovered.append(drcv[i + 1] - drcv[i])
            y.append(i + 1)
        types = "Daily Recovered"
        colour = "blue"
        graphtype = "bar"
        Showgraph(y, types, dailyrecovered, graphtype, colour, cname)

    if DataType == "Daily-Confirmed %":
        x = 1
        y = []
        dcnf = []
        dcnfper = []
        for i in countrydata:
            dcnf.append(i["Confirmed"])
            x += 1
        for i in range(0, (x) - 2):
            if (dcnf[i + 1] - dcnf[i]) <= 0:
                dailyconfirmed.append(0)
            else:
                dailyconfirmed.append(dcnf[i + 1] - dcnf[i])
            y.append(i + 1)
            if dcnf[i + 1] - dcnf[i] <= 0:
                dcnfper.append(0)
            else :
                dcnfper.append((((dcnf[i + 1] - dcnf[i])) /dcnf[i])*100)

        types = "Daily Confirmed %"
        colour = "red"
        graphtype = "bar"
        ShowgraphDaily(y, types, dcnfper, graphtype, colour, cname)

    if DataType == "Daily-Deaths %":
        x = 1
        y = []
        dcnf = []
        dcnfper = []
        for i in countrydata:
            dcnf.append(i["Deaths"])
            x += 1
        for i in range(0, (x) - 2):
            if (dcnf[i + 1] - dcnf[i]) <= 0:
                dailyconfirmed.append(0)
            else:
                dailyconfirmed.append(dcnf[i + 1] - dcnf[i])
            y.append(i + 1)

            if dcnf[i + 1] - dcnf[i] <= 0:
                dcnfper.append(0)
            else:
                dcnfper.append((((dcnf[i + 1] - dcnf[i])) / dcnf[i+1]) * 100)

        types = "Daily Deaths %"
        colour = "black"
        graphtype = "bar"
        ShowgraphDaily(y, types, dcnfper, graphtype, colour, cname)

    if DataType == "Daily-Recovered %":
        x = 1
        y = []
        dcnf = []
        dcnfper = []
        for i in countrydata:
            dcnf.append(i["Recovered"])
            x += 1
        for i in range(0, (x) - 2):
            if (dcnf[i + 1] - dcnf[i]) <= 0:
                dailyconfirmed.append(0)
            else:
                dailyconfirmed.append(dcnf[i + 1] - dcnf[i])
            y.append(i + 1)

            if dcnf[i + 1] - dcnf[i] <= 0:
                dcnfper.append(0)
            else:
                dcnfper.append((((dcnf[i + 1] - dcnf[i])) / dcnf[i+1]) * 100)

        types = "Daily Recovered %"
        colour = "blue"
        graphtype = "bar"
        ShowgraphDaily(y, types, dcnfper, graphtype, colour, cname)

pencere = Tk()
pencere.geometry("1500x650")
pencere.title("CORONAVIRUS STATISTICS")
pencere.iconbitmap(r"covid19.ico")

frameData = Frame(pencere, bg="#01132d", relief=RIDGE, width=200, height=650, border=2)
frameData.place(x=0, y=0)



framegrf = Frame(pencere, bg="#01132d", relief=RIDGE, width=1300, height=650, border=2)
framegrf.place(x=200, y=0)
foto = PhotoImage(file="Map.png")
lblfoto = Label(framegrf, image=foto)
lblfoto.place(x=0, y=0)
foto2 = PhotoImage(file="infolist.png")
lblfoto2 = Label(frameData, image=foto2)
lblfoto2.place(x=1, y=468)

# Countries
entSearch = Entry(frameData, font="Calibri", width=20, text="Search a country")  #
entSearch.place(x=0, y=3)

butSearch = Button(frameData, text="Search", font=("Calibri"), width=5, command=Searchfnk)
butSearch.place(x=147, y=0)
lblcntry = Label(frameData, bg="#797472", text="COUNTRIES", font=("Calibri"))
lblcntry.place(x=50, y=27)
listcntry = Listbox(pencere, bg="#cc0505", font="Calibri", width=24, height=11, exportselection=0)
listcntry.place(x=1, y=53)

scrollbar = Scrollbar(pencere, orient="vertical")
scrollbar.config(command=listcntry.yview)
scrollbar.place(x=183, y=53, height=225)
listcntry.config(yscrollcommand=scrollbar.set)

# Datas
lbldata = Label(frameData, bg="#797472", text="DATA TYPES", font=("Calibri"))
lbldata.place(x=50, y=275)
listdata = Listbox(frameData, bg="#cc0505", font="Calibri", width=24, height=7, exportselection=0)
listdata.place(x=1, y=297)

scrollbar = Scrollbar(pencere, orient="vertical")
scrollbar.config(command=listdata.yview, bg="red")
scrollbar.place(x=183, y=299, height=146)
listdata.config(yscrollcommand=scrollbar.set)

# Info
lblinfo = Label(frameData, bg="#797472", text="INFO", font=("Calibri"))
lblinfo.place(x=70, y=443)


butShow = Button(frameData, text="Show", font=("Calibri"), width=5, command=Datas)
butShow.place(x=20, y=615)



url1 = "https://api.covid19api.com/countries"
country = []
slug = []
response = requests.get(url1)
json1 = response.json()


for i in json1:
    country.append(i["Country"])
butTable = Button(frameData, text='Table it', font='Calibri', width=6, command=Table_It)
butTable.place(x=120, y=615)

country = sorted(country)
country[0] = "Ala Aland Island"
country[190] = "Saint Barthêlemy"
country[191] = "Saint Martin (French part)"
country[231] = "Us Minor Outlying Islands"
country[58] = "Cote D'Ivoire"
country = sorted(country)
for i in country:
    listcntry.insert(END, i)

datatype = ["Confirmed", "Deaths", "Recovered", "Active", "Daily-Confirmed", "Daily-Deaths", "Daily-Recovered",
            "Daily-Confirmed %", "Daily-Deaths %", "Daily-Recovered %"]
for i in datatype:
    listdata.insert(END, i)

pencere.mainloop()
