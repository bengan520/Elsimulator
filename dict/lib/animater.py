#from fileinput import close
from pickle import FALSE, TRUE
import matplotlib.ticker as ticker
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import tkinter
import tkinter.messagebox
import os
import os.path

pielabels = ["Vindkraft","Solkraft","Vattenkraft","Kärnkraft","Värmekraft","Ospec kraft"]
piecolors = ["lightgreen", "yellow", "blue","purple","orange","darkgreen"]
regions = ["SE1","SE2","SE3","SE4"]
flowx = ["Produktion","Förbrukning","Export"]
slicelabels = ["Vindkraft", "Solkraft", "Vattenkraft", "Kärnkraft", "Värmekraft", "Ospec kraft"]
figsizes = {"piechart":(13,7),"piechart+price":(14,8),"piechart+price+flow":(16,8),
            "price":(11,9),"flow":(12,6),"price+flow":(14,9),"piechart+flow":(12,8)}
class Animater:
    def __init__(self,checkboxlist,date,database,nbr_figures,window):
        self.checkboxlist = checkboxlist
        self.date = date
        self.year = database.year
        self.nbr_figures = nbr_figures
        self.window=window
        self.database=database
        self.anifunc = 0
        self.ani = 0
        self.back_button = 0
        self.forward_button = 0
        self.pause_button = 0
        self.resume_button = 0
        self.b1 = 0
        self.b2 = 0
        self.b3 = 0
        self.x = 0
        self.y = 0
    #Creates a figure
    def get_figure(self):
        nbr_figures = self.nbr_figures
        axes=[]

        #error message when no animation chosen
        if(self.checkboxlist == [0,0,0]):
            tkinter.messagebox.showerror("error","Inga typer av animationer valda till animationen")

        #piechart
        if(self.checkboxlist == [1,0,0]):
            fig, ax1= plt.subplots(nrows=1, ncols=1 , figsize =figsizes.get("piechart"),num = nbr_figures)
            axes=[ax1]
        #piechart + elpris
        elif(self.checkboxlist == [1,1,0]):
            fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2 , figsize =figsizes.get("piechart+price"),num = nbr_figures)
            axes=[ax1,ax2]
        #piechart + elpris + elflöde
        elif(self.checkboxlist == [1,1,1]):
            fig = plt.figure(figsize=(16,8),num=nbr_figures)
            gs = fig.add_gridspec(1,3)
            ax1 = fig.add_subplot(gs[0,0])
            ax2 = fig.add_subplot(gs[0,1])
            ax3 = fig.add_subplot(gs[0,2])
            axes=[ax1,ax2,ax3]
            plt.subplots_adjust(wspace=0.6)
        #elpris
        elif(self.checkboxlist == [0,1,0]):
            fig, ax1= plt.subplots(nrows=1, ncols=1 , figsize =figsizes.get("price"),num = nbr_figures)
            axes=[ax1]
        #elflöde
        elif(self.checkboxlist == [0,0,1]):
            fig, ax1= plt.subplots(nrows=1, ncols=1 , figsize = figsizes.get("flow"),num = nbr_figures)
            axes=[ax1]
        #elpris + elflöde
        elif(self.checkboxlist == [0,1,1]):
            fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2 , figsize = figsizes.get("price+flow"),num = nbr_figures)
            plt.subplots_adjust(wspace=0.4)
            axes=[ax1,ax2]
        #piechart + elflöde
        elif(self.checkboxlist == [1,0,1]):
            fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2 , figsize = figsizes.get("piechart+flow"),num = nbr_figures)
            plt.subplots_adjust(wspace=0.4)
            axes=[ax1,ax2]
        fig.canvas.mpl_connect('close_event', self.close) #behöver göra en close funktion i denna klassen som kallas från main klassen när det stängs
        fig.text(0.1,0.8, 'create textlist')
        
        return fig,axes

    #creates the buttons
    def create_buttons(self,x,y,paused):
        self.x = x
        self.y = y
        if(paused == FALSE):
            
            bpause_ax = plt.axes([0.32+x,0.05+y,0.07,0.05])
            bpause = Button(bpause_ax,'Pause',color='cornflowerblue',hovercolor='royalblue')
            bpause.on_clicked(self.pause)
            bforward_ax = plt.axes([0.39+x,0.05+y,0.07,0.05])
            bforward = Button(bforward_ax,'>',color='cornflowerblue',hovercolor='royalblue')
            bforward.on_clicked(self.stepforward)
            bback_ax = plt.axes([0.25+x,0.05+y,0.07,0.05])
            bback = Button(bback_ax,'<',color='cornflowerblue',hovercolor='royalblue')
            bback.on_clicked(self.stepbackward)
            return bpause,bforward,bback
        if(paused == TRUE):
            bresume_ax = plt.axes([0.32+x,0.05+y,0.07,0.05])
            bresume = Button(bresume_ax,'Resume',color='cornflowerblue',hovercolor='royalblue')
            bresume.on_clicked(self.resume)
            bforward_ax = plt.axes([0.39+x,0.05+y,0.07,0.05])
            bforward = Button(bforward_ax,'>',color='cornflowerblue',hovercolor='royalblue')
            bforward.on_clicked(self.stepforward)
            bback_ax = plt.axes([0.25+x,0.05+y,0.07,0.05])
            bback = Button(bback_ax,'<',color='cornflowerblue',hovercolor='royalblue')
            bback.on_clicked(self.stepbackward)
            return bresume,bforward,bback

    def buttonhandler(self,x,y,paused):
        
        if(paused == FALSE):
            self.b1,self.b2,self.b3 = self.create_buttons(x,y,paused)
        
        if(paused == TRUE):
            self.b1,self.b2,self.b3 = self.create_buttons(x,y,paused)



    #determines how the frames should be updated, defines a "generator"
    def update_frame(self):
        f = 0
        while True:
            f += self.ani.direction
            yield f
    
    def pause(self,var):
        self.ani.pause()
        self.buttonhandler(self.x,self.y,TRUE)

    def resume(self,var):
        self.ani.resume() 
        self.buttonhandler(self.x,self.y,FALSE)

    def stepforward(self,var):
        self.ani.direction = +1
        f = self.ani.frame_seq.__next__()
        self.anifunc(f)
        plt.draw()
    
    def stepbackward(self,var):
        self.ani.direction = -1
        f = self.ani.frame_seq.__next__()
        self.anifunc(f)
        plt.draw()
        self.ani.direction = +1


    #returns function for how the pie value labels update
    def poweroutput(self,values):

        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d}'.format(p=pct,v=val) + ' MW' if pct > 1 else ''
        return my_autopct
    #executes when the animation is closed
    def close(self,var):
        self.window.button_choose_graph.configure(state=tkinter.NORMAL)
        
        

    #returns list with the values plotted in the pie chart
    def get_pie_slices(self,i):
        values_slices = []

        for name in slicelabels:
            values_slices.append(self.database.get_num_indexed_value(name, "Sverige", i))

        return values_slices   

    #creates the update function for the pie chart
    def update_pie(self,i,ax):
        ax.clear()
        slices = self.get_pie_slices(i)
        ax.pie(slices, labels=pielabels, colors=piecolors, wedgeprops={'edgecolor': 'black'},autopct=self.poweroutput(slices))
        ax.set_title('Kraftfördelning')


    #creates the update function for the price chart
    def update_price(self,i,ax,pricelim):
        ax.clear()
        pricelist = self.database.get_num_indexed_values("Elpris",i)
        ax.bar(regions,pricelist, edgecolor="white",linewidth = 0.7)
        ax.set_title("Elpris")
        ax.set(ylim = (0,pricelim))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(200))
        ax.set_ylabel('kr/MWh')
        ax.set_xlabel('Elområde')

    #creates the update function for the flowchart
    def update_flow(self,i,ax,flowmin,flowmax):
        ax.clear()
        datalist = [self.database.get_num_indexed_value("Produktion", "Sverige",i),self.database.get_num_indexed_value("Konsumption", "Sverige",i),-self.database.get_num_indexed_value("SE net exchange","Sverige",i)]
        ax.bar(flowx,datalist, edgecolor="white",linewidth = 0.7)
        ax.set_title("Elflöde")
        ax.set(ylim = (flowmin,flowmax))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2000))
        ax.tick_params(labelrotation=15)
        ax.set_ylabel('MW')

    #creates the animations and exports
    def animate(self,export,name,fps):
        plt.style.use("fivethirtyeight")
        flowmin = min(-self.database.get_values_year(f"SE net exchange {self.year} Sverige"))
        flowmax = max(self.database.get_values_year(f"Produktion {self.year} Sverige"))
        pricelim = max(max(self.database.get_values_year(f"Elpris {self.year} SE1")),max(self.database.get_values_year(f"Elpris {self.year} SE2")),
                        max(self.database.get_values_year(f"Elpris {self.year} SE3")),max(self.database.get_values_year(f"Elpris {self.year} SE4")))
        fig,axes = self.get_figure()
        print("date: ",self.date)
        date_offset = self.database.get_index_from_date(self.date)
        if(export == 1):
            path = f"exported gifs/{name}.gif"
            grandparent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            full_path = os.path.join(grandparent_path, path).replace("\\", "/")
            delay = 1000/float(fps)
            
        
        def animate1(i):
            i += date_offset            
            i = i % self.database.nbr_hours            
            del fig.texts[0]        
            fig.text(0.03,0.9,self.database.get_num_indexed_value("Dates", "Sverige", i),fontsize=30)
            self.update_pie(i,axes[0])
            

        def animate2(i):
            i += date_offset
            i = i % self.database.nbr_hours 
            del fig.texts[0]
            fig.text(0.03,0.9,self.database.get_num_indexed_value("Dates", "Sverige", i),fontsize=30)
            self.update_pie(i,axes[0])
            self.update_price(i,axes[1],pricelim)

        def animate3(i):
            i += date_offset
            i = i % self.database.nbr_hours 
            del fig.texts[0]
            fig.text(0.03,0.9,self.database.get_num_indexed_value("Dates", "Sverige", i),fontsize=30)
            self.update_pie(i,axes[0])
            self.update_price(i,axes[1],pricelim)
            self.update_flow(i,axes[2],flowmin,flowmax)
        
        def animate4(i):
            i += date_offset
            i = i % self.database.nbr_hours 
            del fig.texts[0]
            fig.text(0.03,0.9,self.database.get_num_indexed_value("Dates", "Sverige", i),fontsize=30)
            self.update_price(i,axes[0],pricelim)

        def animate5(i):
            i += date_offset
            i = i % self.database.nbr_hours 
            del fig.texts[0]
            fig.text(0.03,0.9,self.database.get_num_indexed_value("Dates", "Sverige", i),fontsize=30)
            self.update_flow(i,axes[0],flowmin,flowmax)
        
        def animate6(i):
            i += date_offset
            i = i % self.database.nbr_hours 
            del fig.texts[0]
            fig.text(0.025,0.95,self.database.get_num_indexed_value("Dates", "Sverige", i),fontsize=30)
            self.update_price(i,axes[0],pricelim)
            self.update_flow(i,axes[1],flowmin,flowmax)
        
        def animate7(i):
            i += date_offset
            i = i % self.database.nbr_hours 
            del fig.texts[0]
            fig.text(0.03,0.9,self.database.get_num_indexed_value("Dates", "Sverige", i),fontsize=30)
            self.update_pie(i,axes[0])
            self.update_flow(i,axes[1],flowmin,flowmax)

        
        if(self.checkboxlist == [1,0,0]):
            if(export == 0):
                self.anifunc = animate1
                self.buttonhandler(-0.12,0,FALSE) 
                self.ani = FuncAnimation(fig,animate1,frames = self.update_frame,interval=500)
                self.ani.direction = +1
                plt.show()
            elif(export == 1):
                ani = FuncAnimation(fig,animate1,frames = 24,interval=delay)
                ani.save(full_path)
                plt.close()
                
        
        if(self.checkboxlist == [1,1,0]):
            if(export == 0):
                self.anifunc = animate2
                self.buttonhandler(-0.12,0,FALSE)
                self.ani = FuncAnimation(fig,animate2,frames = self.update_frame,interval=500)
                self.ani.direction = +1
                plt.show()
            elif(export == 1):
                ani = FuncAnimation(fig,animate2,frames = 24,interval=delay)
                ani.save(full_path)
                plt.close()
        
        if(self.checkboxlist == [1,1,1]):
            if(export == 0):
                self.anifunc = animate3
                self.buttonhandler(-0.12,0,FALSE)
                self.ani = FuncAnimation(fig,animate3,frames = self.update_frame,interval=500)
                self.ani.direction = +1
                plt.show()
            elif(export == 1):
                ani = FuncAnimation(fig,animate3,frames = 24,interval=delay)
                ani.save(full_path)
                plt.close()

        if(self.checkboxlist == [0,1,0]):
            if(export == 0):
                self.anifunc = animate4
                self.buttonhandler(-0.12,0,FALSE)
                self.ani = FuncAnimation(fig,animate4,frames = self.update_frame,interval=500)
                self.ani.direction = +1
                plt.show()
            elif(export == 1):
                ani = FuncAnimation(fig,animate4,frames = 24,interval=delay)
                ani.save(full_path)
                plt.close()

        if(self.checkboxlist == [0,0,1]):
            if(export == 0):
                self.anifunc = animate5
                self.buttonhandler(-0.12,0,FALSE)
                self.ani = FuncAnimation(fig,animate5,frames = self.update_frame,interval=500)
                self.ani.direction = +1
                plt.show()
            elif(export == 1):
                ani = FuncAnimation(fig,animate5,frames = 24,interval=delay)
                ani.save(full_path)
                plt.close()

        
        if(self.checkboxlist == [0,1,1]):
            if(export == 0):
                self.anifunc = animate6
                self.buttonhandler(0.13,-0.055,FALSE)
                self.ani = FuncAnimation(fig,animate6,frames = self.update_frame,interval=500)
                self.ani.direction = +1
                plt.show()
            elif(export == 1):
                ani = FuncAnimation(fig,animate6,frames = 24,interval=delay)
                ani.save(full_path)
                plt.close()

        
        if(self.checkboxlist == [1,0,1]):
            if(export == 0):
                self.anifunc = animate7
                self.buttonhandler(0,0,FALSE)
                self.ani = FuncAnimation(fig,animate7,frames = self.update_frame,interval=500)
                self.ani.direction = +1
                plt.show()
            elif(export == 1):
                ani = FuncAnimation(fig,animate7,frames = 24,interval=delay)
                ani.save(full_path)
                plt.close()
        
        
