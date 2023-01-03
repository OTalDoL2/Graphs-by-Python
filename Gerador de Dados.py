from tkinter import *
import numpy as np
import xarray as xr
import pandas as pd
import time

janela = Tk()
label = Label(janela, text='Menu Principal')
label.pack()


def gerar_diario():
    global janela
    janela.destroy()
    janela = Tk() 
    label = Label(janela, text='Dados Diários')
    label.pack()
    janela.geometry("600x600+250+50")

    #Select relacionado ao Mês
    month_value = StringVar(value=1)
    month = Spinbox( janela, from_=1, to=12, textvariable=month_value)
    month.pack()
    month.place(x=100,y=80)
    month_label = Label(janela, text='Month')
    month_label.place(x=50,y=80)
    
    #Select relacionado ao Ano
    year_value = StringVar(value=2020)
    year = Spinbox( janela, from_=2001, to=2020, textvariable=year_value)
    year.pack()
    year.place(x=390,y=80)
    year_label = Label(janela, text='Year')
    year_label.place(x=350,y=80)
    
    #Checkbox
    def check_eto():
        if var1.get() == 1:
            array_items.append("ETo")
        elif var1.get() == 0: 
            array_items.remove("ETo")
            
#    def add_to_btn():
        
    def check_pr():
        if var2.get() == 1:
            array_items.append("pr")
        elif var2.get() == 0: 
            array_items.remove("pr")
 
    def check_tmin():
        if var3.get() == 1:
            array_items.append("Tmin")
        elif var3.get() == 0: 
            array_items.remove("Tmin")
 
    def check_tmax():
        if var4.get() == 1:
            array_items.append("Tmax")
        elif var4.get() == 0: 
            array_items.remove("Tmax")
    
    def check_rh():
        if var5.get() == 1:
            array_items.append("RH")
        elif var5.get() == 0: 
            array_items.remove("RH")
    
    def check_rs():
        if var6.get() == 1:
            array_items.append("Rs")
        elif var6.get() == 0: 
            array_items.remove("Rs")
    
    def check_u2():
        if var7.get() == 1:
            array_items.append("u2")
        elif var7.get() == 0: 
            array_items.remove("u2")     
        
        
    def generate_file():
        ### ===== EXTRAÇÃO DE DADOS MENSAIS ===== #

        path_var = 'C:\\Users\lucas.ramos\OneDrive\Desktop\Base Climatica\Tipos/'

        # Posicoes: Colocar em ordem, separando por virgula. Neste exemplo temos dois pontos em que as coordenadas
        # (lat, lon) sao (-20.6,-44.6) e  (-21.0, -44.1), respectivamente para o primeiro e segundo ponto.
        # Pode-se colocar quantos pontos quiser, apenas separe por virgula.

        #Região de Fazendas no Maranhão
        lat = [float(lt.get())]
        lon = [float(long.get())]

        # function to read the netcdf files
        def rawData(var2get_xr, var_name2get):
            return var2get_xr[var_name2get].sel(longitude=xr.DataArray(lon, dims='z'),
                                                latitude=xr.DataArray(lat, dims='z'),
                                                method='nearest').values

        # getting data from NetCDF files
        for n, var_name2get in enumerate(var_names):
            print("getting " + var_name2get)
            var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc')
            if n == 0:
                var_ar = rawData(var2get_xr, var_name2get)
                n_lines = var_ar.shape[0]
                time = var2get_xr.time.values
            else:
                var_ar = np.c_[var_ar, rawData(var2get_xr, var_name2get)]

        # saving
        for n in range(len(lat)):
            name_file =  'lat{:.2f}_lon{:.2f}.csv'.format(lat[n], lon[n])
            print(f'arquivo {n + 1} de um total de {len(lat)}; nome do arquivo: {name_file}')
            if ~np.isnan(var_ar[0, n]):
                file = var_ar[:, n::len(lon)]
                pd.DataFrame(file, index=time, columns=var_names).to_csv(name_file, float_format='%.1f')
        
       
        
    
            
        
    array_items = []
    
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    var7 = IntVar()
    
    c1 = Checkbutton(janela, text='ETo',variable=var1, onvalue=1, offvalue=0, command=check_eto)
    c1.pack()
    c1.place(x=50,y=120)
    
    c2 = Checkbutton(janela, text='pr',variable=var2, onvalue=1, offvalue=0, command=check_pr)
    c2.pack()
    c2.place(x=130,y=120)

    c3 = Checkbutton(janela, text='Tmin',variable=var3, onvalue=1, offvalue=0, command=check_tmin)
    c3.pack()
    c3.place(x=190,y=120)
    
    c4 = Checkbutton(janela, text='Tmax',variable=var4, onvalue=1, offvalue=0, command=check_tmax)
    c4.pack()
    c4.place(x=270,y=120)
    
    c5 = Checkbutton(janela, text='RH',variable=var5, onvalue=1, offvalue=0, command=check_rh)
    c5.pack()
    c5.place(x=350,y=120)
    
    c6 = Checkbutton(janela, text='Rs',variable=var6, onvalue=1, offvalue=0, command=check_rs)
    c6.pack()
    c6.place(x=420,y=120)
    
    c7 = Checkbutton(janela, text='u2',variable=var7, onvalue=1, offvalue=0, command=check_u2)
    c7.pack()
    c7.place(x=480,y=120)
    
    Label(janela, text="Latitude", background="#abf321", foreground="#009", anchor=W).place(x=10, y=200, width=150)
    lt=Entry(janela)
    lt.place(x=10, y=220, width=200, height=20)
    
    Label(janela, text="Longitude", background="#abf321", foreground="#009", anchor=W).place(x=10, y=260, width=150)
    long=Entry(janela)
    long.place(x=10, y=280, width=200, height=20)
    
    mostra = Button(janela, text='Gerar Dados .csv', command=generate_file)
    mostra.pack()
    
    menu_bt = Button(janela, text='Voltar/Menur',command=menu)
    menu_bt.pack()


    

def gerar_mensal():
    global janela
    janela.destroy()
    janela = Tk() 
    label = Label(janela, text='Dados Mensais')
    label.pack()
    janela.geometry("600x600+250+50")

    #Select relacionado ao Mês
    month_value = StringVar(value=1)
    month = Spinbox( janela, from_=1, to=12, textvariable=month_value)
    month.pack()
    month.place(x=100,y=80)
    month_label = Label(janela, text='Month')
    month_label.place(x=50,y=80)
    
    #Select relacionado ao Ano
    year_value = StringVar(value=2020)
    year = Spinbox( janela, from_=2001, to=2020, textvariable=year_value)
    year.pack()
    year.place(x=390,y=80)
    year_label = Label(janela, text='Year')
    year_label.place(x=350,y=80)
    
    #Checkbox
    def check_eto():
        if var1.get() == 1:
            array_items.append("ETo")
        elif var1.get() == 0: 
            array_items.remove("ETo")
            
#    def add_to_btn():
        
    def check_pr():
        if var2.get() == 1:
            array_items.append("pr")
        elif var2.get() == 0: 
            array_items.remove("pr")
 
    def check_tmin():
        if var3.get() == 1:
            array_items.append("Tmin")
        elif var3.get() == 0: 
            array_items.remove("Tmin")
 
    def check_tmax():
        if var4.get() == 1:
            array_items.append("Tmax")
        elif var4.get() == 0: 
            array_items.remove("Tmax")
    
    def check_rh():
        if var5.get() == 1:
            array_items.append("RH")
        elif var5.get() == 0: 
            array_items.remove("RH")
    
    def check_rs():
        if var6.get() == 1:
            array_items.append("Rs")
        elif var6.get() == 0: 
            array_items.remove("Rs")
    
    def check_u2():
        if var7.get() == 1:
            array_items.append("u2")
        elif var7.get() == 0: 
            array_items.remove("u2")     
        
        
    def generate_file():
        ### ===== EXTRAÇÃO DE DADOS MENSAIS ===== #

        path_var = 'C:\\Users\lucas.ramos\OneDrive\Desktop\Base Climatica\Tipos/'

        # Posicoes: Colocar em ordem, separando por virgula. Neste exemplo temos dois pontos em que as coordenadas
        # (lat, lon) sao (-20.6,-44.6) e  (-21.0, -44.1), respectivamente para o primeiro e segundo ponto.
        # Pode-se colocar quantos pontos quiser, apenas separe por virgula.

        #Região de Fazendas no Maranhão
        lat = [float(lt.get())]
        lon = [float(long.get())]

        # variables names
        # var_names = ['Rs', 'u2','Tmax', 'Tmin', 'RH', 'pr', 'ETo']
        var_names = array_items

        # function to read the netcdf files
        def rawData(var2get_xr, var_name2get):
            return var2get_xr[var_name2get].sel(longitude=xr.DataArray(lon, dims='z'),
                                                latitude=xr.DataArray(lat, dims='z'),
                                                method='nearest').values

        # getting data from NetCDF files
        for n, var_name2get in enumerate(var_names):
            print("getting " + var_name2get)
            if var_name2get in ["pr", "ETo"]:
                var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").sum("time")
                # var2get_xr[var_name2get].sel(latitude=lat[0], longitude=lon[0], method='nearest').plot()
            else:
                var2get_xr = xr.open_mfdataset(path_var + var_name2get + '*.nc').resample(time="M").mean("time")

            if n == 0:
                var_ar = rawData(var2get_xr, var_name2get)
                n_lines = var_ar.shape[0]
                time = var2get_xr.time.values
            else:
                var_ar = np.c_[var_ar, rawData(var2get_xr, var_name2get)]

        # saving
        for n in range(len(lat)):
            name_file =  'lat{:.2f}_lon{:.2f}.csv'.format(lat[n], lon[n])
            print(f'arquivo {n + 1} de um total de {len(lat)}; nome do arquivo: {name_file}')
            if ~np.isnan(var_ar[0, n]):
                file = var_ar[:, n::len(lon)]
                pd.DataFrame(file, index=time, columns=var_names).to_csv(name_file, float_format='%.1f')
        
       
        
    
            
        
    array_items = []
    
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    var7 = IntVar()
    
    c1 = Checkbutton(janela, text='ETo',variable=var1, onvalue=1, offvalue=0, command=check_eto)
    c1.pack()
    c1.place(x=50,y=120)
    
    c2 = Checkbutton(janela, text='pr',variable=var2, onvalue=1, offvalue=0, command=check_pr)
    c2.pack()
    c2.place(x=130,y=120)

    c3 = Checkbutton(janela, text='Tmin',variable=var3, onvalue=1, offvalue=0, command=check_tmin)
    c3.pack()
    c3.place(x=190,y=120)
    
    c4 = Checkbutton(janela, text='Tmax',variable=var4, onvalue=1, offvalue=0, command=check_tmax)
    c4.pack()
    c4.place(x=270,y=120)
    
    c5 = Checkbutton(janela, text='RH',variable=var5, onvalue=1, offvalue=0, command=check_rh)
    c5.pack()
    c5.place(x=350,y=120)
    
    c6 = Checkbutton(janela, text='Rs',variable=var6, onvalue=1, offvalue=0, command=check_rs)
    c6.pack()
    c6.place(x=420,y=120)
    
    c7 = Checkbutton(janela, text='u2',variable=var7, onvalue=1, offvalue=0, command=check_u2)
    c7.pack()
    c7.place(x=480,y=120)
    
    Label(janela, text="Latitude", background="#abf321", foreground="#009", anchor=W).place(x=10, y=200, width=150)
    lt=Entry(janela)
    lt.place(x=10, y=220, width=200, height=20)
    
    Label(janela, text="Longitude", background="#abf321", foreground="#009", anchor=W).place(x=10, y=260, width=150)
    long=Entry(janela)
    long.place(x=10, y=280, width=200, height=20)
    
    mostra = Button(janela, text='Gerar Dados .csv', command=generate_file)
    mostra.pack()
    
    menu_bt = Button(janela, text='Voltar/Menur',command=menu)
    menu_bt.pack()







def menu():
    global janela
    janela.destroy()
    janela = Tk()
    label = Label(janela, text='Menu Principal')
    label.pack()
    menu_bt_criar = Button(janela, text='Criar Usuario',command=gerar_diario)
    menu_bt_edituser = Button(janela, text='Editar Usuario',command=gerar_mensal)
    menu_bt_criar.place(x=30,y=100)
    menu_bt_edituser.place(x=30,y=130)

    janela.geometry("300x300")
    janela.title("Menu Principal")

    janela.mainloop()


menu_bt_criar = Button(janela, text='Gerar Dados Diários',command=gerar_diario)
menu_bt_edituser = Button(janela, text='Gerar Dados Mensais',command=gerar_mensal)

menu_bt_criar.place(x=30,y=100)
menu_bt_edituser.place(x=30,y=130)

janela.geometry("300x300")
janela.title("Menu Principal")

janela.mainloop()