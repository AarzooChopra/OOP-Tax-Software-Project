"""
Calculate Non-Refundable Federal Tax Credits
"""

#TODO: Add other federal credits

class FedTaxCredit:                     
    def __init__(self,empInc,cpp,eiPrem):
        
        #Set the various values to calculate federal tax credits
        self.__empInc = empInc
        self.__bpa = 0
        self.__low = 151978
        self.__high = 216511
        self.__baseAmt = 12421
        self.__suppAmt = 1387
        self.__cpp = cpp
        self.__eiPrem = eiPrem
        self.__canEmpAmt = 1257
        
    def calc_bpa(self):             #Calculate basic personal amount
        if self.__empInc <= self.__low:
            self.__bpa = 13808
            
        elif self.__empInc >= self.__high:
            self.__bpa = 12421
            
        else:
            self.__calc = ((self.__empInc - self.__low)/64533) * 1387
            self.__calc2 = self.__suppAmt - self.__calc
            
            if self.__calc2 < 0:
                self.__calc2 = 0
                
            self.__bpa = self.__baseAmt + self.__calc2
        
        return self.__bpa
    
    def calc_cpp(self):             #Calculate base CPP and enhanced CPP
        self.__percent = 0.908257
        
        self.__baseCpp = self.__cpp * self.__percent
        self.__enhancedCpp = self.__cpp - self.__baseCpp
        
        return self.__baseCpp, self.__enhancedCpp
    
    def calc_eiPrem(self):          #Calculate EI premium
        self.__max = 889.54
        
        if self.__eiPrem > self.__max:
            self.__eiPrem = self.__max
            
        return self.__eiPrem
    
    def calc_can_emp_amt(self):     #Calculate Canada employment amount
        
        if self.__empInc < self.__canEmpAmt:
            self.__canEmpAmt = self.__empInc
            
        return self.__canEmpAmt
    
    def calc_tui_cred(self,fedCred,totFees,fedTax,unusedCred):      #Calculate tuition credits
        self.__fedCred = fedCred
        self.__totFees = totFees
        self.__fedTax = fedTax
        self.__unusedCred = unusedCred
        
        self.__tuitionCred = self.__totFees 
        
        self.__l15 = (self.__fedTax / 0.15) - self.__fedCred - self.__unusedCred
        
        if self.__l15 <= self.__totFees:
            return self.__unusedCred + self.__l15
        
        else:
            return self.__unusedCred + self.__totFees
        
        
        