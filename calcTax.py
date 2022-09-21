"""
Calculate Tax
"""

#Various values for tax and health premium calculations are stored in tuples

#-------------------------------------------------------------------------------------
#Calculates the tax based on the tax brackets

class CalcTax:
    def __init__(self,netInc,t):
        
        self.__netInc = netInc
        self.__t = t
        self.__tax = 0
        
    def set_fedTax(self):                                   #Define federal tax brackets
        self.__b = (49020,98040,151978,216511)              #Upper limit of tax bracket
        self.__percent = (0.15,0.205,0.26,0.2932,0.33)      #Percentage for each tax bracket
        return self.__b, self.__percent
    
    def set_provTax(self):                                  #Defines provincial tax brackets
        self.__b = (45142,90287,150000,220000)
        self.__percent = (0.0505,0.0915,0.1116,0.1216,0.1316)
        return self.__b, self.__percent
    
    def calc_tax(self):
        
        #Check if federal or provincial tax is needed
        if self.__t == 'f':
            self.__b, self.__percent = self.set_fedTax()
        
        elif self.__t == 'p':
            self.__b, self.__percent = self.set_provTax()
        
        #Calculate tax
        if self.__netInc > self.__b[0]:
            self.__tax = self.__b[0] * self.__percent[0]
            self.__remInc = self.__netInc - self.__b[0]
            
            if self.__netInc > self.__b[1]:
                self.__tax += (self.__b[1]-self.__b[0]) * self.__percent[1]
                self.__remInc -= self.__b[1]-self.__b[0]
                
                if self.__netInc > self.__b[2]:
                    self.__tax += (self.__b[2]-self.__b[1]) * self.__percent[2]
                    self.__remInc -= self.__b[2]-self.__b[1]
                    
                    if self.__netInc > self.__b[3]:
                        self.__tax += (self.__b[3]-self.__b[2]) * self.__percent[3]
                        self.__remInc -= self.__b[3]-self.__b[2]
                        self.__tax += self.__remInc * self.__percent[4] 
                        
                    else:
                        self.__tax += self.__remInc * self.__percent[3]
                    
                else:
                    self.__tax += self.__remInc * self.__percent[2]
            else:
                self.__tax += self.__remInc * self.__percent[1]
                
        return self.__tax

#-------------------------------------------------------------------------------------
#Calculates the health premium based on income

class HealthPrem:
    def __init__(self,netInc):
        
        self.__sub = (20000, 25000, 36000, 38500, 48000, 48600, 72000, 72600, 200000, 200600)
        self.__add = (0, 300, 450, 600, 750, 900)
        self.__mul = (0.06, 0.25)
        self.__netInc = netInc
        
    def get_health_prem(self):
        if self.__netInc <= self.__sub[0]:
            self.__hlthPrem = self.__add[0]
            
        elif self.__netInc > self.__sub[0] and self.__netInc <= self.__sub[1]:
            self.__hlthPrem = (self.__netInc - self.__sub[0]) * self.__mul[0]
            
        elif self.__netInc > self.__sub[1] and self.__netInc <= self.__sub[2]:
            self.__hlthPrem = self.__add[1]
            
        elif self.__netInc > self.__sub[2] and self.__netInc <= self.__sub[3]:
            self.__hlthPrem = ((self.__netInc - self.__sub[2]) * self.__mul[0]) + self.__add[1]
            
        elif self.__netInc > self.__sub[3] and self.__netInc <= self.__sub[4]:
            self.__hlthPrem = self.__add[2]
            
        elif self.__netInc > self.__sub[4] and self.__netInc <= self.__sub[5]:
            self.__hlthPrem = ((self.__netInc - self.__sub[4]) * self.__mul[1]) + self.__add[2]
            
        elif self.__netInc > self.__sub[5] and self.__netInc <= self.__sub[6]:
            self.__hlthPrem = self.__add[3]
            
        elif self.__netInc > self.__sub[6] and self.__netInc <= self.__sub[7]:
            self.__hlthPrem = ((self.__netInc - self.__sub[6]) * self.__mul[1]) + self.__add[3]
            
        elif self.__netInc > self.__sub[7] and self.__netInc <= self.__sub[8]:
            self.__hlthPrem = self.__add[4]
            
        elif self.__netInc > self.__sub[8] and self.__netInc <= self.__sub[9]:
            self.__hlthPrem = ((self.__netInc - self.__sub[8]) * self.__mul[1]) + self.__add[4]
            
        else:
            self.__hlthPrem = self.__add[5]
            
        return self.__hlthPrem

#-------------------------------------------------------------------------------------
#Calculates the amount of capital gains/losses to be applies
#Loss can't be applied on the same year

#TODO: Add functionality to apply capital loss to previous/future years
    
class CapGainLoss:
    def __init__(self,totCg):
        self.__totCg = totCg
        
    def cap_gain_loss(self):
        if self.__totCg < 0:        #Check if there is net gain or loss
            self.__totCg = 0        #If loss, set amount to 0
            
        return self.__totCg