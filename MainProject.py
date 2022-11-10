import time
#Clean start-----------------------------------------------------------------------------------
q=1
student_dict={}
isbn_dict={}
check_dict={}
student_who_checks={}
top_books={}

#students file                      --------------------------------
s=open('students.txt', 'r',encoding="utf-8")
students=s.readlines()
s.close()

for i in students:
    studentID=i[0:6]
    studentName=i[7:].strip("\n")
    studentName=studentName.strip()
    student_dict[studentID]=studentName

#books file                         --------------------------------
s=open('books.txt', 'r',encoding="utf-8")
books=s.readlines()
s.close()


for i in books:
    i=i.strip("\n")
    i=i.strip()
    i=i.split(",")
    check_dict[i[0]]=i[3]
    isbn_dict[i[0]]=i[1]

#for check                          ----------------------------------
s=open('check.txt', 'r',encoding="utf-8")
check=s.readlines()
s.close()

for i in check:
    i=i.split(",")
    student_who_checks[i[0]]=i[1:]

#for count the books                ----------------------------------
s=open('book_counter.txt', 'r',encoding="utf-8")
book_count=s.readlines()
s.close()
for i in range(0,len(book_count),2):
    top_books[book_count[i][:-1]]=int(book_count[i+1][:-1])

#defination part---------------------------------------------------------------------------------------

#list of books--------------------------
def listAllTheBooks(dct=isbn_dict):
    for i in list(dct.values()):
        print(i)

#is it checked---------------------------
def isItChecked(dct=check_dict,name=isbn_dict):
    checked_books=[]
    for i in dct.keys():
        if dct[i]=="T":
            checked_books.append(name[i])
            print(name[i])

#add new book----------------------------------
def addNewBook(dct1=isbn_dict,dct2=check_dict):
    s=open('books.txt', 'a',encoding="utf-8")
    isbn=input("Please enter the ISBN of the book: ")
    book_name=input("Please enter the name of the book: ")
    author_name=input("Please enter the author of the book: ")
    check=input("Is this book checked? If it is please enter T, if not enter F: " ).upper()
    s.write(f"{isbn},{book_name},{author_name},{check}\n")
    s.close()
    check_dict[isbn]=check
    isbn_dict[isbn]=book_name

#Search a book by ISBN number-----------------------------
def searchByIsbn(dct=isbn_dict):
    isbn=input("Please enter the ISBN: ")
    if isbn in isbn_dict.keys():
        return print(dct[str(isbn)])
    else:
        return print("Sorry. We don't have the book that you're looking for.")

#Search a book by name-----------------------------
def searchByName(dct=isbn_dict):
    name=input("Please enter the book name: ")
    result_lst=[]
    for i in isbn_dict.values():
        if name.lower() in i.lower():
            result_lst.append(i)
    for j in result_lst:
        print(j)

#Check out a book to a student---------------------------
def checkForStudent(s_dct=student_dict,i_dct=isbn_dict,c_dct=check_dict):
    s=open("books.txt","r+",encoding="utf-8")
    books=s.readlines()
    x=input("Please enter the ISBN: ")
    y=input("Please enter the student ID: ")

    if c_dct[x]=="T":
        return print("what a bad day for you")
    else:
        c_dct[x]="T"

    if student_dict[y] not in student_who_checks.keys():
        student_who_checks[student_dict[y]]=[isbn_dict[x]]
    else:
        student_who_checks[student_dict[y]].append(isbn_dict[x])

    for i in range(len(books)):
        if x in books[i]:
            books[i]=books[i].strip("\n")
            books[i]=books[i].strip()
            books[i]=books[i][:-2]+",T\n"
            break

    s.seek(0)
    s.writelines(books)
    s.close()

    z=open("check.txt","r+",encoding="utf-8")
    student=z.readlines()
    change=0

    for i in range(len(student)):
        if s_dct[y] in student[i]:
            student[i]=student[i][:-2]+f",{i_dct[x]}\n"
            change=1

    if change==0:
        student.append(f"{s_dct[y]},{i_dct[x]}\n")
        
    z.seek(0)
    z.writelines(student)
    z.close()

    s=open("book_counter.txt","r+",encoding="utf-8")
    books=s.readlines()
    change=0
    for i in range(0,len(books),2):
        if books[i][:-1]==i_dct[x]:
            books[i+1]=str(int(books[i+1])+1)+"\n"
            change=1
            break
    if change==0:
        books.append(isbn_dict[x]+"\n1\n")

    s.seek(0)
    s.writelines(books)
    s.close()



#lists students---------------------------------------------
def Students(s_dct=student_dict,w_dict=student_who_checks):
    for i in s_dct.values():
        print(i)
        if i in w_dict.keys():
            for j in w_dict[i]:
                print("\t",j)

#Top 3 book------------------------------------------------
def top3books(top_books=top_books):
    lst=[-1,"",-1,"",-1,""]
    for i in top_books.keys():
        if top_books[i]>lst[0]:
            lst[0:0]=[top_books[i],i]
            lst.pop()
            lst.pop()
        elif top_books[i]>lst[2]:
            lst[2:2]=[top_books[i],i]
            lst.pop()
            lst.pop()
        elif top_books[i]>lst[4]:
            lst[4:4]=[top_books[i],i]
            lst.pop()
            lst.pop()
    print("1."+lst[1]+"\n2."+lst[3],"\n3."+lst[5])

def top3students():
    lst=[0,"",0,"",0,""]
    for i in student_who_checks.keys():
        x=len(student_who_checks[i])
        if x>lst[0]:
            lst[0:0]=[x,i]
            lst.pop()
            lst.pop()
        elif x>lst[2]:
            lst[2:2]=[x,i]
            lst.pop()
            lst.pop()
        elif x>lst[4]:
            lst[4:4]=[x,i]
            lst.pop()
            lst.pop()
    print("1."+lst[1]+"\n2."+lst[3],"\n3."+lst[5])
def quit():
    global q
    q=0

#menu things-----------------------------------------------------------------------------------------------
menu={"1":listAllTheBooks,"2":isItChecked,"3":addNewBook,"4":searchByIsbn,"5":searchByName,"6":checkForStudent,"7":Students,"8":top3books,"9":top3students,"q":quit}
while q:
    print("---------------------SELECTION---------------------")
    result=input("Press 1 to list all the books.\nPress 2 to list checked out books.\nPress 3 to add a new book.\nPress 4 to search book by ISBN number.\nPress 5 to search book by name.\nPress 6 to check a book for a student.\nPress 7 to list all the students. (with books if they had checked)\nPress 8 to list top 3 books.\nPress 9 to list top 3 students. :")
    print("-----------------------ACTION-----------------------")
    menu[result]()