import os
import os.path
import pandas
import datetime
import csv

regions = ["SE1", "SE2", "SE3", "SE4"]

class Database:
    def __init__(self, year):
        self.year = year
        path = f"resources/Databas{year}_csv.csv"
        #full_path = os.path.join(os.getcwd(), path).replace("\\", "/")
        full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path).replace("\\", "/")
        self.data = pandas.read_csv(full_path, index_col=0, low_memory=False)
        self.num_indexed_data = pandas.read_csv(full_path, low_memory=False)
        self.nbr_hours = len(self.num_indexed_data.index)

    def get_value(self, name, region, date):
        
        column = f"{name} {self.year} {region}"
        # TODO: Return None?
        if not column in self.data:
            return 0
        if not date in self.data[column]:
            return 0
        return self.data[column][date]

    def get_values(self, name, date):
        values = []
        for region in regions:
            values.append(self.get_value(name, region, date))
        return values

    #Returns series with all hour values from the year
    #If it is a date column, we return a list with datetime objects instead of Series objects
    def get_values_year(self,name):
        if ("Dates" in name):
            #s = self.data[name].astype(str)
            #s = s.drop(s.index[-1])
            s = self.data[name]
            s = s.apply(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y:%H'))
            return s    
        #return self.data[name].drop(self.data[name].index[-1])
        return self.data[name]

    
    #Returns a list with strings of the column names in the database
    def get_columns(self):
        return list(self.data.columns)
    
    
    # Gör funktion som returnerar rätt label för rätt data
    def get_label(self,column):

        if("Elpris" in column):
            return column + " [Kr/MWh]"
        
        elif("Dates" in column):
            return column
        
        return column + " [MWh/h]"
    
    #returns a value from the database using numerical indexes
    def get_num_indexed_value(self,name,region,i):
        column = f"{name} {self.year} {region}"
        # TODO: Return None?
        if not column in self.num_indexed_data:
            return 0
        if not i in self.num_indexed_data[column]:
            return 0
        
        return self.num_indexed_data[column][i]

    #returns values from all regions using numerical indexes
    def get_num_indexed_values(self,name,i):
        values = []
        for region in regions:
            values.append(self.get_num_indexed_value(name, region, i))
        return values
    
    #returns numerical index from specific date
    def get_index_from_date(self,date):
        for i in self.num_indexed_data["Dates " + self.year + " Sverige"].index:
           
            if(self.num_indexed_data["Dates " + self.year + " Sverige"][i] == date):
                return i
        return 0        

    def get_column_name(self,type):
        col_names = []
        temp_col=self.get_columns()
        for i in temp_col:
            if(type==0 and "kraft" in i and "Sverige" not in i):
                col_names.append(i)
            elif(type==1 and "Konsumption" in i and "Sverige" not in i):
                col_names.append(i)
            elif(type==2 and ("-" in i) and ("net" not in i) and ("SE - NO " not in i) and ("SE - FI " not in i) and ("SE - DK " not in i)):
                col_names.append(i)
        return col_names
        
    def get_values_export(self,date):
        values=[]
        for column in self.data:
            if ("-" in column) and ("net" not in column) and ("SE - NO " not in column) and ("SE - FI " not in column) and ("SE - DK " not in column):
                values.append(self.data[column][date])    
        return values      
        
    def create_csv(var,filename,column_names,variables):
        path = f"saved_csv_files/{filename}.csv"
        grandparent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        full_path = os.path.join(grandparent_path, path).replace("\\", "/")
        with open(full_path,'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            for values in zip(*variables):
                writer.writerow(values)
    
    def get_values_export_max(self,date):
        values=[]
        for column in self.data:
            if((">" in column) or ("<" in column)):
                values.append(self.data[column][date])
        return values

