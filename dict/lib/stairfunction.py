import matplotlib.pyplot as plt



windprice = 100
solarprice = 200
hydroprice = 400
nuclearprice = 800
ospecprice = 2000
värmeprice = 1000
gasprice = 1600
oilprice = 6400
no_pic = True
class Stairfunction:
    def __init__(self,max_connection):
        print("ny stairfunktion")

    #Function that returns a drawn stairfunction of the price in the picked sector.
    def draw_graph(production,consumption,export_max,export,currentsector,prices):
        
        #Function that scale the prices of the different power sources dependant on the price in the sector and connected sectors.
        #Returns a list with the prices for the power sources
        def price_compare(price_sector, price_import,currentsector):
            if(price_sector>price_import) and (currentsector=="SE3"):
                windprice = 0.1*price_sector
                solarprice = 0.2*price_sector
                hydroprice = 0.4*price_sector
                nuclearprice = 0.6*price_sector
                värmeprice = 0.8*price_sector
                ospecprice = 1.01*price_sector  
                prices_return=[windprice,solarprice,hydroprice,nuclearprice,värmeprice,ospecprice]  
                return prices_return
            elif(price_sector<=price_import) and (currentsector=="SE3"):
                windprice = 0.1*price_sector
                solarprice = 0.2*price_sector
                hydroprice = 0.4*price_sector
                nuclearprice = 0.6*price_sector
                värmeprice = 0.8*price_sector
                ospecprice = 0.9*price_sector  
                prices_return=[windprice,solarprice,hydroprice,nuclearprice,värmeprice,ospecprice]  
                return prices_return
            elif(price_sector>price_import):
                windprice = 0.1*price_sector
                solarprice = 0.2*price_sector
                hydroprice = 0.4*price_sector
                värmeprice = 0.8*price_sector
                ospecprice = 1.01*price_sector  
                prices_return=[windprice,solarprice,hydroprice,värmeprice,ospecprice]  
                return prices_return
            else:
                windprice = 0.1*price_sector
                solarprice = 0.2*price_sector
                hydroprice = 0.4*price_sector
                värmeprice = 0.8*price_sector
                ospecprice = 0.9*price_sector  
                prices_return=[windprice,solarprice,hydroprice,värmeprice,ospecprice]  
                return prices_return
        
        
        
        #remove the nuclear power from the list temporarily to make the other data easier to extract
        temp = production[8]
        production.remove(temp)
        SE1_prod =[]
        SE2_prod =[]
        SE3_prod =[]
        SE4_prod =[]
        #Moves production into a list for its respective sector .
        for i in range(len(production)):
            
            if (i % 4) == 0:
               SE1_prod.append(production[i])
               
            
            elif ((i+3) % 4) == 0:
                SE2_prod.append(production[i])
               

            elif ((i+2) % 4) == 0:
                SE3_prod.append(production[i])
               

            elif ((i+1) % 4) == 0:
                SE4_prod.append(production[i])        

        #adds nuclear power into the production mix for SE3 and puts it back into the production list     
        SE3_prod.append(temp)   
        production.insert(8,temp)
        sectors = [SE1_prod,SE2_prod,SE3_prod,SE4_prod]
        diffs= []
        

        #Not currently used. might be used when expanding the program
        #Function for checking if the production in a sector covers it's own consumption need. 
        for i in range(len(sectors)):
            diff = consumption[i]
            broke=0
            for j in range(len(sectors[i])):
                diff = diff-sectors[i][j]
   
                if diff <=0 and broke == 0:
                    
                    diffs.append(j)
                    broke = 1
            
            if i == 2 and broke == 0:
                diff = diff-sectors[2][5]

                if(diff<=0):
                    diffs.append(5)         

            if broke == 0:
                diffs.append("didnt break")
            
        export_sum = 0
        price = 0
        consumption_sector = 0

        
        #Preps the chosen sector to be drawn up. Sets price, colors and labels for the power sources. ##############
        ############ SE1 ##############
        if currentsector == "SE1":
            export_to_FI = export[5] #Export SE1-FI
            export_to_NO4 = export[7] #Export SE1-NO4
            export_to_SE2 = export[10] #Export SE1-SE2
            price_SE1 = prices[0]
            price_SE2 = prices[1]
            solar = SE1_prod[0]
            wind  = SE1_prod[1]
            hydro = SE1_prod[2]
            värme = SE1_prod[3]
            ospec = SE1_prod[4]
            
            prices = price_compare(price_SE1,price_SE2,currentsector)
            kraftslaglabels = ["Vindkraft","Solkraft","Vattenkraft","Ospec","Värmekraft","Import från SE2"]
            # Checks if we are importing or exporting in the sector
            if(export_to_SE2 > 0):
                kraftslag = [wind,solar,hydro,ospec,värme,abs(export_to_SE2)]
                prices.append(price_SE2)
                #prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice,price_SE2]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange","grey"]
                export_sum = export_to_FI+export_to_NO4
            else:
                kraftslag = [wind,solar,hydro,ospec,värme]
                #prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange"]
                export_sum = export_to_FI+export_to_NO4-abs(export_to_SE2)

            price = price_SE1
            consumption_sector = consumption[0]

        ############ SE2 ##############
        if currentsector == "SE2":
            export_to_NO4 = export[9] #export SE2-NO4
            export_to_NO3 = export[8] #export SE2-NO3
            export_to_SE2 = export[10] #export SE1-SE2
            export_to_SE3 = export[11] #export SE2-SE3

            price_SE1 = prices[0]
            price_SE2 = prices[1]
            price_SE3 = prices[2]
            solar = SE2_prod[0]
            wind  = SE2_prod[1]
            hydro = SE2_prod[2]
            värme = SE2_prod[3]
            ospec = SE2_prod[4]
            prices = price_compare(price_SE2,price_SE1,currentsector)
            
            kraftslaglabels = ["Vindkraft","Solkraft","Vattenkraft","Ospec","Värmekraft","Import från SE1","Import från SE3"]
            
            # Checks if we are importing or exporting in the sector
            if (export_to_SE2 < 0 and export_to_SE3 > 0):
                kraftslag = [wind,solar,hydro,ospec,värme,abs(export_to_SE2),abs(export_to_SE3)]
                prices.append(price_SE1)
                prices.append(price_SE2)
                # prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice,price_SE1,price_SE3]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange","grey","black"]
                export_sum = export_to_NO4+export_to_NO3
            
            elif(export_to_SE2 < 0):
                kraftslag = [wind,solar,hydro,ospec,värme,abs(export_to_SE2)]
                prices.append(price_SE1)
                # prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice,price_SE1]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange","grey"]
                export_sum = export_to_NO4+export_to_NO3-abs(export_to_SE3)
            elif(export_to_SE3 > 0):
                kraftslag = [wind,solar,hydro,ospec,värme,abs(export_to_SE3)]
                prices.append(price_SE3)
                #prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice,price_SE3]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange","grey"]
                export_sum = export_to_NO4+export_to_NO3-abs(export_to_SE2)
                kraftslaglabels = ["Vindkraft","Solkraft","Vattenkraft","Ospec","Värmekraft","Import från SE3"]
            else:
                kraftslag = [wind,solar,hydro,ospec,värme]
                #prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange"]
                export_sum = export_to_NO4+export_to_NO3-abs(export_to_SE2)-abs(export_to_SE3)

            price=price_SE2
            consumption_sector=consumption[1]
        ############ SE3 ##############
        if currentsector == "SE3":
            
            export_to_NO1 = export[2]
            export_to_DK1 = export[3]
            export_to_FI = export[6]
            export_to_SE2 = export[11]
            export_to_SE4 = export[12]
            price_SE2 = prices[1]
            price_SE3 = prices[2]
            price_SE4 = prices[3]
            solar = SE4_prod[0]
            wind = SE3_prod[1]
            hydro = SE3_prod[2]
            värme = SE3_prod[3]
            ospec = SE3_prod[4]
            kärn = SE3_prod[5]
            prices = price_compare(price_SE3,price_SE2,currentsector)
            kraftslaglabels = ["Vindkraft","Solkraft","Vattenkraft","Kärnkraft","Ospec","Värmekraft","Import från SE2","Import från SE4"]

            # Checks if we are importing or exporting in the sector
            if (export_to_SE2 < 0 and export_to_SE4 > 0):
                kraftslag = [wind,solar,hydro,kärn,ospec,värme,abs(export_to_SE2),abs(export_to_SE4)]
                prices.append(price_SE2)
                prices.append(price_SE4)
                # prices = [windprice,solarprice,hydroprice,nuclearprice,ospecprice,värmeprice,price_SE2,price_SE4]
                färger = ["lightgreen","yellow","#4e4ed9","purple","darkgreen","orange","grey","black"]
                export_sum = export_to_NO1+export_to_DK1+export_to_FI
            
            elif(export_to_SE2 < 0):
                kraftslag = [wind,solar,hydro,kärn,ospec,värme,abs(export_to_SE2)]
                prices.append(price_SE2)
                #prices = [windprice,solarprice,hydroprice,nuclearprice,ospecprice,värmeprice,price_SE2]
                färger = ["lightgreen","yellow","#4e4ed9","purple","darkgreen","orange","grey"]
                export_sum = export_to_NO1+export_to_DK1+export_to_FI-abs(export_to_SE4)

            elif(export_to_SE4 > 0):
                kraftslag = [wind,solar,hydro,kärn,ospec,värme,abs(export_to_SE4)]
                prices.append(price_SE4)
                #prices = [windprice,solarprice,hydroprice,nuclearprice,ospecprice,värmeprice,price_SE4]
                färger = ["lightgreen","yellow","#4e4ed9","purple","darkgreen","orange","grey"]
                export_sum = export_to_NO1+export_to_DK1+export_to_FI-abs(export_to_SE2)
            else:
                kraftslag = [wind,solar,hydro,kärn,ospec,värme]
                #prices = [windprice,solarprice,hydroprice,nuclearprice,ospecprice,värmeprice]
                färger = ["lightgreen","yellow","#4e4ed9","purple","darkgreen","orange"]
                export_sum = export_to_NO1+export_to_DK1+export_to_FI-abs(export_to_SE2)-abs(export_to_SE4)
            
            price=price_SE3
            consumption_sector=consumption[2]
        ############ SE4 ##############
        if currentsector == "SE4":
            export_to_DK2 = export[4]   #export SE4-DK2  Negative means export and positive import
            export_to_LT =  export[13] #export  SE4-LT
            export_to_DE = export[1] #export SE4-DE
            export_to_PL = export[0] #export SE4-PL
            export_to_SE4 = export[12] #export SE3-SE4
            price_SE3 = prices[2]
            price_SE4 = prices[3]
            solar = SE4_prod[0]
            wind = SE4_prod[1]
            hydro = SE4_prod[2]
            värme = SE4_prod[3]
            ospec = SE4_prod[4]
            
            prices = price_compare(price_SE4,price_SE3,currentsector)
            kraftslaglabels = ["Vindkraft","Solkraft","Vattenkraft","Ospec","Värmekraft","Import från SE3"]
            
            # Checks if we are importing or exporting in the sector
            if(export_to_SE4 < 0):
                kraftslag = [wind,solar,hydro,ospec,värme,abs(export_to_SE4)]
                prices.append(price_SE3)
                #prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice,price_SE3]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange","red"]
                export_sum = export_to_DK2+export_to_LT+export_to_DE+export_to_PL
            else:
                kraftslag = [wind,solar,hydro,ospec,värme]
                #prices = [windprice,solarprice,hydroprice,ospecprice,värmeprice]
                färger = ["lightgreen","yellow","#4e4ed9","darkgreen","orange"]
                export_sum = export_to_DK2+export_to_LT+export_to_DE+export_to_PL-abs(export_to_SE4)
            
            price=price_SE4
            consumption_sector=consumption[3]

        #Sorts labels, power sources, colors, and prices.
        sorteradekraftslaglabels = [kraftslaglabels for _,kraftslaglabels in sorted(zip(prices,kraftslaglabels))]
        sorteradekraftslag = [kraftslag for _,kraftslag in sorted(zip(prices,kraftslag))]
        sorteradefärger = [färger for _,färger in sorted(zip(prices,färger))]
        sorteradeprices = prices
        sorteradeprices.sort()
        
        fig_stair,ax = plt.subplots(dpi=110)
      
        #sets cordinates for the different part of the stairfunction      
        x1 = [0,sorteradekraftslag[0]]
        x12 = [sorteradekraftslag[0],sorteradekraftslag[0]]
        x2 = [sorteradekraftslag[0],sorteradekraftslag[0]+sorteradekraftslag[1]]
        x23 = [sorteradekraftslag[0]+sorteradekraftslag[1],sorteradekraftslag[0]+sorteradekraftslag[1]]
        x3 =[sorteradekraftslag[0]+sorteradekraftslag[1],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]]
        x34 = [sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]]
        x4=[sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]]
        x45 = [sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]]
        x5 =[sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]]
        x_value= [x1[0], x2[0], x3[0], x4[0], x5[0]]
        
        y1 = [sorteradeprices[0],sorteradeprices[0]]
        y12 = [sorteradeprices[0],sorteradeprices[1]]
        y2 = [sorteradeprices[1],sorteradeprices[1]]
        y23 = [sorteradeprices[1],sorteradeprices[2]]
        y3 = [sorteradeprices[2],sorteradeprices[2]]
        y34 = [sorteradeprices[2],sorteradeprices[3]]
        y4 = [sorteradeprices[3],sorteradeprices[3]]
        y45 = [sorteradeprices[3],sorteradeprices[4]]
        y5 = [sorteradeprices[4],sorteradeprices[4]]
        
        #Checks if we have more power sources than 5 and sets cordinates for the 6th if we do
        if(len(sorteradekraftslag)>5):
            x56 =[sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]]
            x6 = [sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5]]
            y56 = [sorteradeprices[4],sorteradeprices[5]]
            y6 = [sorteradeprices[5],sorteradeprices[5]]
            x_value.append([x6[0]])
          
        #Checks if we have more power sources than 6 and sets cordinates for the 7th if we do  
        if(len(sorteradekraftslag)>6):
            x67 = [sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5]]
            x7 =  [sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5]+sorteradekraftslag[6]]
            y67 = [sorteradeprices[5],sorteradeprices[6]]
            y7 =  [sorteradeprices[6],sorteradeprices[6]]
            x_value.append([x7[0]])
        
        #Checks if we have more power sources than 7 and sets cordinates for the 8th if we do
        if(len(sorteradekraftslag)>7):
            x78 = [sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5]+sorteradekraftslag[6],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5]+sorteradekraftslag[6]]
            x8 =  [sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5]+sorteradekraftslag[6],sorteradekraftslag[0]+sorteradekraftslag[1]+sorteradekraftslag[2]+sorteradekraftslag[3]+sorteradekraftslag[4]+sorteradekraftslag[5]+sorteradekraftslag[6]+sorteradekraftslag[7]]
            y78 = [sorteradeprices[6],sorteradeprices[7]]
            y8 =  [sorteradeprices[7],sorteradeprices[7]]
            x_value.append([x8[0]])
       
        #Draws out the stairfunction       
        ax.plot(x1,y1,linewidth=3, label = sorteradekraftslaglabels[0], color = sorteradefärger[0])
        ax.plot(x12,y12,linewidth=3, color = sorteradefärger[0])
        ax.plot(x2,y2,linewidth=3, label = sorteradekraftslaglabels[1], color=sorteradefärger[1])
        ax.plot(x23,y23,linewidth=3, color = sorteradefärger[1])
        ax.plot(x3,y3,linewidth=3, label = sorteradekraftslaglabels[2],color = sorteradefärger[2])
        ax.plot(x34,y34,linewidth=3,color=sorteradefärger[2])
        ax.plot(x4,y4,linewidth=3, label = sorteradekraftslaglabels[3],color=sorteradefärger[3])
        ax.plot(x45,y45,linewidth=3, color=sorteradefärger[3])
        ax.plot(x5,y5,linewidth=3, label = sorteradekraftslaglabels[4], color=sorteradefärger[4])
        
        #checks the length and draws if the length of sorteradekraftslag is longer than 5,6 and 7.
        if len(sorteradekraftslag)>5:
            ax.plot(x56,y56,linewidth=3,  color=sorteradefärger[4])
            ax.plot(x6,y6,linewidth=3, label = sorteradekraftslaglabels[5], color=sorteradefärger[5])
        
        if  len(sorteradekraftslag)>6:
            ax.plot(x67,y67,linewidth=3,  color=sorteradefärger[5])
            ax.plot(x7,y7,linewidth=3, label = sorteradekraftslaglabels[6], color=sorteradefärger[6])
        
        if  len(sorteradekraftslag)>7:
            ax.plot(x78,y78,linewidth=3,  color=sorteradefärger[6])
            ax.plot(x8,y8,linewidth=3, label = sorteradekraftslaglabels[7], color=sorteradefärger[7])

        
        #Sets the y-axis of the dot tracking current price/consumption to the current powersource.
        y_dot = sorteradeprices[0]
        for i in range(len(x_value)):
            if consumption_sector-export_sum>=x_value[i]:
                y_dot=sorteradeprices[i]
        
        #plots the current price as a green circle
        ax.plot(consumption_sector-export_sum,y_dot,marker = "o", markersize=10, markerfacecolor="green",label = "Elpris")
        
        ax.legend()
        ax.legend(fontsize=10, loc="lower right", facecolor="#2e2e2e", edgecolor="black",
        labelcolor="#d4d4d4")
        plt.xlabel("Produktion och förbrukning [MW]", color = "#d4d4d4",fontsize = 10,labelpad=0)
        plt.ylabel("Pris", color = "#d4d4d4",fontsize = 10)
        ax.set_yticks([])
        ax.grid(color="#787777")
        ax.tick_params(axis="x", labelcolor="#d4d4d4",labelsize = 10)
        fig_stair.set_edgecolor("red")
        ax.set_facecolor("#2e2e2e")
        fig_stair.set_facecolor("#252526")
        ax.spines['bottom'].set_color('black')
        ax.spines['top'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['top'].set_linewidth(1)
        ax.spines['left'].set_linewidth(1)
        ax.spines['right'].set_linewidth(1)
          
        return fig_stair
        
        

        
       

       
