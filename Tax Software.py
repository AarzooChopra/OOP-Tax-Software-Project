"""
Personal Tax Software - Ontario, 2021

1 = T4
2 = RRSP
3 = Capital Gains
4 = Capital Losses
5 = T2202A
6 = Other Deductions
"""

import taxForms as tf
import calcTax as ct
import fedTaxCredit as ftc
import personalInfo as pi

def main():
    
    print('\nWelcome to the Ontario personal tax calculator\n')
    
    pInfo = info()
    
    c = inputValInt('Exit = 0\nT4 = 1\nRRSP = 2\nCapital Gains = 3\n' +
                  'Capital Losses = 4\nT2202A = 5\nOther Deductions/Expenses = 6: ')
    
    t4,rrsplst,cglst,t2202a,ded,unusedCred = choice(c)                  #Call choice()
    
    totInc, totTaxDed, totCpp, totEiPrem, totUnionDues = calcT4(t4)     #Call calcT4()
    
    #Call calc()
    totRRSP = calc(rrsplst)
    totCg = calc(cglst)
    totFees = calc(t2202a)
    totDed = calc(ded)
    
    #Call fedTaxCred()
    enhancedCpp, fedCred, baseCpp = fedTaxCred(totInc,totCpp,totEiPrem,totFees)
    
    totCg = capGainLoss(totCg)                                          #Call capGainLoss()
    
    netInc = netIncome(totInc,totRRSP,totCg,totDed,totUnionDues,enhancedCpp) #Call netIncome()
    
    totTax, fedTax, provTax = calcTax(netInc)                           #Call calcTax()
    
    #Call totFedCred() and totProvCred()
    totfc = totFedCred(totInc,totCpp,totEiPrem,fedCred,totFees,fedTax,unusedCred)
    totpc = totProvCred(baseCpp,totEiPrem)  
    
    hlthPrem = healthPrem(netInc)                                       #Call healthPrem
    
    ref = refund(totTax, totTaxDed, totfc, totpc, hlthPrem)             #Call refund
    
    file(pInfo,totInc,totRRSP,totCg,totUnionDues,enhancedCpp,netInc,totfc,totpc,totTaxDed,ref)
    
    print('\nYour ' + ref[0] + ' is $' + format(ref[1], '0.2f'))
    
#-------------------------------------------------------------------------------------
#Prompts the user for personal info and stores it in an object
#Name, address, SIN, date of birth, marital status

def info():
    
    print('Identification Information:')
    
    fname = inputValStr('First Name: ')             #Call inputValStr
    lname = inputValStr('Last Name: ')
    
    idInfo = pi.PersonalInfo(fname,lname)           #Create object to store info
    
    mAdrs = input('Mailing Address: ')
    
    city = inputValStr('City: ')
    
    pCode = input('Postal Code: ')
    
    pCode = editStr(pCode)                          #Call editStr
    
    #Check if postal code is valid (6 characters)
    
    #TODO: Add input validation to make sure the alphabets and digits are in the right places
    
    while len(pCode) != 6:
        
        pCode = inval(pCode, 'Postal Code: ')
    
    idInfo.set_adrs(mAdrs, city, pCode)
    
    sin = input('SIN: ')
    
    sin = editStr(sin)
    
    #Check if SIN is valid (9 digits)
    while sin.isdigit() == False or len(sin) != 9:
        
        sin = inval(sin,'SIN: ')
        
    idInfo.set_sin(sin)
    
    dob = input('Date of Birth (YYYY MM DD): ')
    
    dob = editStr(dob)
    
    #Check if date of birth is valid (8 digits)
    
    #TODO: Add input validation to make sure the format is YYYY MM DD
    
    while dob.isdigit() == False or len(dob) != 8:
        
        dob = inval(dob,'Date of Birth (YYYY MM DD): ')
    
    dobY = dob[: 4] 
    dobM = dob[4:6]
    dobD = dob[6 :]
    
    dob = dobY + ' ' + dobM + ' ' + dobD
    
    idInfo.set_dob(dob)
    
    #Call inputValInt()
    mStatus = inputValInt('Marital Status on December 31, 2021: \n' + 
                    'Married = 1\nLiving Common Law = 2\nWidowed = 3\nDivorced = 4\n' +
                    'Separated = 5\nSingle = 6: ')
    
    #Check if the user's selection is within the given range of options
    while mStatus < 1 or mStatus > 6:
        
        print('\nInvalid input. Please try again')
        
        mStatus = inputValInt('Marital Status on December 31, 2021: \n' + 
                        'Married = 1\nLiving Common Law = 2\nWidowed = 3\nDivorced = 4\n' +
                        'Separated = 5\nSingle = 6: ')
        
    idInfo.set_mStatus(mStatus)
    
    idInfo.store_info()             #Store all the information in a dictionary
    pInfo = idInfo.get_dict()        #Gat personal info
    
    return pInfo
#-------------------------------------------------------------------------------------
#Prompts the user to choose which form/information to enter

#TODO: add functionality for EI earnings and CPP earnings under T4

def choice(c):
    
    t4 = list()
    rrsplst = list() 
    cglst = list()
    t2202a = list()
    ded = list()
    unusedCred = 0
    
    while c != 0:
        
        if c == 1:                  #T4
          
            name = input('Please enter the name of the employer: ')
             
            A = tf.T4(name)         #Create an object in class T4
            
            #Prompt the user to enter T4 info and call inputValFloat to validate the input
            A.set_empInc(inputValFloat('Please enter the employment income in line 14: $'))
            A.set_cpp(inputValFloat('Please enter the income CPP contributions in line 16: $'))
            A.set_eiPrem(inputValFloat('Please enter the EI premiums in line 18: $'))
            A.set_taxDed(inputValFloat('Please enter the income tax deducted in line 22: $'))
            A.set_unionDues(inputValFloat('Please enter the union dues in line 44: $'))
             
            t4.append(A)            #Add the object to a list
              
        elif c == 2:                #RRSP
            
            name = input('Please enter the name of the bank/company: ')
            B = tf.RRSP(name)
            
            t = input('Enter 1 for March 2, 2021 to December 31, 2021\n' +
                      'Enter 2 for January 1, 2022 to March 1, 2022: ')
            
            while t != '1' and t != '2':
                
                print('\nInvalid input. Please try again')
                t = input('Enter 1 for March 2, 2021 to December 31, 2021\n' +
                          'Enter 2 for January 1, 2022 to March 1, 2022: ')
            
            B.timePeriod(t)
            B.setAmount(inputValFloat('Please enter the total RRSP contribution: $'))
            
            rrsplst.append(B)
            
            
        elif c == 3:                #Capital Gains
            
            name = input('Please enter the name of the gain: ')
            C = tf.CapitalGains(name)
            
            C.setAmount(inputValFloat('Please enter the capital gain amount: $'))
            
            cglst.append(C)
            
        elif c == 4:                #Capital Losses
            
            name = input('Please enter the name of the loss: ')
            C = tf.CapitalGains(name)
            
            C.setAmount(-abs(inputValFloat('Please enter the capital loss amount: $')))
            
            #Capital gains and losses are stored in the same list as 
            #capital losses can be taken as negative capital gains    
            
            cglst.append(C)
        
        elif c == 5:                #T2202A
            
            if len(t2202a) == 0:        #Check if user has already entered a T2202A
                name = input('Please enter the name of the institution: ')
                D = tf.T2202A(name)
                
                D.set_months(inputValInt('Please enter the total number of months: '))
                D.setAmount(inputValFloat('Please enter the eligible tuition fees amount: $'))
                
                if unusedCred == 0:     
                    unusedCred = inputValFloat('Please enter any unused tuition credits: $')
                
                t2202a.append(D)
            
            else:
                print('\nYou can only add 1 T2202A per year. Please choose another option.')
                
        elif c == 6:                #Other Deductions
            
            name = input('Please enter the name of the deduction/expense: ')
            E = tf.CapitalGains(name)
            
            E.setAmount(inputValFloat('Please enter the deduction/expense amount: $'))
            
            ded.append(E)
        
        #Prompt the user for the choice again in case there are multiple forms
        c = inputValInt('Exit = 0\nT4 = 1\nRRSP = 2\nCapital Gains = 3\n' +
                      'Capital Losses = 4\nT2202A = 5\nOther Deductions/Expenses = 6: ')
    
    return t4,rrsplst,cglst,t2202a,ded,unusedCred

#-------------------------------------------------------------------------------------
#Calculates the net income/taxable income
#TODO: Differentiate between net and taxable income
    
def netIncome(totInc,totRRSP,totCg,totDed,totUnionDues,enhancedCpp):
    
    netIncome = totInc - totRRSP + (0.5 * totCg) - totDed - totUnionDues - enhancedCpp
    
    return netIncome

#-------------------------------------------------------------------------------------
#Calculates the total of all the T4s entered for various fields
    
def calcT4(t4):
    
    length = len(t4)
    index = 0
    totInc = 0
    totTaxDed = 0
    totCpp = 0
    totEiPrem = 0
    totUnionDues = 0
    
    #Calculates the sum of all the elements in the list
    #Calls the required method to get the correct value
    while index != length:
        
        totInc += t4[index].get_eInc()
        totTaxDed += t4[index].get_taxDed()
        totCpp += t4[index].get_cpp()
        totEiPrem += t4[index].get_eiPrem()
        totUnionDues += t4[index].get_unionDues()
        index += 1
    
    return totInc, totTaxDed, totCpp, totEiPrem, totUnionDues

#-------------------------------------------------------------------------------------
#Calculates the total of all the elements in the list
#Used for RRSP, capital gains/losses, T2202A and other deductions

def calc(lst):
    
    length = len(lst)
    index = 0
    tot = 0
    
    while index != length:    
        tot += lst[index].getAmount()
        index += 1
    
    return tot

#-------------------------------------------------------------------------------------
#Calculates the federal, provincial and total tax

def calcTax(netInc):
    
    fedTax = federal(netInc)            #Call federal()
    provTax = provincial(netInc)        #Call provincial()
    totTax = fedTax + provTax           #Calculate total tax
    
    return totTax, fedTax, provTax

#-------------------------------------------------------------------------------------
#Calculates federal tax
    
def federal(totInc):
    
    A = ct.CalcTax(totInc,'f')          #'f' specifies federal tax is needed
    tax = A.calc_tax()                  #Call the calc_tax method
    
    return tax

#-------------------------------------------------------------------------------------
#Calculates provincial tax

def provincial(totInc):
    
    A = ct.CalcTax(totInc,'p')          #'p' specifies provincial tax is needed
    tax = A.calc_tax()
    
    return tax

#-------------------------------------------------------------------------------------
#Calculates intermediate federal tax credits, basic personal amount, 
#EI premium, Canada employment amount, enhanced cpp and base cpp

#TODO: Combine fedTaxCred() and totFedCred() into one function

def fedTaxCred(totInc,totCpp,totEiPrem,totFees):
    
    A = ftc.FedTaxCredit(totInc,totCpp,totEiPrem)
    bpa = A.calc_bpa()
    baseCpp, enhancedCpp = A.calc_cpp()
    eiPrem = A.calc_eiPrem()
    canEmpAmt = A.calc_can_emp_amt()
    
    fedCred = bpa + baseCpp + eiPrem + canEmpAmt
    
    return enhancedCpp, fedCred, baseCpp

#-------------------------------------------------------------------------------------
#Calculates total federal tax credits

def totFedCred(totInc,totCpp,totEiPrem,fedCred,totFees,fedTax,unusedCred):
    
    taxCredRate = 0.15
    A = ftc.FedTaxCredit(totInc,totCpp,totEiPrem)
    
    tuitionCred = A.calc_tui_cred(fedCred,totFees,fedTax,unusedCred)
    
    totfc = (fedCred + tuitionCred) * taxCredRate     
    
    return totfc

#-------------------------------------------------------------------------------------
#Calculates total provincial tax credits

def totProvCred(baseCpp, totEiPrem):
    
    taxCredRate = 0.0505
    bpa = 10880
    
    totpc = (bpa + baseCpp + totEiPrem) * taxCredRate
    
    return totpc

#-------------------------------------------------------------------------------------
#Calculates health premium

def healthPrem(netInc):
    
    A = ct.HealthPrem(netInc)
    
    hlthPrem = A.get_health_prem()
    
    return hlthPrem

#-------------------------------------------------------------------------------------
#Calculate the total capital gain/loss

def capGainLoss(totCg):
    
    A = ct.CapGainLoss(totCg)
    
    totCg = A.cap_gain_loss()
    
    return totCg

#-------------------------------------------------------------------------------------
#Calculates the refund or balance owing

def refund(totTax, totTaxDed, totfc, totpc, hlthPrem):
    
    amount = abs((totTax - totfc - totpc + hlthPrem) - totTaxDed)
    
    if amount > 2:                  #Check if amount is less than $2
        if totTax > totTaxDed:
            status = 'Balance Owing'
            
        else:
            status = 'Refund'
            
    else:
        status = 'Refund/Balance Owing'
        amount = 0
    
    ref = (status,amount)
    
    return ref

#-------------------------------------------------------------------------------------
#Write information to a file

#TODO: Make the file more detailed

def file(pInfo,totInc,totRRSP,totCg,totUnionDues,enhancedCpp,netInc,totfc,totpc,totTaxDed,ref):
    
    outfile = open('Tax_Summary.txt', 'w')
    
    #Write personal info to file
    outfile.write('Name: ' + pInfo.get('Name') + '\n')
    outfile.write('Address: ' + pInfo.get('Address') + '\n')
    outfile.write('SIN: ' + pInfo.get('SIN') + '\n')
    outfile.write('Date of Birth: ' + pInfo.get('DOB') + '\n')
    outfile.write('Marital Status: ' + pInfo.get('Marital Status') + '\n\n')
    
    #Write tax return details to file
    outfile.write('Employment Income = $' + format(totInc, '0.2f') + '\n')
    outfile.write('RRSP Contribution = $' + format(totRRSP, '0.2f') + '\n')
    outfile.write('Capital Gains/Losses Applied = $' + format(totCg, '0.2f') + '\n')
    outfile.write('Union Dues = $' + format(totUnionDues, '0.2f') + '\n')
    outfile.write('Enhanced CPP = $' + format(enhancedCpp, '0.2f') + '\n')
    outfile.write('Net Income = $' + format(netInc, '0.2f') + '\n')
    outfile.write('Total Federal Tax Credits = $' + format(totfc, '0.2f') + '\n')
    outfile.write('Total Provincial Tax Credits = $' + format(totpc, '0.2f') + '\n')
    outfile.write('Total Tax Deducted = $' + format(totTaxDed, '0.2f') + '\n\n')
    outfile.write('Your ' + ref[0] + ' is $' + format(ref[1], '0.2f'))
    
    outfile.close()
    
#-------------------------------------------------------------------------------------
#Input validation and processing
#Make sure the input is in the right format
#-------------------------------------------------------------------------------------
#Edit the input to remove any extra spaces and/or unwanted special characters

def editStr(string):
    
    string = string.strip()
    string = string.replace('-', '')
    string = string.replace(' ','')
    string = string.replace('/','')
    string = string.replace('.','')
    string = string.replace(',','')
    
    return string

#-------------------------------------------------------------------------------------
#Print 'Invalid input' and pprompt the user to enter the value again

def inval(x, y):
    
    print('\nInvalid input. Please try again')
    x = input(y)
    x = editStr(x)
    
    return x

#-------------------------------------------------------------------------------------
#Make sure the input is a floating point number

def inputValFloat(x):
    
    while True:    
        try:
            x = float(input(x))
            
        except ValueError:
            print('\nInvalid input. Please try again')
            
        else:
            break
        
    return float(x)

#-------------------------------------------------------------------------------------
#Make sure the input is an integer

def inputValInt(x):
    
    while True:    
        try:
            x = int(input(x))
            
        except ValueError:
            print('\nInvalid input. Please try again')
            
        else:
            break
        
    return int(x)

#-------------------------------------------------------------------------------------
#Make sure the input is a string of alphabets

def inputValStr(y):
    
    x = input(y)
    x = x.rstrip()
    
    while x.isalpha() == False:
        print('\nInvalid input. Please try again')
        x = input(y)
        x = x.rstrip()
    
    return x

main()