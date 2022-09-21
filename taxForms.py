"""
Tax Forms
"""

#Super class with basic layout for all the tax forms

#Name of the employer/company/deduction
#Amount

#All the other forms (subclasses) inherit from this class

class TaxForms:                 
    
    def __init__(self, name):           #Set name
        
        self.__name = name
        self.__amt = 0
        
    def setAmount(self, amount):        #Set amount
        
        self.__amt = amount
        
    def getAmount(self):                #Get amount
        
        return self.__amt

#-------------------------------------------------------------------------------------
#Sub-classes
#-------------------------------------------------------------------------------------
#T4
#Set and get the vaious values given in the T4

#TODO: add functionality for EI earnings and CPP earnings

class T4(TaxForms):
    
    def __init__(self, name):
        
        self.__empInc = 0
        self.__taxDed = 0
        self.__cpp = 0
        # self.__eiErn = 0
        # self.__cppErn = 0
        self.__eiPrem = 0
        self.__unionDues = 0
        TaxForms.__init__(self, name)
        
    def set_empInc(self, empInc):
        self.__empInc = empInc
        
    def set_taxDed(self, taxDed):
        self.__taxDed = taxDed
    
    def set_cpp(self, cpp):
        self.__cpp = cpp
        
    # def set_eiErn(self, eiErn):
    #     self.__eiErn = eiErn
        
    # def set_cppErn(self, cppErn):
    #     self.__cppErn = cppErn
    
    def set_eiPrem(self, eiPrem):
        self.__eiPrem = eiPrem
    
    def set_unionDues(self, unionDues):
        self.__unionDues = unionDues
    
    def get_eInc(self):
        return self.__empInc
    
    def get_taxDed(self):
        return self.__taxDed
    
    def get_cpp(self):
        return self.__cpp
    
    def get_eiPrem(self):
        return self.__eiPrem
    
    def get_unionDues(self):
        return self.__unionDues
    
#-------------------------------------------------------------------------------------
#RRSP
#Set the time period for the RRSP contribution
    
class RRSP(TaxForms):
    
    def __init__(self, name):
        
        TaxForms.__init__(self, name)
        
    def timePeriod(self,tp):
        self.__tp = tp
        
    
#-------------------------------------------------------------------------------------
#Capital gains, capital losses and other deductions
#The same class si used for all 3 because they have the same attributes
        
class CapitalGains(TaxForms):
    
    def __init__(self, name):
        
        TaxForms.__init__(self, name)

#-------------------------------------------------------------------------------------
#T2202A
#Set and get the year and number of months      
  
class T2202A(TaxForms):
    
    def __init__(self, name):
        
        TaxForms.__init__(self, name)
    
    def set_t22year(self, year):
        self.__t22year = year
        
    def set_months(self, months):
        self.__months = months
    
    def get_t22year(self):
        return self.__t22year
    
    def get_months(self):
        return self.__months
    
#-------------------------------------------------------------------------------------
#T4A

#TODO: Add functionality for a T4A

#Checks if the user was an eligible full time/ part time student for the year of the T4A
#If not, calculates what part of the income (T4A) will be taxable

# class T4A(T2202A):
    
#     def __init__(self, name):
        
#         T2202A.__init__(self, name)
        
#     def set_t4ayear(self, year):
#         self.__t4ayear = year
    
#     def calc_elig(self):
#         self.__y = T2202A.get_t22year()
        
#         yr = (self.__y, (self.__y - 1), (self.__y + 1))
        
#         if self.__t4ayear != all(yr):
#             return 1
    
        