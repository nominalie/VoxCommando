# Script to assist with json parsing. 
# Generates payload xml lists for Nest devices.
# Also returns Fahrenheit or Celsius temps based on your Nest settings.
# This code is designed to work with VoxCommando.
# It does not include any http authentication or Nest login functions.
# Version date: 25-Mar-2016
############################################################################################

from System.Collections.Generic import *
import json
import time

class NestVC:

    def __init__(self):
        
        self.d = ""
        self.t = round(time.clock())
        self.thermos = {}
        self.prots = {}
        self.strucs = {}
        
    def readNest(self):
    
        now = round(time.clock())
        
        if self.d=="" or now - self.t > 180:#If Nest data was last updated over 3 mins ago, will rescan online data. Otherwise uses prev. data.
            vc.triggerEvent("nestUpdate",None)
            with open("Nest/Nest_dev_status.txt","r") as nest_data:
                read_nest = nest_data.read()
            self.d = json.loads(read_nest)
            self.t = now
            #vc.log("Nest.py log: Nest data over 3 mins old. Re-scanned Nest data.")
                
        else:
            with open("Nest/Nest_dev_status.txt","r") as nest_data:
                read_nest = nest_data.read()
            self.d = json.loads(read_nest)
            #vc.log("Nest.py log: Nest data downloaded less than 3 minutes ago. Using existing data.")
                
        return self.t                    

    def getDevices(self):
        self.readNest()
        d = self.d
        
        #get structure id data for home and other Nest locations
        for i in range(len(d["structure"].keys())):
            struc_id = d["structure"].keys()[i]
            struc = d["structure"][struc_id]["name"]
            self.strucs[struc_id] = struc
        vc.savePayloadFile("Nest/abodeList.xml",Dictionary[str,str](self.strucs),True)

        #get thermostat device names and id values
        if "device" in d:        
            for x in range(len(d["device"].keys())):
                device_id = d["device"].keys()[x]
                device = d["shared"][device_id]["name"]
                if device =='':
                    device = "thermostat without a label "+str(x+1)
                self.thermos[device_id] = device
            vc.savePayloadFile("Nest/thermoList.xml",Dictionary[str,str](self.thermos),True)
            
        #get protect device names and id values
        if "topaz" in d:            
            for i in range(len(d["topaz"].keys())):
                protect_id = d["topaz"].keys()[i]
                protect = d["topaz"][protect_id]["description"]
                if protect == '':
                    protect = "protect without a label "+str(i+1)
                self.prots[protect_id] = protect
            vc.savePayloadFile("Nest/protectList.xml",Dictionary[str,str](self.prots),True)
                
      
    def getShared(self,device_id,var): #get certain types of thermostat info (e.g. temperature settings and current temp)
        self.readNest()
        d = self.d
        var = var.replace(' ','_')
        
        units = d["device"][device_id]["temperature_scale"]#check if device is using Fahrenheit or Celsius
        deviceInfo = d["shared"][device_id]
                
        if var == "target_temperature":        
            state = deviceInfo["target_temperature_type"] #check state of thermostat("off", "range", "heat","cool") 
            
            if state == "off":
                return "Thermostat is off"

            elif ("heat" or "cool") in state:
                res = deviceInfo[var]
                return self.getTemp(units,res)
            
            elif state == "range":
                res_high = deviceInfo["target_temperature_high"]
                res_low = deviceInfo["target_temperature_low"]
                temps = ''
                for x in (res_low,res_high):
                    temps = self.getTemp(units,x)+', '+temps
                return "is in heat-cool mode. High and low targets are: "+temps.rstrip(', ')
        else:
            res = deviceInfo[var]
            return self.getTemp(units,res)

                
    def getTemp(self,units,temp):

        if (units == "F"):
            temp = temp *1.8 + 32
            return "%0.1f" % temp+" Fahrenheit" #return temp in F, rounded to one decimal place
        else:
            return "%0.1f" % temp+" Celsius" #return temp in C, rounded to one decimal place
                            
            
    def getDeviceInfo(self,id,var): #get other environmental info such as current thermostat mode, home away status etc.
    
        self.readNest()
        if not self.strucs:
            self.getDevices()

        d = self.d
        var = var.replace(' ','_')
        
        if id in self.strucs.keys():#if id comes from a structure
            res = d["structure"][id][var]
            
        else:
            res = d["device"][id][var]

        
        if res == True:
            return "enabled"
            
        elif res == False:
            return "disabled"
            
        else:
            return res
        
    def getProtectInfo(self,protect_id,var): #get Protect-related info
        
        #Nest returns battery levels 0 (Exc) to 4 (Bad). Here, translated to meaningful labels.
        bat_health = ['Excellent','Very good','OK','Low','Very low']
        
        self.readNest()
        d = self.d
        var = var.replace(' ','_')
        
        if var == "battery_health_state":
            if protect_id == None:#if you pass parameter "None" rather than an ID, will check all units
                self.getDevices()
                bats_state_list = []#this list will store states of all batteries

                for key,val in self.prots.iteritems():#iterates through all protect units
                    res = d["topaz"][key][var]#retrieves battery healt for each protect unit
                    bats_state_list.append(val+": "+bat_health[res])#adds each unit name: bat_level to list.
                vc.setResultList(List[str](bats_state_list))#returns {Match.#} list where {#M} is total num of Protects. Each match is: "name: level".
                return
                
            else:#checks level of specific unit (if you pass a protect id to the function)
                level = d["topaz"][protect_id][var]
                res = bat_health[level]
                return res
        
        #return results for other Protect variables.
        res = d["topaz"][protect_id][var]
        
        if res == True:
            return "enabled"
            
        elif res == False:
            return "disabled"
            
        else:
            return res
                    

myNest = NestVC()
