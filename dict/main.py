import tkinter
import tkinter.messagebox
import customtkinter
import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import date
from datetime import datetime
from tkcalendar import DateEntry
from lib.db import Database
from lib.animater import Animater
from lib.stairfunction import Stairfunction
from lib.map_drawing import Map_drawing
import re
import webbrowser
import babel.numbers     #neccessary for bundling with pyinstaller, otherwise tkcalendar doesnt work




##--------------------RECOMENDED/FUTURE ADDITIONS------------------------##
# Currently the export is limited to the actual max for that day. An interesting addition would be to make the user able to increase export/import over 
# the current maximum to see how an increase of capacity in the connections between sectors would allow for more even prices in Sweden
# For some reason the data for import/export and importmax/exportmax isnt consistant.
#  We found out that during certain dates the import was larger than the maximum import through a connection. for example SE2-NO3 on date 08-06-2022:16 


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
absolute_path = os.path.dirname(__file__)
PATH = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_default_color_theme(PATH+"/lib/dark_green.json")  # Themes: "blue" (standard), "green", "dark-blue"
          
production = []
consumption = []
export = []
export_max = []

intressanta_datum = ["Intressanta händelser", "19-04-2022:09", "08-06-2022:16", "20-06-2022:07", "29-07-2022:07"]
intressanta_datum_info = {"2022-04-19: 09-10": "Situation 1 var väldigt spännande på detta datum", "2022-06-08: 16-17": "Situation 2 var väldigt spännande på detta datum",
 "2022-06-20: 07-08":"Situation 3 var väldigt spännande på detta datum", "2022-07-29: 07-08": "Situation 4 var väldigt spännande på detta datum" }
years = ["2018", "2019", "2020", "2021", "2022"]
graphtypes = ["Spridningsdiagram","Linjediagram"]
dt1 = date(2018,1,1)        #First choosable date
dt2 = date(2022,7,31)       #Last choosable date
#button_fg_colors = [,'dodgerblue']
databases = [Database(year) for year in years]
 


class App(customtkinter.CTk):
    WIDTH = 1920
    HEIGHT = 1080
    
    def __init__(self, *args, **kwargs):
        omsimulatorn_activated = FALSE  #info picture is deactivated at startup

        #function for showing or not showing the information picture
        def omsimulatorn(): 
            nonlocal omsimulatorn_activated
            if(omsimulatorn_activated == FALSE):
                self.image_label_info.tkraise()         #raises the info-picture above the normal background picture
                self.frame.tkraise()                    #raises the left menu-frame above the info-picture
                omsimulatorn_activated = TRUE

            elif(omsimulatorn_activated == TRUE):
                self.image_label.tkraise()              #raises the background image above the info-image
                self.frame.tkraise()                    #raises the left menu-frame above the background image
                omsimulatorn_activated = FALSE    

        super().__init__(*args, **kwargs)

        #link to userguide
        def open_link():
            webbrowser.open_new("https://github.com/bengan520/Elsimulator")

        self.title("Elsimulator")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)
        self.resizable(True, True)
        self.state('zoomed')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # load image with PIL and convert to PhotoImage
        
        image = Image.open(PATH + "/resources/om_simulatorn.png").resize((self.WIDTH, self.HEIGHT))
        self.bg_image_info = ImageTk.PhotoImage(image)
        self.image_label_info = tkinter.Label(master=self, image=self.bg_image_info)
        self.image_label_info.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.arrow_image = self.load_image("/resources/pil.png", 20)

        image = Image.open(PATH + "/resources/startbild3.png").resize((self.WIDTH, self.HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


        self.frame = customtkinter.CTkFrame(master=self,
                                            width=300,
                                            height=App.HEIGHT,
                                            corner_radius=0,
                                            fg_color=("#252526")
                                            )
                                            
        self.frame.place(x=0, y=0, anchor=tkinter.NW)

        self.label_1 = customtkinter.CTkLabel(master=self.frame,
                                            width=200,
                                            height=60,
                                            fg_color=("#3c3c3c"),
                                            text_color="#d4d4d4",
                                            text="Elsimulator",
                                            text_font=("Roboto",25),
                                            corner_radius=8)
        self.label_1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.button_start1 = customtkinter.CTkButton(master=self.frame,
                                                    corner_radius=6,
                                                    width=200,
                                                    text="Simulator",
                                                    command=self.create_simulator)
        self.button_start1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.button_start2 = customtkinter.CTkButton(master=self.frame,
                                                    corner_radius=6,
                                                    width=200,
                                                    text="Grafer och animationer",
                                                    command=self.create_graphs)
        self.button_start2.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self.frame,
                                                text="Om simulatorn",
                                                corner_radius=6,
                                                command=omsimulatorn,
                                                width=200)
        self.button_2.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        link = customtkinter.CTkButton(self.frame,
                                        corner_radius=6,
                                        width=200,
                                        text="Källkod (länk)",
                                        command=open_link)
        link.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)
        
        
        
    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()
    



    

    def create_simulator(self):
        
        #clears and closes all figures 
        plt.cla()
        plt.close('all')
        

        #prodlist = SE1->SE4:sol,vind,vatten, kärnse3, ,värme,ospec
        prodmax_list = [19, 94, 1109, 372, 1927, 5342, 3000, 1805, 6882,5271, 8077, 2593, 345, 271, 680, 2804, 1545, 1, 2, 950, 582]
        #conslist max consumption for SE1->SE4 2021
        consmax_list = [3409, 8409, 16744, 4947]
    
        date = "date"
        currentsector = "SE1"
        prices = 0
        scheduled_func = None
        
        #Function to go back to the startmenu 
        def startmenu():
            window.destroy()

        #Function that highlights the clicked buttons when clicking on them, used on Production/consumptio/Export and SE1,SE2,SE3,SE4
        def click_color(my_button):
            std_col=["#72CF9F", "#11B384"] 
            if(my_button.text in ["Historik", "Egna värden"]):
                window.button_own.configure(fg_color=std_col)
                window.button_historic.configure(fg_color=std_col)    
            
            elif(my_button.text in ["Produktion","Konsumption","Export"]):
                for i in range(3):
                    tab_dict[i].configure(fg_color=std_col)      
            
            elif(my_button.text in ["SE1","SE2","SE3","SE4"]):
                for i in range(4):
                    tab_sectors[i].configure(fg_color=std_col)
             
            my_button.configure(fg_color=["#0E9670", "#0D8A66"])
            

        #Function that updates the values for the sliders when moving them.
        #If we are changing the import/export sliders we also show if we are importing or exporting
        def slider_event(value,k,e_list,pce,label_text):
            first_part = label_text[k].split(" ")[0]  
            value=round(value,1)
            if ("-" in label_text[k]) and value<0:
                e_list[k].configure(text=first_part + " exporterar "+str(abs(value))+" MWH/H")
            elif("-" in label_text[k]):
                e_list[k].configure(text=first_part + " importerar "+str(abs(value))+" MWH/H")
            else:
                e_list[k].configure(text=str(value)+" MWH/H")
            pce[k]=value
            

        #Function for when we release the mousebutton after having clicked on a slider. 
        # Set up this way so that we dont continiously run the code while changing slider value
        def slider_event_release():
            update_map()
            stairs() 


        #Function that updates the date using the calender  
        def update_date(var):
            year = cal.get_date().strftime("%Y")
            month = cal.get_date().strftime("%m")
            day = cal.get_date().strftime("%d")
            nonlocal date 
            date = (day+"-"+month+"-"+year+":00")
            window.simulate.configure(state=NORMAL)

       #Function to update the map
        def map_update():
            year = date[6:10]
            index = years.index(year)
            nonlocal prices

            #update values with the date that is picked
            prices = databases[index].get_values("Elpris", date)      
            wind  = databases[index].get_values("Vindkraft", date)
            water = databases[index].get_values("Vattenkraft", date)      
            nuclear = databases[index].get_values("Kärnkraft", date)[2]    
            ospec = databases[index].get_values("Ospec kraft", date) 
            heat = databases[index].get_values("Värmekraft", date)
            solar = databases[index].get_values("Solkraft", date)
            
            #update information window with the prices
            textvar=str("Datumet är: "+str(date)+"\nPriset i SE1 blir "+str(prices[0])+"\nPriset i SE2 blir "+str(prices[1])
                    +"\nPriset i SE3 blir "+str(prices[2])+"\nPriset i SE4 blir "+str(prices[3]))
            window.label_info_1.configure(text=textvar)


           #Updates values with the date that is picked and put them in their respective lists
            global production
            global consumption
            global export
            global export_max

            production = [*solar, *wind, nuclear, *water, *heat, *ospec]
            consumption = databases[index].get_values("Konsumption",date)
            export = databases[index].get_values_export(date)
            export_max = databases[index].get_values_export_max(date)
            production_label = databases[index].get_column_name(0)
            consumption_label = databases[index].get_column_name(1)
            export_label = databases[index].get_column_name(2)
            
            #draws up the production/consumption and exports with the draw_pce Function
            draw_pce(production, frame_production, production_label, prodmax_list)
            draw_pce(consumption, frame_consumption, consumption_label, consmax_list)
            draw_pce(export,frame_export, export_label, export_max)

        # function for picking preset values that also updates the date in the calender
        def pick_preset(value):
            nonlocal date
            date = value
            day=date[0:2]
            month=date[3:5]
            year=date[6:10]
            cal_date=year+"-"+month+"-"+day
            cal.set_date(cal_date)
            window.simulate.configure(state=NORMAL)

        #Function to pick the sector we want to draw our stairfunctions for. 
        #If we have simulated allready we draw up the stairfunction for that sector
        def pick_sector(sector,button):
            
            nonlocal currentsector
            if(sector == 0):
                currentsector = "SE1"
                
            elif(sector == 1):
                currentsector = "SE2"
                
            elif(sector == 2):
                currentsector = "SE3"
                
            elif(sector == 3):
                currentsector = "SE4"
                
            click_color(button)
            if export_max != []:
                stairs()

        #============Functions to change the production in the different electricity sectors.============
        
        #function to draw the production/consumption or exports with ability to change to the max possible values for that hour.
        def draw_pce(pce, frame_pce, label_text,pce_max):
            
            #Function on_press and on_relase work together to block slider_event_release untill we have released the button.
            def on_press(event):
                try:
                    tkinter.Tk.after_cancel(scheduled_func)
                except NameError:
                    pass
                
            def on_release(event):
                scheduled_func = self.after(10,slider_event_release)
            
            
            #Clears the all the widgets in Production/Consumption/Export
            for widget in frame_pce.winfo_children():
                widget.destroy()

            tab_n = len(pce)
            e_list=[]
            # Draws up the sliders for the currently chosen date of either Production, consumption or export.
            for j in range(tab_n):
                if("-" in label_text[j]):
                    if (int(pce_max[2*j]) ==0) and (int(pce_max[2*j+1])==0):
                        e=customtkinter.CTkSlider(master=frame_pce,from_ = -1, to =1,command=lambda val, list=e_list,k=j:slider_event(val,k,list,pce,label_text))   
                    else:                       
                        e=customtkinter.CTkSlider(master=frame_pce,from_ = -pce_max[2*j], to =pce_max[2*j+1],command=lambda val, list=e_list,k=j:slider_event(val,k,list,pce,label_text))  
                    
                    e.set(round(float(pce[j]),1))
                    
                else:        
                    e=customtkinter.CTkSlider(master=frame_pce,from_ = 0, to =pce_max[j], command=lambda val, list=e_list,k=j:slider_event(val,k,list,pce,label_text))
                    e.set(round(float(pce[j]),1))
                
                e.canvas.bind("<ButtonPress-1>",on_press)
                e.canvas.bind("<ButtonRelease-1>",on_release)
            
                # Removes the years from the strings
                for year in years:
                    label_text[j] = re.sub(year, "", label_text[j])

                #label that explains what the slider correlates too
                e2 = customtkinter.CTkLabel(master=frame_pce,
                                        text_color="#d4d4d4",
                                        text=label_text[j].replace("-","till"))
                e3 = customtkinter.CTkLabel(master=frame_pce,
                                        text_color="#d4d4d4",
                                        text=str(e.get())+" MWH/H")

                first_part = label_text[j].split(" ")[0]  
                #checks if we are are looking at exports and if we are importing or exporting from chosen sector.
                if ("-" in label_text[j]) and pce[j]<0:
                    e3.configure(text= first_part + " exporterar "+str(abs(e.get()))+" MWH/H")
                elif("-" in label_text[j]):
                    e3.configure(text=first_part + " importerar "+str(abs(e.get()))+" MWH/H")
                e_list.append(e3)
                e.grid(row=j,column=1)
                e2.grid(row=j,column=0)
                e3.grid(row=j,column=2)
            
        #Function that displays either Production, Consumption or Export.
        def show_pce(val, button):
            #Tries to forget all the grids
            try:
                frame_production.grid_forget()       
            except:
                pass
            
            try:
                frame_consumption.grid_forget()
            except:
                pass

            try:
                frame_export.grid_forget()
            except:
                pass
            
            #places the grid we want
            if val==0:
                frame_production.grid(row=2,column=0)
            elif val==1:
                frame_consumption.grid(row=2,column=0)
            elif val==2:
                frame_export.grid(row=2,column=0) 
            
            click_color(button)
        
        

        #Function that runs the simulation
        #first updates the arrows on the map
        #then we add the buttons for previous and next hour and disables them if there is no next/previous hour.
        #Ends with running the stair function
        def simulate():
            
            map_update()
            update_map()
            global export
            
            for j in range(tab_n):
                tab_dict[j].configure(state=NORMAL)
            
            window.next_hour_button = customtkinter.CTkButton(master=frame_simulate,
                                                    text=">",
                                                    command=lambda:next_hour())
            window.next_hour_button.grid(row=0, column=2, sticky='sw')
            
            window.previous_hour_button = customtkinter.CTkButton(master=frame_simulate,
                                                    text="<",
                                                    command=lambda:previous_hour())
            window.previous_hour_button.grid(row=0,column=0,sticky='sw')
    
            if(date[-2:]=="00"):
                window.previous_hour_button.configure(state=tkinter.DISABLED)
            elif(date[-2:]=="23"):
                window.next_hour_button.configure(state=tkinter.DISABLED)
            else:
                window.previous_hour_button.configure(state=tkinter.NORMAL)
                window.next_hour_button.configure(state=tkinter.NORMAL)
            stairs()

        
        #Function to update the map. Creates a map_drawing object and places it over the current map
        def update_map():
            new_map=Map_drawing.draw_map(window.map_label, window.bg_map, window.frame_left_U, export, export_max)
            new_map.place(x=0, y=0, anchor=NW)
                 
        #Function that initilizes the drawing of price curves                                   
        def stairs():
            #Creates starifunction object
            stairfig = Stairfunction.draw_graph(production, consumption, export_max,export,currentsector,prices)
            
            #Clears the frame containing the stairfunction to make room for a new stairfunction
            for widget in window.frame_center_MID.winfo_children():
                widget.destroy()

            #Sets the size of the stairfunction and places it)
            plt.figure(dpi=100)
            canvas = FigureCanvasTkAgg(stairfig,master=window.frame_center_MID)
            canvas.draw()
            #toolbar = NavigationToolbar2Tk(canvas, window.frame_center_MID)
            #toolbar.update()
            canvas.get_tk_widget().pack()
            
        #Function that changes to next hour and runs simulate(). 
        def next_hour():
            nonlocal date
            hour=date[-2:]
            new_hour = int(hour)+1
            if(new_hour<10):
                new_hour="0"+str(new_hour)
            new_hour=":"+str(new_hour)
            new_date = date.split(":",1)[0]
            date=(new_date+new_hour)
            simulate()

        #Function that changes to previous hour and runs simulate(). 
        def previous_hour():
            nonlocal date
            hour=date[-2:]
            new_hour = int(hour)-1
            if(new_hour<10):
                new_hour="0"+str(new_hour)
            new_hour=":"+str(new_hour)
            new_date = date.split(":",1)[0]
            date=(new_date+new_hour)
            simulate()
               
        # This is the start of the  GUI and its buildingblocks
        
        self.update()
        window=customtkinter.CTkFrame(master=self,
                                    fg_color="#252526",
                                    width=self.winfo_width(),
                                    height=self.winfo_height())
        window.grid_propagate(False)
        window.place(relx = 0.5, rely = 0.5, anchor=CENTER)

        window.grid_columnconfigure(0, weight=20)
        window.grid_columnconfigure(1, weight=20)
        window.grid_columnconfigure(2, weight=15)
        window.grid_rowconfigure(1, weight=7)

        #The top frame that spans the entire screen from left to right.
        window.frame_top = customtkinter.CTkFrame(master=window,
                                                corner_radius=0,fg_color="#3c3c3c",height=30)
        window.frame_top.grid(row=0, column=0, columnspan=3, sticky="nswe")
        window.frame_top.grid_propagate(False)

        #the upper left frame is introduced and placed in the grid
        window.frame_left_U = customtkinter.CTkFrame(master=window,
                                                 corner_radius=0)
        window.frame_left_U.grid(row=1, column=0, sticky="nswe")

        #the upper middle frame is introduced and placed in the grid
        window.frame_center_U = customtkinter.CTkFrame(master=window,
                                                    fg_color="#252526",
                                                    corner_radius=0) 
        window.frame_center_U.grid(row=1, column=1, sticky= "nswe")


        #the upper right frame is introduced and placed in the grid
        window.frame_right_U = customtkinter.CTkFrame(master=window,
                                                    fg_color="#252526",
                                                    corner_radius=0) 
        window.frame_right_U.grid(row=1, column=2, sticky="nswe")

        #the lower left frame is introduced and placed in the grid
        window.frame_left_L = customtkinter.CTkFrame(master=window,
                                                    corner_radius=0)
        window.frame_left_L.grid(row=2, column=0, sticky="nswe")

        #the lower middle frame is introduced and placed in the grid
        window.frame_center_L = customtkinter.CTkFrame(master=window,
                                                    corner_radius=0) 
        window.frame_center_L.grid(row=2, column=1, sticky= "nswe")
        
        #the lower right frame is introduced and placed in the grid
        window.frame_right_L = customtkinter.CTkFrame(master=window,
                                                    fg_color="#252526",
                                                    corner_radius=0) 
        window.frame_right_L.grid(row=2, column=2, sticky="nswe")
        
        #locks the size of the frames in the grid
        window.frame_left_U.grid_propagate(False)
        window.frame_center_U.grid_propagate(False)
        window.frame_right_U.grid_propagate(False)
        window.frame_left_L.grid_propagate(False)
        window.frame_center_L.grid_propagate(False)
        window.frame_right_L.grid_propagate(False)
        


        # ============ TOP FRAME ============
        #Contains one button that takes us back to the startpage
        window.button_startmeny = customtkinter.CTkButton(master=window.frame_top,
                                                              width=40,
                                                              height=14,
                                                              corner_radius=4,
                                                              text="Startmeny",
                                                              fg_color="#3c3c3c",
                                                              text_color="#d4d4d4",
                                                              image = self.arrow_image,
                                                              compound="left",
                                                              command=lambda: startmenu())
        window.button_startmeny.grid(row=1, column=0,columnspan=1,pady=0,padx=0,sticky="w")

        # ============ UPPER LEFT FRAME ============
        #Contains a map of sweden and the connecting electricity sectors.
        window.frame_left_U.update()
        map = Image.open(PATH + "/resources/elkarta.png").resize((window.frame_left_U.winfo_width(),window.frame_left_U.winfo_height()))
        window.bg_map = ImageTk.PhotoImage(map)

        window.map_label = customtkinter.CTkLabel(master=window.frame_left_U, 
                                            image=window.bg_map,
                                            fg_color="#3c3c3c"
                                            )
        window.map_label.place(x=0, y=0, anchor=NW)
  
        # ============ LOWER LEFT FRAME ============

        #ERROR/INFO MESSAGEBOX isnt really used right now. Can be a future feature. 
        window.frame_left_L.update()
        window.error_box = customtkinter.CTkLabel(master=window.frame_left_L,
                                                   text_color="#d4d4d4",
                                                   text="I detta fönster kommer info - och felmeddelanden visas",
                                                   anchor=CENTER,
                                                   width=window.frame_left_L.winfo_width()-1,
                                                   height=window.frame_left_L.winfo_height(),
                                                   fg_color=("white", "gray38")
                                                   )
        window.error_box.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


        
        # ============ UPPER CENTER FRAME ============
        #Contains the buttons for changing sectors.

        #configure columnsize etc for the upper centerframe
        window.frame_center_U.grid_columnconfigure(0, weight=1)
        window.frame_center_U.grid_columnconfigure(1, weight=1)
        window.frame_center_U.grid_columnconfigure(2, weight=1)
        window.frame_center_U.grid_columnconfigure(3, weight=1)
        tab_list = ["SE1","SE2","SE3","SE4"]
        tab_n = 4
        tab_sectors={}
        for j in range(tab_n):
            tab_sectors[j]=customtkinter.CTkButton(master=window.frame_center_U,
                                                text=tab_list[j],
                                                command=lambda k=j:pick_sector(k, tab_sectors[k]))
            tab_sectors[j].grid(row=0,column=j)
        
        
        # ============ MIDDLE CENTER FRAME ============
        #A frame inside the upper middle frame that contains the price graph
        window.frame_center_MID = customtkinter.CTkFrame(master=window.frame_center_U,
                                                        fg_color="#252526")

        window.frame_center_MID.place(relx=0.5, rely=0.95, anchor=tkinter.S)
       
        # ============ LOWER CENTER FRAME ============
        #Contains an infobox that writes out the date and hour and the price in the different sectors when running simulate()

        window.frame_center_L.update()
        window.label_info_1 = customtkinter.CTkLabel(master=window.frame_center_L,
                                                   text_color="#d4d4d4",
                                                   text="Resultat",
                                                   width=window.frame_center_L.winfo_width()-1,
                                                   height=window.frame_center_L.winfo_height(),
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   anchor=CENTER
                                                   )
        window.label_info_1.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


        # ============ UPPER RIGHT FRAME ============
        #Used to be the middle frame in a previous version(which explains the name of the frame). Is now placed on the top.
        #Contains everything on the right side of the simulator.
        
        #Creates the frame, sets it size and places it.
        window.frame_right_mid = customtkinter.CTkFrame(master=window.frame_right_U,
                                                        fg_color="#252526",
                                                        width=window.frame_right_U.winfo_width(),
                                                        height=100)
        window.frame_right_mid.grid_propagate(False)
        window.frame_right_mid.grid(row=1,column=0)
        window.frame_right_mid.grid_columnconfigure(0, weight=1)
        window.frame_right_mid.grid_columnconfigure(1, weight=1)
        window.frame_right_mid.grid_columnconfigure(2, weight=1)
        window.frame_right_mid.update()
    
        #Optionmenu that allows us to pick from preset dates 
        window.preset_dates = customtkinter.CTkOptionMenu(master=window.frame_right_mid,
                                                       values=intressanta_datum,
                                                       command=pick_preset)
        window.preset_dates.grid(row=0, column=0)
        window.preset_dates.update()
        
        #Calender to pick date
        cal = DateEntry(window.frame_right_mid, maxdate=dt2, mindate=dt1 ,width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2021,locale='en_UK',date_pattern='yyyy-MM-dd')
        cal.grid(row=0,column=1)
        cal.bind("<<DateEntrySelected>>",update_date)
        

        tab_list = ["Produktion","Konsumption","Export"]
        tab_n = 3
        tab_dict = {}
        #Buttons for showing production/consumption/exports
        for j in range(tab_n):
            tab_dict[j]=customtkinter.CTkButton(master=window.frame_right_mid,
                                            text=tab_list[j],
                                            state=DISABLED,
                                            command=lambda k=j:show_pce(k, tab_dict[k]))
            tab_dict[j].grid(row=1,column=j,pady=10)

        #frames for consumption/production/export sliders
        frame_consumption = customtkinter.CTkFrame(master=window.frame_right_U,
                                                fg_color="#252526")    
        frame_production = customtkinter.CTkFrame(master=window.frame_right_U,
                                                fg_color="#252526")
        frame_export = customtkinter.CTkFrame(master=window.frame_right_U,
                                            fg_color="#252526")
       
            

        frame_simulate = customtkinter.CTkFrame(master=window.frame_right_U)
        frame_simulate.grid(row=4, column=0)
        window.simulate = customtkinter.CTkButton(master=frame_simulate,
                                                    text="Simulera",
                                                    command=lambda : simulate())
        window.simulate.grid(row=0, column=1, sticky='sw')
        
        
        #default values
        window.simulate.configure(state=DISABLED)
        
        


    def create_graphs(self):
        #clears and closes all figures 
        plt.cla()
        plt.close('all')
        
        
        #declares parameters
        nbr_figures = 0
        nbr_y_buttons = 0

        x_axis_label = 0
        x_axis = 0

        y_axis_label_1 = 0
        y_axis_1 = 0
        
        y_axis_label_2 = 0
        y_axis_2 = 0
        
        y_axis_label_3 = 0
        y_axis_3 = 0
        
        y_axis_label_4 = 0
        y_axis_4 = 0
       
        y_axis_label_5 = 0
        y_axis_5 = 0

        y_axis_label_6 = 0
        y_axis_6 = 0

        window = self
        
        #Takes what year was chosen and fills the corresponding optionmenu with the columns for that year
        def optionmenuyear_callback(choice,name):
            index = years.index(choice)
            
            if(name=="optionmenux"):
                window.optionmenux.configure(values=databases[index].get_columns())
                window.optionmenux.set(databases[index].get_columns()[0])

            if(name=="optionmenuy1"):
                window.optionmenuy1.configure(values=databases[index].get_columns())
                window.optionmenuy1.set(databases[index].get_columns()[0])

            if(name=="optionmenuy2"):
                window.optionmenuy2.configure(values=databases[index].get_columns())
                window.optionmenuy2.set(databases[index].get_columns()[0])    

            if(name=="optionmenuy3"):
                window.optionmenuy3.configure(values=databases[index].get_columns())
                window.optionmenuy3.set(databases[index].get_columns()[0])     
        
            if(name=="optionmenuy4"):
                window.optionmenuy4.configure(values=databases[index].get_columns())
                window.optionmenuy4.set(databases[index].get_columns()[0])

            if(name=="optionmenuy5"):
                window.optionmenuy5.configure(values=databases[index].get_columns())
                window.optionmenuy5.set(databases[index].get_columns()[0])

            if(name=="optionmenuy6"):
                window.optionmenuy6.configure(values=databases[index].get_columns())
                window.optionmenuy6.set(databases[index].get_columns()[0])

        #Takes the choice of column and puts the data for the whole year in x-axis
        def optionmenux_callback(choice):
            nonlocal x_axis
            nonlocal x_axis_label

            
            index = years.index(window.optionmenuxyear.get())
            x_axis_label = databases[index].get_label(choice)      #sets the x-axis label to the choosed option
            x_axis = databases[index].get_values_year(choice)  #sets the x-axis data to the choosed option
            
        #Takes the choice of column and puts the data for the whole year in the corresponding y-axis
        def optionmenuy_callback(choice,name):
            nonlocal x_axis

            nonlocal y_axis_label_1
            nonlocal y_axis_1

            nonlocal y_axis_label_2
            nonlocal y_axis_2

            nonlocal y_axis_label_3
            nonlocal y_axis_3

            nonlocal y_axis_label_4
            nonlocal y_axis_4

            nonlocal y_axis_label_5
            nonlocal y_axis_5

            nonlocal y_axis_label_6
            nonlocal y_axis_6

            #initializes the x_axis optionmenu so that we can use x_axis to resize the axeses
            optionmenux_callback(str(window.optionmenux.get()))
            if(name=="optionmenuy1"):
                
                index = years.index(window.optionmenuyyear1.get())
                y_axis_label_1 = databases[index].get_label(choice)       #sets the y-axis label to the choosed option
                y_axis_1 = databases[index].get_values_year(choice)  #sets the y-axis data to the choosed option
                
            if(name=="optionmenuy2"):
                index = years.index(window.optionmenuyyear2.get())
                y_axis_label_2 = databases[index].get_label(choice)       #sets the y-axis label to the choosed option
                y_axis_2 = databases[index].get_values_year(choice)  #sets the y-axis data to the choosed option
                # Checks that the axes to be plotted are the same size, otherwise, we resize them
                resize_axes(x_axis,y_axis_2,2)

            if(name=="optionmenuy3"):
                index = years.index(window.optionmenuyyear3.get())
                y_axis_label_3 = databases[index].get_label(choice)       #sets the y-axis label to the choosed option
                y_axis_3 = databases[index].get_values_year(choice)  #sets the y-axis data to the choosed option
                # Checks that the axes to be plotted are the same size, otherwise, we resize them
                resize_axes(x_axis,y_axis_3,3)
            if(name=="optionmenuy4"):
                index = years.index(window.optionmenuyyear4.get())
                y_axis_label_4 = databases[index].get_label(choice)       #sets the y-axis label to the choosed option
                y_axis_4 = databases[index].get_values_year(choice)  #sets the y-axis data to the choosed option
                # Checks that the axes to be plotted are the same size, otherwise, we resize them
                resize_axes(x_axis,y_axis_4,4)
            if(name=="optionmenuy5"):
                index = years.index(window.optionmenuyyear5.get())
                y_axis_label_5 = databases[index].get_label(choice)       #sets the y-axis label to the choosed option
                y_axis_5 = databases[index].get_values_year(choice)  #sets the y-axis data to the choosed option
                # Checks that the axes to be plotted are the same size, otherwise, we resize them
                resize_axes(x_axis,y_axis_5,5)
            if(name=="optionmenuy6"):
                index = years.index(window.optionmenuyyear6.get())
                y_axis_label_6 = databases[index].get_label(choice)       #sets the y-axis label to the choosed option
                y_axis_6 = databases[index].get_values_year(choice)  #sets the y-axis data to the choosed option     
                # Checks that the axes to be plotted are the same size, otherwise, we resize them
                resize_axes(x_axis,y_axis_6,6)
        #enables the add line button if "linjediagram" is chosen and there is room for more
        def optionmenu_callback_graph_type(choice):
            if(choice == "Spridningsdiagram"):
                window.button_add_line.configure(state=tkinter.DISABLED)
            
            if(choice == "Linjediagram"):
                
                if(nbr_y_buttons < 5):
                    window.button_add_line.configure(state=tkinter.NORMAL)
       
        #Removes the last added y-axis optionmenus
        def remove_line():
            nonlocal nbr_y_buttons
            

            if(nbr_y_buttons == 1):
                window.optionmenuyyear2.destroy()
                window.optionmenuy2.destroy()
                window.ylabel2.destroy()
                nbr_y_buttons -=1   #number of optionmenus has decreased by 1

                window.button_remove_line.configure(state=tkinter.DISABLED)      #deactivates remove button

            if(nbr_y_buttons == 2):
                window.optionmenuyyear3.destroy()
                window.optionmenuy3.destroy()
                window.ylabel3.destroy()
                nbr_y_buttons -=1   #number of optionmenus has decreased by 1

            if(nbr_y_buttons == 3):
                window.optionmenuyyear4.destroy()
                window.optionmenuy4.destroy()
                window.ylabel4.destroy()
                nbr_y_buttons -=1   #number of optionmenus has decreased by 1

                

            if(nbr_y_buttons == 4):
                window.optionmenuyyear5.destroy()
                window.optionmenuy5.destroy()
                window.ylabel5.destroy()
                nbr_y_buttons -=1   #number of optionmenus has decreased by 1


            if(nbr_y_buttons == 5):
                window.optionmenuyyear6.destroy()
                window.optionmenuy6.destroy()
                window.ylabel6.destroy()
                nbr_y_buttons -=1   #number of optionmenus has decreased by 1 

            #if there is room for more optionmenus, enables the "add new line" button again
            if(nbr_y_buttons<5):
                window.button_add_line.configure(state=tkinter.NORMAL)  

        #Adds another y-axis line to plot by creating 2 new optionmenus for the y-axis
        def add_line():

            nonlocal nbr_y_buttons

            #if an optionmenu has been removed this makes it possible to add a line again
            if(nbr_y_buttons<5):        
                window.button_add_line.configure(state=tkinter.NORMAL)

            #creates new y-axis optionmenus
            if(nbr_y_buttons == 0):
                
                window.ylabel2 = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Data 2 på y-axel:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
                window.ylabel2.grid(row=2, column=0, columnspan=1, pady=2, padx=10, sticky="nw")

                window.optionmenuyyear2 = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                         values=years,
                                                         command=lambda x: optionmenuyear_callback(x,"optionmenuy2"))
                                                         
                window.optionmenuyyear2.grid(row=2, column=1, columnspan=1, pady=2, padx=2, sticky="nw")
                

                window.optionmenuy2= customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                             values=databases[0].get_columns(),
                                                             command=lambda x: optionmenuy_callback(x,"optionmenuy2"))
                window.optionmenuy2.grid(row=2, column=2, columnspan=1, pady=2, padx=2, sticky="nw")
                window.optionmenuy2.set(databases[0].get_columns()[0])   #initializes menu

                window.button_remove_line.configure(state=tkinter.NORMAL)      #activates remove button

                nbr_y_buttons +=1       #increases the number of optionmenus

            #creates the third y-axis optionmenu and the corresponding remove button
            elif(nbr_y_buttons == 1):
                
                window.ylabel3 = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Data 3 på y-axel:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
                window.ylabel3.grid(row=3, column=0, columnspan=1, pady=2, padx=10, sticky="nw")

                window.optionmenuyyear3 = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                         values=years,
                                                         command=lambda x: optionmenuyear_callback(x,"optionmenuy3"))
                                                         
                window.optionmenuyyear3.grid(row=3, column=1, columnspan=1, pady=2, padx=2, sticky="nw")

                window.optionmenuy3= customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                             values=databases[0].get_columns(),
                                                             command=lambda x: optionmenuy_callback(x,"optionmenuy3"))
                window.optionmenuy3.grid(row=3, column=2, columnspan=1, pady=2, padx=2, sticky="nw")
                window.optionmenuy3.set(databases[0].get_columns()[0])   #initializes menu

                nbr_y_buttons +=1       #increases the number of optionmenus

            #creates the fourth y-axis optionmenu and the corresponding remove button
            elif(nbr_y_buttons == 2):
                
                window.ylabel4 = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Data 4 på y-axel:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
                window.ylabel4.grid(row=4, column=0, columnspan=1, pady=2, padx=10, sticky="nw")

                window.optionmenuyyear4 = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                         values=years,
                                                         command=lambda x: optionmenuyear_callback(x,"optionmenuy4"))
                                                         
                window.optionmenuyyear4.grid(row=4, column=1, columnspan=1, pady=2, padx=2, sticky="nw")

                window.optionmenuy4= customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                             values=databases[0].get_columns(),
                                                             command=lambda x: optionmenuy_callback(x,"optionmenuy4"))
                window.optionmenuy4.grid(row=4, column=2, columnspan=1, pady=2, padx=2, sticky="nw")
                window.optionmenuy4.set(databases[0].get_columns()[0])   #initializes menu

                nbr_y_buttons +=1       #increases the number of optionmenus

            #creates the fifth y-axis optionmenu and the corresponding remove button
            elif(nbr_y_buttons == 3):
                
                window.ylabel5 = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Data 5 på y-axel:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
                window.ylabel5.grid(row=5, column=0, columnspan=1, pady=2, padx=10, sticky="nw")

                window.optionmenuyyear5 = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                         values=years,
                                                         command=lambda x: optionmenuyear_callback(x,"optionmenuy5"))
                                                         
                window.optionmenuyyear5.grid(row=5, column=1, columnspan=1, pady=2, padx=2, sticky="nw")

                window.optionmenuy5= customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                             values=databases[0].get_columns(),
                                                             command=lambda x: optionmenuy_callback(x,"optionmenuy5"))
                window.optionmenuy5.grid(row=5, column=2, columnspan=1, pady=2, padx=2, sticky="nw")
                window.optionmenuy5.set(databases[0].get_columns()[0])   #initializes menu
                
                nbr_y_buttons +=1       #increases the number of optionmenus

            #creates the sixth y-axis optionmenu and the corresponding remove button
            elif(nbr_y_buttons == 4):
                
                window.ylabel6 = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Data 6 på y-axel:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
                window.ylabel6.grid(row=6, column=0, columnspan=1, pady=2, padx=10, sticky="nw")

                window.optionmenuyyear6 = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                         values=years,
                                                         command=lambda x: optionmenuyear_callback(x,"optionmenuy6"))
                                                         
                window.optionmenuyyear6.grid(row=6, column=1, columnspan=1, pady=2, padx=2, sticky="nw")

                window.optionmenuy6= customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                             values=databases[0].get_columns(),
                                                             command=lambda x: optionmenuy_callback(x,"optionmenuy6"))
                window.optionmenuy6.grid(row=6, column=2, columnspan=1, pady=2, padx=2, sticky="nw")
                window.optionmenuy6.set(databases[0].get_columns()[0])   #initializes menu
                
                nbr_y_buttons +=1       #increases the number of optionmenus

                window.button_add_line.configure(state=tkinter.DISABLED)       #disables the "add another line" button since we now have 6 different y-axis optionmenus which is the maximum

        def resize_axes(x,y,yname):
            nonlocal y_axis_1
            nonlocal y_axis_2
            nonlocal y_axis_3
            nonlocal y_axis_4
            nonlocal y_axis_5
            nonlocal y_axis_6
            nonlocal x_axis

            if(len(x) > len(y)):
                for i in range(len(x) - len(y)):
                    x = x.drop(x.index[-1])
                x_axis = x

            elif(len(x) < len(y)):
                for i in range(len(y) - len(x)):
                    y = y.drop(y.index[-1])

                if(yname==1):
                    y_axis_1 = y
                if(yname==2):
                    y_axis_2 = y
                if(yname==3):
                    y_axis_3 = y
                if(yname==4):
                    y_axis_4 = y
                if(yname==5):
                    y_axis_5 = y
                if(yname==6):
                    y_axis_6 = y

        #Creates the line and scatter plots
        def graph_maker():
            #declares the parameters not local for this function
            nonlocal nbr_y_buttons
            nonlocal y_axis_label_1
            nonlocal y_axis_label_2
            nonlocal y_axis_label_3
            nonlocal y_axis_label_4
            nonlocal y_axis_label_5
            nonlocal y_axis_label_6
            nonlocal y_axis_1
            nonlocal y_axis_2
            nonlocal y_axis_3
            nonlocal y_axis_4
            nonlocal y_axis_5
            nonlocal y_axis_6
            nonlocal x_axis_label
            nonlocal x_axis
            nonlocal nbr_figures
            
            #initializes the optionmenus without having to click them
            optionmenux_callback(str(window.optionmenux.get()))
            optionmenuy_callback(str(window.optionmenuy1.get()),"optionmenuy1")

            #gets what type of graph to plot
            type = window.optionmenu_graph_type.get()
          

           
            # Checks that the axes to be plotted are the same size, otherwise, we resize them
            resize_axes(x_axis,y_axis_1,1)
            

            #plots a scatterplot       
            if(type == "Spridningsdiagram"):
                
                nbr_figures = nbr_figures + 1   #counts number of figures to give the plot the correct number
                plt.figure(nbr_figures)
                plt.scatter(x_axis,y_axis_1, c="blue")
                plt.title(type)
                plt.xlabel(x_axis_label)
                plt.ylabel(y_axis_label_1)
                plt.show()

            #plots a line graph with the correct number of lines chosen
            if(type == "Linjediagram"):
                
                if(nbr_y_buttons == 0):     #checks how many lines the plot shall have

                    nbr_figures = nbr_figures + 1   #counts number of figures to give the plot the correct number
                    plt.figure(nbr_figures)
                    plt.plot(x_axis,y_axis_1)
                    plt.xlabel(x_axis_label)
                    plt.ylabel(y_axis_label_1)
                    plt.show()
                    
                
                if(nbr_y_buttons == 1):     #checks how many lines the plot shall have
                
                    
                    nbr_figures = nbr_figures + 1   #counts number of figures to give the plot the correct number
                    plt.figure(nbr_figures)
                    plt.plot(x_axis,y_axis_1, label = y_axis_label_1)
                    plt.plot(x_axis,y_axis_2, label = y_axis_label_2)
                    plt.xlabel(x_axis_label)
                    #plt.ylabel("/MW")
                    plt.legend()
                    plt.show()

                if(nbr_y_buttons == 2):     #checks how many lines the plot shall have
                    

                    nbr_figures = nbr_figures + 1   #counts number of figures to give the plot the correct number
                    plt.figure(nbr_figures)
                    plt.plot(x_axis,y_axis_1, label = y_axis_label_1)
                    plt.plot(x_axis,y_axis_2, label = y_axis_label_2)
                    plt.plot(x_axis,y_axis_3, label = y_axis_label_3)
                    plt.xlabel(x_axis_label)
                    #plt.ylabel("/MW")
                    plt.legend()
                    plt.show()

                if(nbr_y_buttons == 3):     #checks how many lines the plot shall have
                    

                    nbr_figures = nbr_figures + 1   #counts number of figures to give the plot the correct number
                    plt.figure(nbr_figures)
                    plt.plot(x_axis,y_axis_1, label = y_axis_label_1)
                    plt.plot(x_axis,y_axis_2, label = y_axis_label_2)
                    plt.plot(x_axis,y_axis_3, label = y_axis_label_3)
                    plt.plot(x_axis,y_axis_4, label = y_axis_label_4)
                    plt.xlabel(x_axis_label)
                    #plt.ylabel("/MW")
                    plt.legend()
                    plt.show()

                if(nbr_y_buttons == 4):     #checks how many lines the plot shall have
                    
                   
                    nbr_figures = nbr_figures + 1   #counts number of figures to give the plot the correct number
                    plt.figure(nbr_figures)
                    plt.plot(x_axis,y_axis_1, label = y_axis_label_1)
                    plt.plot(x_axis,y_axis_2, label = y_axis_label_2)
                    plt.plot(x_axis,y_axis_3, label = y_axis_label_3)
                    plt.plot(x_axis,y_axis_4, label = y_axis_label_4)
                    plt.plot(x_axis,y_axis_5, label = y_axis_label_5)
                    plt.xlabel(x_axis_label)
                    #plt.ylabel("/MW")
                    plt.legend()
                    plt.show()    
        

                if(nbr_y_buttons == 5):     #checks how many lines the plot shall have
                    
                    
                    nbr_figures = nbr_figures + 1   #counts number of figures to give the plot the correct number
                    plt.figure(nbr_figures)
                    plt.plot(x_axis,y_axis_1, label = y_axis_label_1)
                    plt.plot(x_axis,y_axis_2, label = y_axis_label_2)
                    plt.plot(x_axis,y_axis_3, label = y_axis_label_3)
                    plt.plot(x_axis,y_axis_4, label = y_axis_label_4)
                    plt.plot(x_axis,y_axis_5, label = y_axis_label_5)
                    plt.plot(x_axis,y_axis_6, label = y_axis_label_6)
                    plt.xlabel(x_axis_label)
                    #plt.ylabel("/MW")
                    plt.legend()
                    plt.show()    
        
       
        #Creates a animater object and sends the info needed from the interface to create the animation
        def animations(export):
            nonlocal nbr_figures
            checkboxlist = [window.checkbox_pie.get(),window.checkbox_elpris.get(),window.checkbox_prod.get()]
            date = cal.get_date().strftime("%d-%m-%Y") + ":00"
            year = cal.get_date().strftime("%Y")
            index = years.index(year)
            

            if(export == 0):
                window.button_choose_graph.configure(state=tkinter.DISABLED) #prevents making a new graph while animation is running
                nbr_figures += 1
                animation = Animater(checkboxlist,date,databases[index],nbr_figures,window)
                animation.animate(0,"","")
                
                

            elif(export == 1):
                animation = Animater(checkboxlist,date,databases[index],nbr_figures,window)
                name_dialog = customtkinter.CTkInputDialog(master=None, text="Döp din fil", title="Exportera GIF animation")
                name = name_dialog.get_input()
                fps_dialog = customtkinter.CTkInputDialog(master=None, text="Välj fps (1 fps - 15 fps )", title="Välj fps")
                fps = fps_dialog.get_input()
                if(name == ""):
                    tkinter.messagebox.showerror("error","Ogiltigt val av namn")
                elif(name == None):
                    pass
                
                elif(float(fps) < 1 or float(fps) > 15):
                    tkinter.messagebox.showerror("error","Ogiltigt val av fps, välj mellan 1 och 15.")
                else:
                    animation.animate(export,name,fps)
                    
        
        #creates a csv file with the data chosen in the optionmenus
        def create_csv():
            col_num = nbr_y_buttons + 2
            column_names = [x_axis_label,y_axis_label_1,y_axis_label_2,y_axis_label_3,y_axis_label_4,y_axis_label_5,y_axis_label_6]
            column_names = column_names[:col_num]
            datalist = [x_axis,y_axis_1,y_axis_2,y_axis_3,y_axis_4,y_axis_5,y_axis_6]
            datalist = datalist[:col_num]
            name_dialog = customtkinter.CTkInputDialog(master=None, text="Döp din fil", title="Spara data i en CSV fil")
            filename = name_dialog.get_input()
            if(filename == ""):
                    tkinter.messagebox.showerror("error","Ogiltigt val av namn")
            elif(filename == None):
                    pass
            else:
                databases[0].create_csv(filename,column_names,datalist)
        #changes between the graph and animate tabs
        def change_tab(type):
          
            if(type == 'graphs'):
                window.frame_center_graphs.tkraise()
            elif(type == 'animations'):
                window.frame_center_animations.tkraise()

        #takes a date from the optionmenu and puts it in the calendar widget and also writes info text in the text box for that date
        def date_to_calendar(date):

            info_box.configure(text=intressanta_datum_info.get(date))
            date = date.split(":", 1)[0]
            date = datetime.strptime(date,"%d-%m-%Y")
            date.strftime("%Y-%m-%d")
            cal.set_date(date)
            
        #returns to the startmenu by destroying all frames in this window
        def startmenu():
            window.head_frame.destroy()
            

        #creates the frames
        self.update()
        window.head_frame = customtkinter.CTkFrame(master = self, corner_radius=0, height=self.winfo_height(),width=self.winfo_width(), fg_color="#252526")
        window.head_frame.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
        window.head_frame.grid_propagate(False)
        window.head_frame.grid_rowconfigure(0, weight = 1)
        window.head_frame.grid_rowconfigure(1, weight = 30)
        window.head_frame.grid_rowconfigure(2, weight = 1)
        window.head_frame.grid_columnconfigure(0, weight =1)
        window.head_frame.grid_columnconfigure(1, weight = 1)


        window.frame_upper = customtkinter.CTkFrame(master = window.head_frame,
                                                    corner_radius=0, fg_color="#3c3c3c")
        window.frame_upper.grid(row=0,column=0 ,columnspan=2,sticky="nswe")

        window.frame_center_animations = customtkinter.CTkFrame(master = window.head_frame,
                                                    corner_radius=12, fg_color="#1e1e1e")
        window.frame_center_animations.grid(row=1,column=0,padx=30,pady=30, sticky="nswe")

        window.frame_center_graphs = customtkinter.CTkFrame(master = window.head_frame,
                                                    corner_radius=12, fg_color="#1e1e1e")
        window.frame_center_graphs.grid(row=1,column=0,padx=30,pady=30, sticky="nswe")

        window.frame_bottom = customtkinter.CTkFrame(master = window.head_frame,
                                                    corner_radius=0, fg_color="#252526")
        window.frame_bottom.grid(row=2,column=0, sticky="nswe")

        window.frame_right = customtkinter.CTkFrame(master = window.head_frame,
                                                    corner_radius=0, fg_color="#252526")
        window.frame_right.grid(row=1,column=1,rowspan=3, sticky="nswe")


        # ========= UPPER FRAME ===========
        window.frame_upper.grid_rowconfigure(0,weight=1)
        window.frame_upper.grid_rowconfigure(1,weight=1)
        window.frame_upper.grid_rowconfigure(2,weight=1)

        window.button_startmeny = customtkinter.CTkButton(master=window.frame_upper,
                                                              width=40,
                                                              height=14,
                                                              corner_radius=4,
                                                              text="Startmeny",
                                                              fg_color="#3c3c3c",
                                                              text_color="#d4d4d4",
                                                              image = self.arrow_image,
                                                              compound="left",
                                                              command=lambda: startmenu())
        window.button_startmeny.grid(row=1, column=0,columnspan=1,pady=0,padx=0,sticky="w")

        window.button_grafer = customtkinter.CTkButton(master=window.frame_upper,
                                                              width=30,
                                                              height=14,
                                                              corner_radius=4,
                                                              text="Grafer",
                                                              fg_color="#3c3c3c",
                                                              text_color="#d4d4d4",
                                                              command=lambda: change_tab('graphs'))
        window.button_grafer.grid(row=1, column=1,columnspan=1,pady=0,padx=0,sticky="w")

        window.button_animationer = customtkinter.CTkButton(master=window.frame_upper,
                                                              width=30,
                                                              height=14,
                                                              corner_radius=4,
                                                              text="Animationer",
                                                              fg_color="#3c3c3c",
                                                              text_color="#d4d4d4",
                                                              command=lambda: change_tab('animations'))
        window.button_animationer.grid(row=1, column=2,columnspan=1,pady=0,padx=0,sticky="w") 

        # ========= CENTER ANIMATION FRAME ===========
        window.frame_center_animations.grid_columnconfigure(0, weight = 1,uniform='row')
        window.frame_center_animations.grid_columnconfigure(1, weight = 1,uniform='row')
        window.frame_center_animations.grid_columnconfigure(2, weight = 1)
        window.frame_center_animations.grid_columnconfigure(3, weight = 1)
        window.frame_center_animations.grid_columnconfigure(4, weight = 10)
        window.frame_center_animations.grid_rowconfigure(0, weight = 1)
        window.frame_center_animations.grid_rowconfigure(1, weight = 1)
        window.frame_center_animations.grid_rowconfigure(2, weight = 1)
        window.frame_center_animations.grid_rowconfigure(3, weight = 1)
        
        window.date_label = customtkinter.CTkLabel(master=window.frame_center_animations,
                                                text="Välj eget datum",
                                                text_color="#d4d4d4",
                                                width=50,
                                                height=25,
                                                anchor="nw")     
        window.date_label.grid(row=0, column=0, columnspan=1, pady=20, padx=10, sticky="w")

        cal = DateEntry(window.frame_center_animations, maxdate=dt2, mindate=dt1, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2021,locale='en_UK',date_pattern='yyyy-MM-dd')
        cal.grid(row=0,column=1,sticky='w')
        

        window.interesting_date_label = customtkinter.CTkLabel(master=window.frame_center_animations,
                                                text="Intressanta datum: ",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
        window.interesting_date_label.grid(row=1, column=0, columnspan=1, pady=20, padx=10, sticky="w")

        window.optionmenu_dates = customtkinter.CTkOptionMenu(master=window.frame_center_animations,
                                                         values=intressanta_datum,
                                                         width=175,
                                                         command=date_to_calendar)
                                                         
        window.optionmenu_dates.grid(row=1, column=1, pady=20, padx=2, sticky="w")

        info_box = customtkinter.CTkLabel(master=window.frame_center_animations,
                                                   text="Infobox",
                                                   width=400,
                                                   height=100,
                                                   text_color="#d4d4d4",
                                                   fg_color=("white", "gray38"),
                                                   corner_radius=8)
        info_box.grid(row=1, column=2,columnspan=2, pady=20, padx=2, sticky="w")

        window.checkbox_pie  = customtkinter.CTkCheckBox(master=window.frame_center_animations, text="Kraftfördelning",text_color="#d4d4d4")
        window.checkbox_pie.grid(row=2,column=0,columnspan=1,padx=20, pady=20,sticky ='w')
        window.checkbox_pie.select()

        window.checkbox_elpris  = customtkinter.CTkCheckBox(master=window.frame_center_animations, text="Elpris",text_color="#d4d4d4")
        window.checkbox_elpris.grid(row=2,column=1,columnspan=1,padx=12, pady=20,sticky='w')
        window.checkbox_elpris.select()

        window.checkbox_prod  = customtkinter.CTkCheckBox(master=window.frame_center_animations, text="Elflöde",text_color="#d4d4d4")
        window.checkbox_prod.grid(row=2,column=2,columnspan=1,padx=2, pady=20,sticky='w')
        window.checkbox_prod.select()

        window.button_animate = customtkinter.CTkButton(master=window.frame_center_animations,
                                                              width=120,
                                                              height=32,
                                                              corner_radius=4,
                                                              text="Animera",
                                                              command=lambda: animations(0))
        window.button_animate.grid(row=3, column=0,pady=20,padx=20,sticky='w')

        window.button_export = customtkinter.CTkButton(master=window.frame_center_animations,
                                                              width=120,
                                                              height=32,
                                                              corner_radius=4,
                                                              text="Exportera",
                                                              command=lambda: animations(1))
        window.button_export.grid(row=3, column=1,columnspan=1,pady=20,padx=20,sticky='w')


        # ========= CENTER GRAPH FRAME ===========
        window.frame_center_graphs.grid_columnconfigure(0, weight = 1)
        window.frame_center_graphs.grid_columnconfigure(1, weight = 1)
        window.frame_center_graphs.grid_columnconfigure(2, weight = 1)
        window.frame_center_graphs.grid_columnconfigure(3, weight = 10)
        window.frame_center_graphs.grid_rowconfigure(0, weight = 2)
        window.frame_center_graphs.grid_rowconfigure(1, weight = 1,uniform='row')
        window.frame_center_graphs.grid_rowconfigure(2, weight = 1,uniform='row')
        window.frame_center_graphs.grid_rowconfigure(3, weight = 1,uniform='row')
        window.frame_center_graphs.grid_rowconfigure(4, weight = 1,uniform='row')
        window.frame_center_graphs.grid_rowconfigure(5, weight = 1,uniform='row')
        window.frame_center_graphs.grid_rowconfigure(6, weight = 1,uniform='row')
        window.frame_center_graphs.grid_rowconfigure(7, weight = 2)
        window.frame_center_graphs.grid_rowconfigure(8, weight = 2)
        


        window.xlabel = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Data på x-axel:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
        window.xlabel.grid(row=0, column=0, columnspan=1, pady=10, padx=10, sticky="nw") 

        window.optionmenuxyear = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                          values=years,
                                                         command=lambda x: optionmenuyear_callback(x,"optionmenux"))
                                                         
        window.optionmenuxyear.grid(row=0, column=1, columnspan=1, pady=10, padx=2, sticky="nw") 

        window.optionmenux = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                          values=databases[0].get_columns(),
                                                         command=optionmenux_callback)
        window.optionmenux.grid(row=0, column=2, columnspan=1, pady=10, padx=2, sticky="nw") 
        window.optionmenux.set(databases[0].get_columns()[0])   #initializes menu
        


        window.ylabel = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Data 1 på y-axel:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
        window.ylabel.grid(row=1, column=0, columnspan=1, pady=2, padx=10, sticky="nw")

        window.optionmenuyyear1 = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                         values=years,
                                                         command=lambda x: optionmenuyear_callback(x,"optionmenuy1"))
                                                         
        window.optionmenuyyear1.grid(row=1, column=1, columnspan=1, pady=2, padx=2, sticky="nw")

        window.optionmenuy1 = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                         values=databases[0].get_columns(),
                                                         command=lambda x: optionmenuy_callback(x,"optionmenuy1"))
                                                         #variable=optionmenu_var)
        window.optionmenuy1.grid(row=1, column=2, columnspan=1, pady=2, padx=2, sticky="nw")
        window.optionmenuy1.set(databases[0].get_columns()[0])   #initializes menu

        window.graph_type_label = customtkinter.CTkLabel(master=window.frame_center_graphs,
                                                text="Typ av graf:",
                                                text_color="#d4d4d4",
                                                width=120,
                                                height=25,
                                                anchor="nw")     
        window.graph_type_label.grid(row=7, column=0, columnspan=1, pady=20, padx=10, sticky="sw")

        window.optionmenu_graph_type = customtkinter.CTkOptionMenu(master=window.frame_center_graphs,
                                                                    values=graphtypes,
                                                                    width=150,
                                                                    command=optionmenu_callback_graph_type)
                                                                    
        window.optionmenu_graph_type.grid(row=7, column=1,columnspan=1,pady=20, padx=2, sticky="sw")

        window.button_choose_graph = customtkinter.CTkButton(master=window.frame_center_graphs,
                                                              width=100,
                                                              height=32,
                                                              corner_radius=4,
                                                              text="Rita graf",
                                                              command=graph_maker)
        window.button_choose_graph.grid(row=8, column=0,columnspan=1,pady=20,padx=10,sticky="w")

        window.button_add_line = customtkinter.CTkButton(master=window.frame_center_graphs, #ändra kolumnsizes eller pady mellan extralinjerna
                                                              width=100,
                                                              height=32,
                                                              corner_radius=4,
                                                              text="Lägg till y-linje",
                                                              state=DISABLED,
                                                              command=add_line)
        window.button_add_line.grid(row=8, column=1,columnspan=1,pady=20,padx=12,sticky="w")

        window.button_remove_line = customtkinter.CTkButton(master=window.frame_center_graphs,
                                                              width=100,
                                                              height=32,
                                                              corner_radius=4,
                                                              text="Ta bort linje",
                                                              state=DISABLED,
                                                              command=remove_line)
        window.button_remove_line.grid(row=8, column=2,columnspan=1,pady=20,padx=0,sticky="w")

        window.button_save_data = customtkinter.CTkButton(master=window.frame_center_graphs,
                                                              width=100,
                                                              height=32,
                                                              corner_radius=4,
                                                              text="Spara data i en CSV fil",
                                                              command=create_csv)
        window.button_save_data.grid(row=8, column=3,columnspan=1,pady=20,padx=0,sticky="w")

     
    def switch_appearance_mode(self):
        if(customtkinter.get_appearance_mode() == "Light"):
            self.change_appearance_mode("dark")
            

        else:
            self.change_appearance_mode("light")  
             

    def change_appearance_mode(self,mode):
        customtkinter.set_appearance_mode(mode)

    def on_closing(self, event=0):
        self.quit()
        self.destroy()

    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))


if __name__ == "__main__":
    app = App()
    app.mainloop()