import tkinter as tk  
# Importing the tkinter library for GUI development
from tkinter import messagebox
# Importing messagebox from tkinter for displaying messages
from time import gmtime, strftime  
# Importing functions to handle time-related tasks

def is_number(s):
    # Function to check if a string can be converted to a number
    try:
        float(s)
        return 1
    except ValueError:
        return 0

def check_acc_nmb(num):
    # Function to check if an account number exists by attempting to open a file with that name
    try:
        fpin = open(num + ".txt", 'r')
    except FileNotFoundError:
        # If the file doesn't exist, display an error message
        messagebox.showinfo("Error", "Invalid Credentials!\nTry Again!")
        return 0
    fpin.close()
    return

def home_return(master):
    # Function to close the current window and return to the main menu
    master.destroy()
    Main_Menu()

def write(master, name, oc, pin):
    # Function to create a new account and save account details

    if (is_number(name)) or (is_number(oc) == 0) or (is_number(pin) == 0) or name == "":
        # If any of the credentials are invalid, display an error message
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        return

    # Read the current account number from the record file
    f1 = open("Accnt_Record.txt", 'r')
    accnt_no = int(f1.readline())
    accnt_no += 1
    f1.close()

    # Update the account number in the record file
    f1 = open("Accnt_Record.txt", 'w')
    f1.write(str(accnt_no))
    f1.close()

    # Save the account details in a new file named with the account number
    fdet = open(str(accnt_no) + ".txt", "w")
    fdet.write(pin + "\n")
    fdet.write(oc + "\n")
    fdet.write(str(accnt_no) + "\n")
    fdet.write(name + "\n")
    fdet.close()

    # Create a transaction record file for the account
    frec = open(str(accnt_no) + "-rec.txt", 'w')
    frec.write("Date                             Credit      Debit     Balance\n")
    frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "     " + oc + "              " + oc + "\n")
    frec.close()

    # Display the newly created account number to the user
    messagebox.showinfo("Details", "Your Account Number is:" + str(accnt_no))
    master.destroy()
    return

def crdt_write(master, amt, accnt, name):
    # Function to credit an amount to the account

    if is_number(amt) == 0:
        # If the amount is not a valid number, display an error message
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        return

    # Open the account file and retrieve the current balance
    fdet = open(accnt + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()

    # Update the balance by adding the credited amount
    amti = int(amt)
    cb = amti + camt
    fdet = open(accnt + ".txt", 'w')
    fdet.write(pin)
    fdet.write(str(cb) + "\n")
    fdet.write(accnt + "\n")
    fdet.write(name + "\n")
    fdet.close()

    # Update the transaction record with the credit operation
    frec = open(str(accnt) + "-rec.txt", 'a+')
    frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "     " + str(amti) + "              " + str(cb) + "\n")
    frec.close()
    
    # Inform the user of successful credit operation
    messagebox.showinfo("Operation Successful!!", "Amount Credited Successfully!!")
    master.destroy()
    return

def debit_write(master, amt, accnt, name):
    # Function to debit an amount from the account

    if is_number(amt) == 0:
        # If the amount is not a valid number, display an error message
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        return

    # Open the account file and retrieve the current balance
    fdet = open(accnt + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()

    if int(amt) > camt:
        # If the requested debit amount exceeds the current balance, display an error message
        messagebox.showinfo("Error!!", "You don't have that amount left in your account\nPlease try again.")
    else:
        # Update the balance by subtracting the debited amount
        amti = int(amt)
        cb = camt - amti
        fdet = open(accnt + ".txt", 'w')
        fdet.write(pin)
        fdet.write(str(cb) + "\n")
        fdet.write(accnt + "\n")
        fdet.write(name + "\n")
        fdet.close()

        # Update the transaction record with the debit operation
        frec = open(str(accnt) + "-rec.txt", 'a+')
        frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "     " + "              " + str(amti) + "              " + str(cb) + "\n")
        frec.close()

        # Inform the user of successful debit operation
        messagebox.showinfo("Operation Successful!!", "Amount Debited Successfully!!")
        master.destroy()
        return

def Cr_Amt(accnt, name):
    # Function to create a window for crediting amount

    creditwn = tk.Tk()
    creditwn.geometry("600x300")
    creditwn.title("Credit Amount")
    creditwn.configure(bg="SteelBlue1")

    # Create and display the title label
    fr1 = tk.Frame(creditwn, bg="blue")
    l_title = tk.Message(creditwn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=2000, padx=600, pady=0, fg="white", bg="blue4", justify="center", anchor="center")
    l_title.config(font=("Arial", "50", "bold"))
    l_title.pack(side="top")

    # Create and display the label and entry field for the credit amount
    l1 = tk.Label(creditwn, relief="raised", font=("Times", 16), text="Enter Amount to be credited: ")
    e1 = tk.Entry(creditwn, relief="raised")
    l1.pack(side="top")
    e1.pack(side="top")

    # Create and display the credit button, binding it to the crdt_write function
    b = tk.Button(creditwn, text="Credit", font=("Times", 16), relief="raised", command=lambda: crdt_write(creditwn, e1.get(), accnt, name))
    b.pack(side="top")

    # Bind the Enter key to trigger the credit operation
    creditwn.bind("<Return>", lambda x: crdt_write(creditwn, e1.get(), accnt, name))

def De_Amt(accnt, name):
    # Function to create a window for debiting amount

    debitwn = tk.Tk()
    debitwn.geometry("600x300")
    debitwn.title("Debit Amount")
    debitwn.configure(bg="SteelBlue1")

    # Create and display the title label
    fr1 = tk.Frame(debitwn, bg="blue")
    l_title = tk.Message(debitwn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=2000, padx=600, pady=0, fg="white", bg="blue4", justify="center", anchor="center")
    l_title.config(font=("Arial", "50", "bold"))
    l_title.pack(side="top")

    # Create and display the label and entry field for the debit amount
    l1 = tk.Label(debitwn, relief="raised", font=("Times", 16), text="Enter Amount to be debited: ")
    e1 = tk.Entry(debitwn, relief="raised")
    l1.pack(side="top")
    e1.pack(side="top")

    # Create and display the debit button, binding it to the debit_write function
    b = tk.Button(debitwn, text="Debit", font=("Times", 16), relief="raised", command=lambda: debit_write(debitwn, e1.get(), accnt, name))
    b.pack(side="top")

    # Bind the Enter key to trigger the debit operation
    debitwn.bind("<Return>", lambda x: debit_write(debitwn, e1.get(), accnt, name))


def disp_bal(accnt):
    # Open the account file in read mode
    fdet = open(accnt + ".txt", 'r')
    # Skip the first line (could be header or irrelevant information)
    fdet.readline()
    # Read the second line which contains the balance
    bal = fdet.readline()
    # Close the file
    fdet.close()
    # Display the balance in a message box
    messagebox.showinfo("Balance", bal)


def disp_tr_hist(accnt):
    # Create a new window for displaying the transaction history
    disp_wn = tk.Tk()
    disp_wn.geometry("900x600")  # Set window size
    disp_wn.title("Transaction History")  # Set window title
    disp_wn.configure(bg="SteelBlue1")  # Set window background color

    # Create a title message for the transaction history window
    fr1 = tk.Frame(disp_wn, bg="blue")
    l_title = tk.Message(disp_wn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=2000,
                         padx=600, pady=0, fg="white", bg="blue4", justify="center", anchor="center")
    l_title.config(font=("Arial", "50", "bold"))
    l_title.pack(side="top")  # Place the title at the top of the window

    # Create and pack the frame
    fr1 = tk.Frame(disp_wn)
    fr1.pack(side="top")

    # Create and pack the label for transaction history
    l1 = tk.Message(disp_wn, text="Your Transaction History:", font=("Times", 16), padx=100, pady=20, width=1000,
                    bg="blue4", fg="SteelBlue1", relief="raised")
    l1.pack(side="top")

    # Create and pack the frame for transaction details
    fr2 = tk.Frame(disp_wn)
    fr2.pack(side="top")

    # Open the account's transaction history file
    frec = open(accnt + "-rec.txt", 'r')
    # Loop through each line in the file and display it as a message in the window
    for line in frec:
        l = tk.Message(disp_wn, anchor="w", text=line, relief="raised", width=2000)
        l.pack(side="top")
    # Create a quit button to close the transaction history window
    b = tk.Button(disp_wn, text="Quit", relief="raised", command=disp_wn.destroy)
    b.pack(side="top")
    # Close the transaction history file
    frec.close()


def logged_in_menu(accnt, name):
    # Create a new window for the logged-in menu
    rootwn = tk.Tk()
    rootwn.geometry("1600x500")  # Set window size
    rootwn.title("CopyAssignment Bank | Welcome - " + name)  # Set window title with user name
    rootwn.configure(background='SteelBlue1')  # Set window background color

    # Create and pack the frame for the title
    fr1 = tk.Frame(rootwn)
    fr1.pack(side="top")

    # Create and pack the title message
    l_title = tk.Message(rootwn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=2000,
                         padx=600, pady=0, fg="white", bg="blue4", justify="center", anchor="center")
    l_title.config(font=("Arial", "50", "bold"))
    l_title.pack(side="top")

    # Create and pack the label showing who is logged in
    label = tk.Label(text="Logged in as: " + name, relief="raised", bg="blue3", font=("Times", 16),
                     fg="white", anchor="center", justify="center")
    label.pack(side="top")

    # Load images for buttons and create buttons with their respective commands
    img2 = tk.PhotoImage(file="credit.gif")
    myimg2 = img2.subsample(2, 2)
    img3 = tk.PhotoImage(file="debit.gif")
    myimg3 = img3.subsample(2, 2)
    img4 = tk.PhotoImage(file="balance1.gif")
    myimg4 = img4.subsample(2, 2)
    img5 = tk.PhotoImage(file="transaction.gif")
    myimg5 = img5.subsample(2, 2)

    b2 = tk.Button(image=myimg2, command=lambda: Cr_Amt(accnt, name))  # Button for credit amount
    b2.image = myimg2
    b3 = tk.Button(image=myimg3, command=lambda: De_Amt(accnt, name))  # Button for debit amount
    b3.image = myimg3
    b4 = tk.Button(image=myimg4, command=lambda: disp_bal(accnt))  # Button to display balance
    b4.image = myimg4
    b5 = tk.Button(image=myimg5, command=lambda: disp_tr_hist(accnt))  # Button to display transaction history
    b5.image = myimg5

    img6 = tk.PhotoImage(file="logout.gif")
    myimg6 = img6.subsample(2, 2)
    b6 = tk.Button(image=myimg6, relief="raised", command=lambda: logout(rootwn))  # Button to logout
    b6.image = myimg6

    # Position the buttons on the window
    b2.place(x=100, y=150)
    b3.place(x=100, y=220)
    b4.place(x=900, y=150)
    b5.place(x=900, y=220)
    b6.place(x=500, y=400)


def logout(master):
    # Display a message box indicating successful logout
    messagebox.showinfo("Logged Out", "You Have Been Successfully Logged Out!!")
    # Close the current window
    master.destroy()
    # Return to the main menu
    Main_Menu()


def check_log_in(master, name, acc_num, pin):
    # Check if the account number is valid
    if (check_acc_nmb(acc_num) == 0):
        master.destroy()  # Destroy the current window
        Main_Menu()  # Return to the main menu
        return

    # Check if the name is not a number and the pin is a number
    if (is_number(name)) or (is_number(pin) == 0):
        # Show an error message if credentials are invalid
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()  # Destroy the current window
        Main_Menu()  # Return to the main menu
    else:
        # Destroy the current window and log in to the user's account
        master.destroy()
        logged_in_menu(acc_num, name)


def log_in(master):
    # Destroy the current window and create a new window for logging in
    master.destroy()
    loginwn = tk.Tk()
    loginwn.geometry("600x300")  # Set window size
    loginwn.title("Log in")  # Set window title
    loginwn.configure(bg="SteelBlue1")  # Set window background color

    # Create and pack the frame for the title
    fr1 = tk.Frame(loginwn, bg="blue")
    l_title = tk.Message(loginwn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=2000,
                         padx=600, pady=0, fg="white", bg="blue4", justify="center", anchor="center")
    l_title.config(font=("Arial", "50", "bold"))
    l_title.pack(side="top")

    # Create and pack the labels and entry fields for name, account number, and PIN
    l1 = tk.Label(loginwn, text="Enter Name:", font=("Times", 16), relief="raised")
    l1.pack(side="top")
    e1 = tk.Entry(loginwn)
    e1.pack(side="top")

    l2 = tk.Label(loginwn, text="Enter account number:", font=("Times", 16), relief="raised")
    l2.pack(side="top")
    e2 = tk.Entry(loginwn)
    e2.pack(side="top")

    l3 = tk.Label(loginwn, text="Enter your PIN:", font=("Times", 16), relief="raised")
    l3.pack(side="top")
    e3 = tk.Entry(loginwn, show="*")
    e3.pack(side="top")

    # Create and pack the submit button with command to check login credentials
    b = tk.Button(loginwn, text="Submit", command=lambda: check_log_in(loginwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    b.pack(side="top")

    # Create and pack the home button to return to the home screen
    b1 = tk.Button(text="HOME", font=("Times", 16), relief="raised", bg="blue4", fg="white", command=lambda: home_return(loginwn))
    b1.pack(side="top")

    # Bind the Return key to the submit action
    loginwn.bind("<Return>", lambda x: check_log_in(loginwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))


def Create():
    # Create a new window for account creation
    crwn = tk.Tk()
    crwn.geometry("600x300")  # Set window size
    crwn.title("Create Account")  # Set window title
    crwn.configure(bg="SteelBlue1")  # Set window background color

    # Create and pack the frame for the title
    fr1 = tk.Frame(crwn, bg="blue")
    l_title = tk.Message(crwn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=2000,
                         padx=600, pady=0, fg="white", bg="blue4", justify="center", anchor="center")
    l_title.config(font=("Arial", "50", "bold"))
    l_title.pack(side="top")

    # Create and pack the labels and entry fields for name, opening credit, and desired PIN
    l1 = tk.Label(crwn, text="Enter Name:", font=("Times", 16), relief="raised")
    l1.pack(side="top")
    e1 = tk.Entry(crwn)
    e1.pack(side="top")

    l2 = tk.Label(crwn, text="Enter opening credit:", font=("Times", 16), relief="raised")
    l2.pack(side="top")
    e2 = tk.Entry(crwn)
    e2.pack(side="top")

    l3 = tk.Label(crwn, text="Enter desired PIN:", font=("Times", 16), relief="raised")
    l3.pack(side="top")
    e3 = tk.Entry(crwn, show="*")
    e3.pack(side="top")

    # Create and pack the submit button to create the account
    b = tk.Button(crwn, text="Submit", font=("Times", 16), command=lambda: write(crwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    b.pack(side="top")

    # Bind the Return key to the submit action
    crwn.bind("<Return>", font=("Times", 16), command=lambda x: write(crwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    return


def Main_Menu():
    # Create the main menu window
    rootwn = tk.Tk()
    rootwn.geometry("1600x500")  # Set window size
    rootwn.title("Bank Management System - CopyAssignment")  # Set window title
    rootwn.configure(background='SteelBlue1')  # Set window background color

    # Create and pack the frame for the title
    fr1 = tk.Frame(rootwn)
    fr1.pack(side="top")

    # Create and pack the title message
    l_title = tk.Message(text="BANK MANAGEMENT SYSTEM ", relief="raised", width=2000,
                         padx=600, pady=0, fg="white", bg="blue4", justify="center", anchor="center")
    l_title.config(font=("Verdana", "40", "bold"))
    l_title.pack(side="top")

    # Load images for buttons and create buttons with their respective commands
    imgc1 = tk.PhotoImage(file="new.gif")
    imglo = tk.PhotoImage(file="login.gif")
    imgc = imgc1.subsample(2, 2)
    imglog = imglo.subsample(2, 2)

    b1 = tk.Button(image=imgc, command=Create)  # Button to create a new account
    b1.image = imgc
    b2 = tk.Button(image=imglog, command=lambda: log_in(rootwn))  # Button to log in
    b2.image = imglog

    img6 = tk.PhotoImage(file="quit.gif")
    myimg6 = img6.subsample(2, 2)

    # Button to quit the application
    b6 = tk.Button(image=myimg6, command=rootwn.destroy)
    b6.image = myimg6

    # Position the buttons on the window
    b1.place(x=800, y=300)
    b2.place(x=800, y=200)
    b6.place(x=920, y=400)

    # Run the main loop of the window
    rootwn.mainloop()


Main_Menu()  
# Call the main menu function to start the application
