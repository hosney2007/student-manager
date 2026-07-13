import os
import sqlite3
def clear_screen():
   os.system("cls" if os.name == "nt" else "clear")

db = sqlite3.connect("student.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS student(id INTEGER PRIMARY KEY,name TEXT, student_num TEXT, parent_num TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS group_table(id INTEGER PRIMARY KEY AUTOINCREMENT,group_name TEXT) ")
cur.execute("CREATE TABLE IF NOT EXISTS student_group(student_id INTERGE, group_id INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT,student_id INTEGER  ,group_id INTEGER)")
db.commit()


class Student:

    def  __init__(self, name  , student_num , parent_num, ):
        self.name = name
        self.student_num = student_num
        self.parent_num = parent_num
    def display(self):
        print(f"name : {self.name}")
        print(f"student num : {self.student_num}")
        print(f"parent num  : {self.parent_num}")



class student_manger:
     #students
    def add_student_sql(self):
        name = input("student name : ") 
        student_num = input("student num : ") 
        parent_num = input("parent num : ") 
        cur.execute("INSERT INTO student(name , student_num, parent_num) VALUES(?,?,?)",(name, student_num, parent_num))
        db.commit()

    def show_student_sql(self):
        cur.execute("SELECT * FROM student")
        students = cur.fetchall()
        if not students:
            print("    NO STUDENTS   ")
        else:
          for student in students:
             print(f"NAME : {student[1]} | STUDENT NUM : {student[2]} | PARENT NUM : {student[3]}")
             print("="*50)
        db.commit()  

    def delete_student_sql(self):
        name = input("enter student name : ")
        cur.execute("DELETE FROM student WHERE name = ? " , (name,)) 
        if cur.rowcount > 0:
            print("student deleted")
        else:
            print("student not found")    
        db.commit()

    def search_student_sql(self):
        name = input("Enter student name : ")
        cur.execute("SELECT * FROM student WHERE name = ?" , (name,))
        student = cur.fetchone()
        if student is None:
            print("Student not found ")
        else:
            print(f"NAME : {student[1]} | STUDENT NUM : {student[2]} | PARENT NUM : {student[3]}")    
    
    def edit_student(self):
         cur.execute("SELECT* FROM student")
         students = cur.fetchall()
         if not students:
            print("    NO STUDENTS   ")
         else:
           for student in students:
             print(f" ID : {student[0]}  |  NAME : {student[1]} ")
             print("="*50)
         db.commit() 
         student = input("CHOOSE STUDENT :  ")
         cur.execute("SELECT * FROM student WHERE id = ?" , (student,))
         studentt = cur.fetchone()
         if studentt is None:
             print("STUDENT NOT FOUND")
             return
         clear_screen()
         new_name = input("ENTER NEW NAME : " )
         new_num = input("ENTER NEW NUM : " )
         new_parent_num = input("ENTER NEW PARENT NUM : " )
         cur.execute("UPDATE student SET name = ? ,student_num = ? ,parent_num = ? WHERE id = ? " ,( new_name, new_num, new_parent_num ,student))
         db.commit
         clear_screen()
         print("student updated")

   
   #groups
    def new_group_sql(self):
        name = input("ENTER Group Name : ")
        cur.execute("INSERT INTO group_table(group_name) VALUES(?)" ,(name,))
        db.commit()
        print("group added") 

    def show_group_sql(self):
        cur.execute("SELECT * FROM group_table")
        groups = cur.fetchall()
        if not groups :
            print("    NO groups   ")
        else:
          for group in groups:
             print(f"ID : {group[0]} | NAME : {group[1]}")
             print("="*25)
        db.commit()     

    def delete_group_sql(self):
        self.show_group_sql()
        name = input("choose group name : ")
        cur.execute("DELETE FROM group_table WHERE id = ? " , (name,)) 
       # cur.execute("DELETE FROM student WHERE id = ? " , (name,)) 
        if cur.rowcount > 0:
            print("group deleted")
        else:
            print("group not found")    
        db.commit()    
    
    #STUDENTS IN GROUP
    def add_student_to_group_sql(self):
         
         
         cur.execute("SELECT* FROM student")
         students = cur.fetchall()
         if not students:
            print("    NO STUDENTS   ")
         else:
           for student in students:
             print(f" ID : {student[0]}  |  NAME : {student[1]} ")
             print("="*50)
         db.commit() 
         student = input("CHOOSE STUDENT :  ")
         cur.execute("SELECT* FROM student WHERE id = ? " , (student,))
         stu = cur.fetchone()
         if stu is None:
             print("no student")
             return
         clear_screen()
         self.show_group_sql()
         group = input("CHOOSE GROUP : ")
         
         cur.execute("SELECT * FROM student_group WHERE student_id = ? AND grooup_id = ?" , (student,group,))
         if cur.fetchone():
             print("STUDENT IS ALREADY IN THIS GROUP")
             return
         cur.execute("SELECT * FROM group_table WHERE id = ?" , (group,))
         gro = cur.fetchone()
       
         if stu and gro:
             cur.execute("INSERT INTO student_group(student_id, grooup_id) VALUES(?,?)" ,(student,group,))
             db.commit()
             print("student added to group ")
         else:
             print("group not found")    

    def show_group_students_sql(self):
        self.show_group_sql()
        group_id = input("CHOOSE GROUP : ")
        clear_screen()
        cur.execute("SELECT * FROM group_table WHERE id = ?" , (group_id,))
        group = cur.fetchone()
        if group is None:
            print("GROUP NOT FOUND")
            return
        cur.execute("SELECT student.id,student.name,student.student_num,student.parent_num FROM student JOIN student_group ON student.id = student_group.student_id WHERE student_group.grooup_id = ? " , (group_id,))
        students = cur.fetchall()
        if not students :
            print("    NO student in this group   ")
            return
        else:
          for student in students:
             print(
                 f"ID: {student[0]} |"
                 f"NAME: {student[1]} | "
                 f"STUDENT NUM: {student[2]} | "
                 f"PARENT NUM: {student[3]}")
             print("="*25)
        return students , group_id
        
    def  delete_student_from_group(self):
        result  = self.show_group_students_sql()
        if result is None:
            return
        students, group_id = result
        student_id = input("CHOOSE STUDENT : ")


        cur.execute("SELECT * FROM student_group WHERE student_id = ? AND grooup_id = ?" ,(student_id, group_id))
        
        if cur.fetchone() is None:
            print("student not found")
            return

        cur.execute("DELETE FROM student_group WHERE student_id = ? AND grooup_id = ?" , (student_id, group_id,))
        db.commit()

        if cur.rowcount > 0:
            print("student removed")
        else:
            print("student not in this group")

    #ATTENDACNE
    def attendance_sql(self):
        cur.execute("DELETE FROM attendance")
        db.commit()
        print("bb")
        result = self.show_group_students_sql()
        if result is None:
            return
        students, group_id = result 
        
        present = input("CHOOSE STUDENTS : ").split() 
        clear_screen()
        for student in students:
           if str(student[0]) in present:
               cur.execute("INSERT INTO attendance(student_id, group_id) VALUES(?, ?)",(student[0], group_id))
        db.commit()
        print("ABSENT STUDENTS")
        for student in students:
            if str(student[0]) not in present:
                print(f"{student[1]} | parent : {student[3]}")  
                print("="*25)

                  
   #MENU 
def show_menu():
    print("="*40)
    print("        STUDENT MANAGMENT SYSTEM")
    print("="*40)
    print("1-Add Student")
    print("2-Show Student")
    print("3-Search Student")
    print("  4-EDIT STUDENT ")
    print("5-Remove Student")
    print("6-New Group")
    print("7-Show Group")
    print("8-Add Student to Group")
    print("9-remove group")
    print("10-Show Group Students")
    print("11-delete student from group")
    print("12-attend")
    print("13-EXI")
    print("="*40)

    
def pause():
    input("\npress Enter to continue")
manger = student_manger()  
  #FUNCTIONS
while True:
    
    
    clear_screen()


    show_menu()

    choice = input("choose : ")

    if choice == "1":
        clear_screen()
        manger.add_student_sql()
        

        pause()

    elif choice == "2":
        clear_screen()
        manger.show_student_sql()
        pause()
    elif choice == "3":
        clear_screen()
      
        manger.search_student_sql()
        pause()
    elif choice == "4":
        clear_screen()
        manger.edit_student()
        pause()
    elif choice =="5":
        clear_screen()
        manger.delete_student_sql ()
        #print("student removed successfully!")  
        pause()
    elif  choice == "6":
        clear_screen()
        manger.new_group_sql()
        
        pause()
    elif choice == "7":
        clear_screen()
        manger.show_group_sql()
        pause()
    elif choice == "8":
        clear_screen()
        manger.add_student_to_group_sql()
        pause()

    elif choice == "9":
        clear_screen()
        manger.delete_group_sql()
        pause()

    elif choice == "10":
        clear_screen()
        manger.show_group_students_sql()
        pause()
   
    elif choice == "11":  
        clear_screen()
        manger.delete_student_from_group()
        pause()  
    elif choice == "12":
        clear_screen()
        manger.attendance_sql()
        pause()


    elif choice == "13":
        break
    else:
        clear_screen()
        print("invaild choice!") 
        pause()
             