
from tkinter import *
from tkinter import messagebox

from game import main_menu



root = Tk()
root.title("Login")
root.geometry("400x390")
root.configure(bg='#fff')
root.resizable(False, False)

def signin():
    username= user.get()
    password= code.get()

    userInputValid = userDataCheck(username)
    passInputValid = passDataCheck(password)
    if userInputValid == True and passInputValid ==True:
        main_menu()
        

def userDataCheck (userInput='dindacha'):
    try :
        str(userInput)
        return True
    except :
        messagebox.showerror('error', 'username or password incorrect', icon='error')
        return False

def passDataCheck (passInput='3333'):
    try :
        int(passInput)
        return True
    except :
        messagebox.showerror('error', 'username or password incorrect', icon='error')
        return False
    
 


Label(root, bg='white').place(x=50,y=50)

frame = Frame(root, width=350, height=350,bg='white') 
frame.place (x=30,y=30)

heading=Label(frame, text='login', fg='#68AC4F', bg='white', font=('orange days', 23, 'bold'))
heading.place(x=130, y=5)

#============================

def on_enter(e):
    user.delete(0, 'end')
def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


user = Entry(frame,width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

#===========================

def on_enter(e):
    code.delete(0, 'end')
def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

code = Entry(frame,width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)


Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)



#===========================

Button(frame, width=39, pady=7, text='login', bg='#68AC4F', fg='white', border=0 , command=signin).place(x=35,y=204)



root.mainloop()
