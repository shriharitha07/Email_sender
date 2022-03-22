from tkinter import *
from tkinter import messagebox, filedialog
from email.message import EmailMessage
import smtp
import os
import imghdr
import pandas
check=False

def browse():
    global final_emails
    path=filedialog.askopenfilename(initialdir='c:/',title='Select Excel File')
    if path=='':
        messagebox.showerror('Error','Please select an Excel File')

    else:
        data=pandas.read_excel(path)
        if 'Email' in data.columns:
            emails=list(data['Email'])
            final_emails=[]
            for i in emails:
                if pandas.isnull(i)==False:
                    final_emails.append(i)

            if len(final_emails)==0:
                messagebox.showerror('Error','File does not contain any email addresses')

            else:
                toEntryField.config(state=NORMAL)
                toEntryField.insert(0,os.path.basename(path))
                toEntryField.config(state='readonly')
                totalLabel.config(text='Total: '+str(len(final_emails)))
                sentLabel.config(text='Sent:')
                leftLabel.config(text='Left:')
                failedLabel.config(text='Failed:')


def button_check():
    if choice.get()=='multiple':
        browseButton.config(state=NORMAL)
        toEntryField.config(state='readonly')

    if choice.get()=='single':
        browseButton.config(state=DISABLED)
        toEntryField.config(state=NORMAL)

def attachment():
    global filename, filetype, filepath, check
    check = True
    filepath = filedialog.askopenfilename(initialdir='c:/', title='Select File')
    filetype = filepath.split('.')
    filetype = filetype[1]
    filename = os.path.basename(filepath)
    textarea.insert(END, f'\n{filename}\n')

def sendingEmail(toAddress,subject,body):
    f = open('credentials.txt', 'r')
    for i in f:
        credentials = i.split(',')

    message = EmailMessage()
    message['subject'] = subject
    message['to'] = toAddress
    message['from'] = credentials[0]
    message.set_content(body)

    if check:
        if filetype == 'png' or filetype == 'jpg' or filetype == 'jpeg':
            f = open(filepath, 'rb')
            file_data = f.read()
            subtype = imghdr.what(filepath)

            message.add_attachment(file_data, maintype='image', subtype=subtype, filename=filename)

        else:
            f = open(filepath, 'rb')
            file_data = f.read()
            message.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=filename)

    s = smtp.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(credentials[0], credentials[1])
    s.send_message(message)
    x = s.ehlo()
    if x[0] == 250:
        return 'sent'
    else:
        return 'failed'

def send_email():
    if toEntryField.get()=='' or subjectEntryField.get()=='' or textarea.get(1.0,END)=='\n':
        messagebox.showerror('Error','All Fields Are Required',parent=root)

    else:
        if choice.get()=='single':
            result = sendingEmail(toEntryField.get(), subjectEntryField.get(), textarea.get(1.0, END))

            if result == 'sent':
                messagebox.showinfo('Success', 'Email is sent successfulyy')

            if result == 'failed':
                messagebox.showerror('Error', 'Email is not sent.')

        if choice.get() == 'multiple':
            sent = 0
            failed = 0
            for x in final_emails:
                result = sendingEmail(x, subjectEntryField.get(), textarea.get(1.0, END))
                if result == 'sent':
                    sent += 1
                if result == 'failed':
                    failed += 1

                totalLabel.config(text='')
                sentLabel.config(text='Sent:' + str(sent))
                leftLabel.config(text='Left:' + str(len(final_emails) - (sent + failed)))
                failedLabel.config(text='Failed:' + str(failed))

                totalLabel.update()
                sentLabel.update()
                leftLabel.update()
                failedLabel.update()

            messagebox.showinfo('Success', 'Emails are sent successfully')


def settings():
    def clear1():
        fromEntryField.delete(0, END)
        passwordEntryField.delete(0, END)

    def save():
        if fromEntryField.get() == '' or passwordEntryField.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=root1)
        else:
            f = open('credentials.txt', 'w')
            f.write(fromEntryField.get() + ',' + passwordEntryField.get())
            f.close()
            messagebox.showinfo('Information', 'CREDENTIALS SAVED SUCCESSFULLY', parent=root1)

    root1 = Toplevel()
    root1.title('Settings')
    root1.geometry('650x340+350+90')

    root1.config(bg='seashell3')

    Label(root1, text='  CREDENTIAL SETTINGS', image=logoImage, compound=LEFT, font=('goudy old style', 15, 'bold'),
          fg='black', bg='seashell3').grid(padx=160)

    fromLabelFrame = LabelFrame(root1, text='From (Email Address)', font=('goudy old style', 16, 'bold'), bd=5,
                                fg='blue4',
                                bg='seashell3')
    fromLabelFrame.grid(row=1, column=0, pady=20)

    fromEntryField = Entry(fromLabelFrame, font=('goudy old style', 13, 'bold'), width=30)
    fromEntryField.grid(row=0, column=0)

    passwordLabelFrame = LabelFrame(root1, text='Password', font=('goudy old style', 16, 'bold'), bd=5,
                                    fg='blue4',
                                    bg='seashell3')
    passwordLabelFrame.grid(row=2, column=0, pady=20)

    passwordEntryField = Entry(passwordLabelFrame, font=('goudy old style', 13, 'bold'), width=30,show='*')
    passwordEntryField.grid(row=0, column=0)

    Button(root1, text='SAVE', font=('times new roman', 12, 'bold'), cursor='hand2', bg='azure', fg='black'
           ,command=save ).place(x=230, y=280)
    Button(root1, text='CLEAR', font=('times new roman', 12, 'bold'), cursor='hand2', bg='azure', fg='black'
           ,command=clear1).place(x=340, y=280)

    f=open('credentials.txt','r')
    for i in f:
        credentials=i.split(',')

    fromEntryField.insert(0,credentials[0])
    passwordEntryField.insert(0,credentials[1])


    root1.mainloop()


def iexit():
    result=messagebox.askyesno('Notification', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def clear():
    toEntryField.delete(0,END)
    subjectEntryField.delete(0,END)
    textarea.delete(1.0,END)

root = Tk()
root.title('Email Sender App')
root.geometry('780x620+100+50')
root.resizable(0,0)
root.config(bg='seashell2')

titleFrame = Frame(root, bg='seashell2')
titleFrame.grid(row=0, column=0)
logoImage = PhotoImage(file='email.png')
titleLabel = Label(titleFrame, text='  EMAIL SENDER', image=logoImage, compound=LEFT, font=('Goudy Old Style', 17, 'bold'),
                   bg='seashell2', fg='blue4')
titleLabel.grid(row=0, column=0)
settingImage = PhotoImage(file='setting.png')

Button(titleFrame, image=settingImage, bd=0, bg='seashell2', cursor='hand2', activebackground='seashell2'
       ,command=settings).grid(row=0,column=1,padx=20)

chooseFrame=Frame(root,bg='seashell2')
chooseFrame.grid(row=1,column=0)
choice=StringVar()

singleRadioButton=Radiobutton(chooseFrame,text='Single', font=('Goudy Old Style',13,'bold'),
                              variable=choice,value='single',bg='seashell2',activebackground='seashell2',command=button_check)
singleRadioButton.grid(row=0,column=0,padx=20)

multipleRadioButton=Radiobutton(chooseFrame,text='Multiple', font=('Goudy Old Style',13,'bold'),
                              variable=choice,value='multiple',bg='seashell2',activebackground='seashell2',command=button_check)
multipleRadioButton.grid(row=0,column=1,padx=20)

choice.set('single')

toLabelFrame=LabelFrame(root,text='To (Email Address)',font=('Goudy Old Style',13,'bold'),bd=5,fg='maroon',bg='seashell2')
toLabelFrame.grid(row=2,column=0,padx=200,pady=10)

toEntryField=Entry(toLabelFrame,font=('Goudy Old Style',13,'bold'),width=30)
toEntryField.grid(row=0,column=0)

browseImage=PhotoImage(file='browse.png')

browseButton=Button(toLabelFrame,text='  BROWSE',image=browseImage,compound=LEFT,font=('Goudy Old Style',10,'bold'),
       cursor='hand2',bd=0,bg='seashell2',activebackground='seashell2',state=DISABLED,command=browse)
browseButton.grid(row=0,column=1,padx=20)

subjectLabelFrame=LabelFrame(root,text='Subject',font=('Goudy Old Style',13,'bold'),bd=5,fg='maroon',bg='seashell2')
subjectLabelFrame.grid(row=3,column=0,pady=10)

subjectEntryField=Entry(subjectLabelFrame,font=('Goudy Old Style',13,'bold'),width=30)
subjectEntryField.grid(row=0,column=0)

emailLabelFrame=LabelFrame(root,text='Compose Email',font=('Goudy Old Style',13,'bold'),bd=5,fg='maroon',bg='seashell2')
emailLabelFrame.grid(row=4,column=0,pady=10)

attachImage=PhotoImage(file='attachments.png')

Button(emailLabelFrame,text='  ATTACHMENT',image=attachImage,compound=LEFT,font=('Goudy Old Style',10,'bold'),
       cursor='hand2',bd=0,bg='seashell2',activebackground='seashell2',command=attachment).grid(row=0,column=1)

textarea=Text(emailLabelFrame,font=('Goudy Old Style',14,),height=8,width=70)
textarea.grid(row=1,column=0,columnspan=2)

sendImage=PhotoImage(file='send.png')
Button(root,image=sendImage,bd=0,bg='seashell2',cursor='hand2',activebackground='seashell2'
       ,command=send_email).place(x=490,y=540)

clearImage=PhotoImage(file='clear.png')
Button(root,image=clearImage,bd=0,bg='seashell2',cursor='hand2',activebackground='seashell2'
       ,command=clear).place(x=590,y=550)

exitImage=PhotoImage(file='exit.png')
Button(root,image=exitImage,bd=0,bg='seashell2',cursor='hand2',activebackground='seashell2'
       ,command=iexit).place(x=690,y=550)

totalLabel=Label(root,font=('Goudy Old Style',18,'bold'),bg='seashell2')
totalLabel.place(x=10,y=560)

sentLabel=Label(root,font=('Goudy Old Style',18,'bold'),bg='seashell2')
sentLabel.place(x=100,y=560)

leftLabel=Label(root,font=('Goudy Old Style',18,'bold'),bg='seashell2')
leftLabel.place(x=190,y=560)

failedLabel=Label(root,font=('Goudy Old Style',18,'bold'),bg='seashell2')
failedLabel.place(x=280,y=560)

root.mainloop()