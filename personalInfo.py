"""
Personal Info
"""

class PersonalInfo:
    def __init__(self, fname, lname):
        self.__fname = fname
        self.__lname = lname
        self.__mAdrs = None
        self.__city = None
        self.__pCode = None
        self.__prov = 'ON'
        self.__sin = None
        self.__dob = None
        self.__mStatus = None
        
    def set_adrs(self,mAdrs,city,pCode):
        
        #Set the address, city and postal code
        self.__mAdrs = mAdrs
        self.__city = city
        self.__pCode = pCode
        
        #Concatenate the strings and save the complete address in one attribute
        self.__adrs = self.__mAdrs + ', ' + self.__city + ', ' + self.__pCode + ', ' + self.__prov
        
    def set_sin(self,sin):
        self.__sin = sin                #Set the SIN
        
    def set_dob(self,dob):
        self.__dob = dob                #Set the date of birth
        
    def set_mStatus(self,mStatus):
        self.__mStatus = mStatus    
        
        #Set the marital status according to the option chosen 
        if self.__mStatus == 1: self.__mStatus = 'Married'
        elif self.__mStatus == 2: self.__mStatus = 'Living Common Law'
        elif self.__mStatus == 3: self.__mStatus = 'Widowed'
        elif self.__mStatus == 4: self.__mStatus = 'Divorced'
        elif self.__mStatus == 5: self.__mStatus = 'Separated'
        else: self.__mStatus = 'Single'
    
    def store_info(self):
        
        #Store all the personal info in a dictionary
        
        self.__info = {'Name' : self.__fname + ' ' + self.__lname,
                       'Address' : self.__adrs,
                       'SIN' : self.__sin,
                       'DOB' : self.__dob,
                       'Marital Status' : self.__mStatus}
    
    def get_dict(self):                 #Get the dictionary
        return self.__info
    