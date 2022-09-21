# OOP-Tax-Software-Project

The program is a personal tax calculator for Ontario (2021). It takes various inputs, performs tax related calculations and determines the amount of refund/balance owing. In addition, it also takes the user's personal information and stores it in a dictionary so that the required field can be accessed when needed. Finally, it outputs a summary in a file called 'Tax_Summary.txt'.

The program takes the farrowing inputs:
Personal Info: Name, address, SIN, date of birth and marital status
Tax Forms: T4, RRSP, Capital Gains, Capital Losses, T2202A and other deductions

It also has the ability to take multiples of any of the forms except the T2202A (only one T2202A is allowed per tax year).

In the case of multiple instances of a form, the program adds the appropriate fields and uses them for further calculations.

After that, the net income, health premium and the provincial and federal tax credits are calculated using the information provided. These are then further used to calculate if there is a refund or a balance owing and how much. 

As CRA does not process a refund or balance owing of less than $2, the program also ignores it if the amount is less than that.

Finally, a summary is written to a file which can be saved for the user's records.

*****************************************************************************************************

To use this program, the user simply has to follow the instructions given on the screen and type in the required information when prompted. The order in which the user enters the forms does not matter.

Most of the inputs are being validated, so it safeguards against the user entering the information in a format that is not supported.
