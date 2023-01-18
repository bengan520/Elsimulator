from tkinter import *

class Map_drawing:
    
    def __init__(self):
        print("my new map")
    #Function to draw our map with arrows
    def draw_map(map_label, map, map_window,export, export_max):

        #Function for setting colors dependent on how close to their max export/import values
        def color_code(value,export_max,import_max):
            if value<0:
                x= export_max
            else:
                x = import_max
            value = abs(value)
            #value = min(max(value,0),export_max)
            r, g, b = 1, 1, 1

            if value < x/2:
                b = ((x/2)-value) / (x/2)
                if(b<0):
                    b=0
                    
            
            elif x == 0:
                pass
                
            else:
                
                g,b = (x-value) / (x/2),0
                if g<0:
                    g=0

            return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
            

        map_label.update()
        my_map = Canvas(map_window, 
                        width=map_label.winfo_width(), 
                        height=map_label.winfo_height(), 
                        highlightthickness=0,
                        bg="#3c3c3c")
        
        #draws on the image as background
        my_image = my_map.create_image(0, 0, anchor=NW, image=map)
        
        
        #Coordinates for the arrows that goes between the sectors
        #SEPL SEDE SE3NO1 SE3DK1 SE4DK2 SE1FI SE3FI SE1NO4 SE2NO3 SE2NO4 SE1SE2 SE2SE3 SE3SE4 SE4LT 
        pos_x0 = [250, 230, 240, 200, 220, 440, 370, 350, 230, 280, 350, 280, 260, 320]
        pos_y0 = [600, 600, 440, 500, 550, 180, 450, 180, 330, 280, 240, 380, 510, 550]
        pos_x1 = [350, 220, 170, 150, 200, 500, 450, 350, 200, 260, 350, 280, 260, 480]
        pos_y1 = [650, 660, 420, 530, 600, 180, 400, 130, 330, 260, 290, 440, 550, 600]
        color=[]

        
        for i in range(len(pos_x0)):
            color.append(color_code(export[i],export_max[2*i], export_max[2*i+1]))
            

     
        # checks if export is 0,- or + and positions arrow depending on that
        for i in range(len(pos_x0)):
            dir=''
            
            if(export[i]==0):
                
                my_map.create_line(pos_x0[i],pos_y0[i],pos_x1[i],pos_y1[i],fill="black", arrow="both",arrowshape=(2,1,8), width=5)        
            
            elif(export[i]<0):
                dir='last'
                my_map.create_line(pos_x0[i],pos_y0[i],pos_x1[i],pos_y1[i],fill=color[i], arrow=dir, width=5)        
            else:
                dir='first'
                my_map.create_line(pos_x0[i],pos_y0[i],pos_x1[i],pos_y1[i],fill=color[i], arrow=dir, width=5)
            
        

        return(my_map)

    