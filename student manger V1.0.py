import os
import json
def clear_screen():
   os.system("cls" if os.name == "nt" else "clear")
class Student:

    def  __init__(self, name  , student_num , parent_num, ):
        self.name = name
        self.student_num = student_num
        self.parent_num = parent_num
    def display(self):
        print(f"name : {self.name}")
        print(f"student num : {self.student_num}")
        print(f"parent num  : {self.parent_num}")
class Group:
    def __init__(self,group_name):
        self.group_name = group_name
        self.students = []     


class student_manger:
    def __init__(self):
        self.students = []
        self.groups = []

    def save_groups(self):
        data = []
        for group in self.groups:
            group_dic = {
                "group_name": group.group_name,
                "student": []
            }
            
            for student in group.students:
                group_dic["student"].append(student.name)

            data.append(group_dic) 
        with open("groups.json", "w") as file:
            json.dump(data, file)     

    def load_groups(self):
        try:
            with open("groups.json", "r") as file:
                data = json.load(file)
        except:
            return
        for item in data:
            group = Group(item["group_name"])
            for student_name in item["student"]:
                for student in self.students:
                   if student.name == student_name:
                       group.students.append(student) 
            self.groups.append(group)           

    def save_students(self):

        data =[]
        for student in self.students:
            student_dic ={
                "name": student.name,
                "student_num": student.student_num,
                "parent_num": student.parent_num
            }
            data.append(student_dic)
        with open("students.json", "w") as file:
            json.dump(data , file)  

    def load_students(self):
        try:
          with open("students.json" , "r") as file:
              data = json.load(file)
        except:
            return      
        for item in data:
            student = Student(
                item["name"],
                item["student_num"],
                item["parent_num"],
            )
            self.students.append(student)


    def new_group(self):
        name = input("Group name : ")   
        group = Group(name)
        self.groups.append(group)
        self.save_groups()
        

    def show_group(self):
        if not self.groups:
            print("no group found")
            return
        for i,group in enumerate(self.groups,start=1):
            print(f"{i}-{group.group_name}")
            print("-"*20)
    
    def add_student_to_group(self):
        if not self.groups:
            print("no groups")
            return
        self.show_group()     
        try:
            choice = int(input("choose group : "))
            if choice < 1 or choice > len(self.groups):
                clear_screen()
                print("invalid group numbr")
                return
            
        except ValueError:
            clear_screen()
            print("please enter a vaild number")
            return
        group = self.groups[choice-1]
        student_name = input("Enter student name : ")
        clear_screen()
        for student in self.students:
            if student.name == student_name:
                if student not in group.students:
                  group.students.append(student)
                  self.save_groups()
                  print(len(group.students))
                  print("added successfully!")
                else:
                    print("student already exists in the group")
                return
        print("student not found")    
                    
        
    def show_grouo_students(self):
        if not self.groups:
            print("no groups")
            return
        self.show_group()
        try:
            choice = int(input("choose group : "))
            if choice < 1 or choice > len(self.groups):
                clear_screen()
                print("invalid group numbr")
                return
            
        except ValueError:
            clear_screen()
            print("please enter a vaild number")
            return
        clear_screen()
        group  = self.groups[choice-1]
        if len(group.students) == 0:
            print("no students in this group ")
            return
        for student in group.students:
            student.display()
            print("-"*20)
  
  
    def attendance(self):
        if not self.groups:
            print("no groups")
            return
        self.show_group()
        try:
            choice = int(input("choose group : "))
            if choice < 1 or choice > len(self.groups):
                clear_screen()
                print("invalid group numbr")
                return
            
        except ValueError:
            clear_screen()
            print("please enter a vaild number")
            return
        clear_screen() 
        group  = self.groups[choice-1]
        for i, student in enumerate(group.students,start=1):
            print(f"{i}-{student.name}")
        present_student = input("enter present students : ").split()
        clear_screen()
        print("absent students ")
        print("-"*20)
        for i, student in enumerate(group.students,start=1):
            if str(i) not in present_student:
                student.display()
                print("-"*20)

    def rmove_from_group(self):
         if not self.groups:
            print("no groups")
            return
         self.show_group()
         try:
            choice = int(input("choose group : "))
            if choice < 1 or choice > len(self.groups):
                clear_screen()
                print("invalid group numbr")
                return
            
         except ValueError:
            clear_screen()
            print("please enter a vaild number")
            return
         clear_screen() 
         group  = self.groups[choice-1] 
         student_name = input(" enter student name : ")
         for student in group.students:
            if student.name == student_name:
                group.students.remove(student)
                self.save_groups()
                clear_screen()
                print("student removed")
                return
            print("not found")
 


    def add_student (self): 
        name = input("student name : ") 
        student_num = input("student num : ") 
        parent_num = input("parent num : ") 
        student = Student(name,student_num,parent_num,)
        self.students.append(student)
        self.save_students()
        print("student added successfully!")
        clear_screen()



    def show_students(self):
        if len(self.students) == 0:
            print("no students") 
            return
        
        for student in self.students:
         student.display()
         print("-"*20)
    def search_student(self):
        student_name = input("Enter student name : ") 
        for student in self.students:
            if student_name == student.name:    
                clear_screen()
                print("-"*20)
                student.display()
                print("-"*20)
            else:
                clear_screen()
                print("not found")    
    def remove_student(self):
        student_name = input("Enter student name : ") 
        for student in self.students:
            if student_name == student.name:    
                self.students.remove(student)
                self.save_students()
                print("student removed successfully!")  
                clear_screen()   
                return
        print("student not found")  


def show_menu():
    print("="*40)
    print("        STUDENT MANAGMENT SYSTEM")
    print("="*40)
    print("1-Add Student")
    print("2-Show Student")
    print("3-Search Student")
    print("4-Remove Student")
    print("5-New Group")
    print("6-Show Group")
    print("7-Add Student to Group")
    print("8-remove from group")
    print("9-Show Group Students")
    print("10-attendance")
    print("11-Exit")
    print("="*40)

    
def pause():
    input("\npress Enter to continue")
manger = student_manger()   

manger.load_students()

manger.load_groups()



while True:
    clear_screen()

    show_menu()

    choice = input("choose : ")

    if choice == "1":
        clear_screen()
        manger.add_student()
        print("student added successfully!")

        pause()

    elif choice == "2":
        clear_screen()
        manger.show_students()
        pause()
    elif choice == "3":
        clear_screen()
      
        manger.search_student()
        pause()
    elif choice =="4":
        clear_screen()
        manger.remove_student ()
        print("student removed successfully!")  
        pause()
    elif  choice == "5":
        clear_screen()
        manger.new_group()
        print("New Group created!")
        pause()
    elif choice == "6":
        clear_screen()
        manger.show_group()
        pause()
    elif choice == "7":
        clear_screen()
        manger.add_student_to_group()
        pause()

    elif choice == "8":
        clear_screen()
        manger.rmove_from_group()
        pause()

    elif choice == "9":
        clear_screen()
        manger.show_grouo_students()
        pause()
   
    elif choice == "10":  
        clear_screen()
        manger.attendance()
        pause()  

    elif choice == "11":
        break
    else:
        print("invaild choice!!")      






