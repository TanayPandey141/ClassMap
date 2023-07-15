from tkinter import *
from tkinter import messagebox
# from sms_functions import*
import pymongo
import os
from twilio.rest import Client
from functools import partial

#Sending messages to phone
def custommsg(inp):
    # account_sid = "AC79f798bc18dc363c13b3509e3e431b30"
    # auth_token  = "b72ef33108b885d9ddbb4a4a9c3fc7de"
    # msgclient = Client(account_sid, auth_token)
    # message = msgclient.messages.create(to="+919821840188",from_="+16105573346",body=inp)
    # print(message.sid)
    print(inp)


    
#Connecting to DB
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client['tanay']
Subjects=db["Subjects List Here"]

#Making main UI window 
root=Tk()
root.title("Class Map")
ww=root.winfo_screenwidth()
hh=root.winfo_screenheight()
root.geometry("%dx%d" %(ww,hh))
var_list=[]
b=[]

#Adding a subject
def Add2DB(className,toAdd):
    print(toAdd)
    lala=db[className]
    thiss=[{'name':toAdd}]
    lala.insert_many(thiss)

def AddSubject(className):
    subjectWindow=Toplevel(root)
    h2=hh-100
    subjectWindow.geometry("300x%d"%(h2))
    subjectWindow.title("Add subject/lecture")
    subj=db[className]
    addsub=Text(subjectWindow,height=2,width=40)
    addsub.pack(pady=20,padx=25)
    # toAdd=addsub.get(1.0, "end-1c")
    toAdd=""
    def gettext():
        toAdd=addsub.get(1.0,"end-1c")
        Add2DB(className,toAdd)
    btn=Button(subjectWindow,text="Add lecture",command=gettext,width=25,font=("Helvetica", 13,"bold"))
    btn.pack(pady=20)
 
#Deleting a document in DB:
def DeleteSubject(className):
    # print("yo")
    delWindow=Toplevel(root)
    delWindow.geometry("400x%d"%(hh))
    delWindow.title("Deleting Lectures")
    subj=db[className]
    k=[]
    def choose(index, task):
        if (var_list2[index].get() == 1) :
            if task not in k: k.append(task)
        else:
            if task in k: k.remove(task)
        print(k)
    a1=[]
    for items in subj.find({},{'_id':0}): a1.append(items.values())
    FinalSubList2=[]  
    for subjs in a1:
        c=(" ".join(subjs))
        FinalSubList2.append(c)
    # print(FinalSubList2)
    
    var_list2=[]
    message=Label(delWindow,text="Select the ones to be deleted :",font=("Helvetica", 13,"bold")).grid(row=0,column=0,pady=20,padx=30)
    place=3
    for index,subj in enumerate(FinalSubList2):
        var_list2.append(IntVar(value=0))
        chkbtn=Checkbutton(delWindow, variable=var_list2[index],text=str(subj), command=partial(choose, index, subj),font=("Helvetica", 13))
        chkbtn.grid(row=place,column=0,sticky='w',pady=7,padx=40)
        place+=2
    def deleteit(k):
        mydb=db[className]
        for items in k:
            mydb.delete_one({'name':items})
    delButton=Button(delWindow,text="Delete",command=partial(deleteit,k),width=25,font=("Helvetica", 12,"bold")).grid(row=200,column=0,pady=30,padx=45)
        

#Checkbox Main screen for msg sending
def Trial(className):
    trialWindow=Toplevel(root)
    trialWindow.geometry("400x%d"%(hh))
    trialWindow.title(className)    
    Subjects=db[className]
    b=[]
    def choose(index, task):
        if (var_list[index].get() == 1) :
            if task not in b: b.append(task)
        else:
            if task in b: b.remove(task)
        print(b)
    a=[]
    for items in Subjects.find({},{'_id':0}): a.append(items.values())
    FinalSubList=[]  
    for subjs in a:
        c=(" ".join(subjs))
        FinalSubList.append(c)
    print(FinalSubList)
    
    var_list=[]
    message=Label(trialWindow,text="Select the ones to be cancelled :",font=("Helvetica", 14,"bold")).grid(row=0,column=0,pady=20,padx=30)
    place=3
    for index,subj in enumerate(FinalSubList):
        var_list.append(IntVar(value=0))
        chkbtn=Checkbutton(trialWindow, variable=var_list[index],text=str(subj), command=partial(choose, index, subj),font=("Helvetica", 13))
        chkbtn.grid(row=place,column=0,sticky='w',pady=10,padx=40)
        place+=2

    def cancelmsg(a,b):
        # account_sid = "AC79f798bc18dc363c13b3509e3e431b30"
        # auth_token  = "b72ef33108b885d9ddbb4a4a9c3fc7de"
        # msgclient = Client(account_sid, auth_token)
        msg="The following lectures for "+a+" have been cancelled: \n"
        for items in b:
            msg=msg+items+" \n"
        print(msg)
        # message = msgclient.messages.create(to="+919821840188",from_="+16105573346",body=msg)
        # print(message.sid)
        messagebox.showinfo("Confirmation","The message has been sent")
        trialWindow.destroy()
    sendBtn=Button(trialWindow,text="Send",command=partial(cancelmsg,className,b),width=25,font=("Helvetica", 13,"bold")).grid(row=800,column=0,pady=25,padx=45)
    addSubjectButton=Button(trialWindow,text="Add Lecture",command=partial(AddSubject,className),width=25,font=("Helvetica", 13,"bold")).grid(row=900,column=0,pady=20,padx=45)
    addSubject2Button=Button(trialWindow,text="Delete Lecture",command=partial(DeleteSubject,className),width=25,font=("Helvetica", 13,"bold")).grid(row=910,column=0,pady=10,padx=45)
    
#Class Cancelling
def ClassCancel():
    ClassCancelWindow=Toplevel(root)
    ClassCancelWindow.geometry("500x%d"%(hh))
    ClassCancelWindow.title("Cancelling a Class")
    Label(ClassCancelWindow,text="Select the batch:",font=("Helvetica", 13,"bold")).pack(pady=15,padx=30)
    temp=[]
    Batches=db["Batches"]
    for item in Batches.find({},{'_id':0}): temp.append(item.values())
    batchesList=[]
    for classes in temp:
        c=(" ".join(classes))
        batchesList.append(c)
    for item in batchesList:
        buttonTest = Button(ClassCancelWindow,text=item,command=lambda x=item: Trial(x),width=25,font=( 13)).pack(pady=10)
    buttonAddClass=Button(ClassCancelWindow,text="Add a new Class",width=25,font=("Helvetica", 13,"bold")).pack(pady=50)
   

#Custom Message
def CustomMsg():
    from tkinter import scrolledtext
    CustomMsgWindow=Toplevel(root)
    CustomMsgWindow.geometry("600x%d"%(hh))
    CustomMsgWindow.title("Messenger")
    Label(CustomMsgWindow, text="ScrolledText Widget Example",font=("Times New Roman", 15)).pack(pady=10)
    Label(CustomMsgWindow, text="Enter your comments :", font=("Bold", 15)).pack(pady=10)
    
    def printInput():
        from tkinter import messagebox
        inp=text_area.get(1.0, "end-1c")
        custommsg(inp)
        messagebox.showinfo("Confirmation","The message has been sent")
        CustomMsgWindow.destroy()
    
    text_area = scrolledtext.ScrolledText(CustomMsgWindow, wrap=WORD,width=40, height=8,font=("Times New Roman", 15))
    text_area.pack(pady=10,ipady=10,ipadx=10)
    sendMsgbutton=Button(CustomMsgWindow,text="Send",width=20,command=printInput,font=("Helvetica", 15,"bold")).pack(pady=20)

#root window
message = Label(root, text="Which of these are you looking for:",fg="#003366",font=("Helvetica", 16,"bold")).pack(pady=50)
buttonTableGenerate=Button(root,text="Generate Time Table",width=30,height=2,font=("Helvetica", 16,"bold"),fg="#006633",bg="#fdd18a",activebackground="pink").pack(pady=20)
buttonCancelNotify=Button(root,text="Cancel a Class",command=ClassCancel,width=30,height=2,font=("Helvetica", 16,"bold"),fg="#006633",bg="#fdd18a",activebackground="pink").pack(pady=20)
buttonCustomMsg=Button(root,text="Drop a Message",width=30,height=2,command=CustomMsg,font=("Helvetica", 16,"bold"),fg="#006633",bg="#fdd18a",activebackground="pink").pack(pady=20)

root.mainloop()

