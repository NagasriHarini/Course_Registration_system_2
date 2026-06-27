import re
from data_structures import BST, LinkedList, queue 

class Course:
    def __init__(self, course_id, course_name, max_seats):
        self.course_id = course_id
        self.course_name = course_name
        self.max_seats = max_seats
        self.students = LinkedList()
        self.waiting_list = queue()
        
    def available_seats(self):
        return self.max_seats - len(self.students)

    def add_student(self, student):
        if len(self.students) < self.max_seats:
            self.students.append(student)
            return True
        return False

    def remove_student(self, student):
        self.students.remove(student)

    def add_to_waiting_list(self, student):
        self.waiting_list.enqueue(student)
        return True
        
    def process_waiting_list(self):
        if len(self.waiting_list) > 0 and self.available_seats() > 0:
            next_student = self.waiting_list.front()
            if next_student and self.add_student(next_student):
                next_student.registered_courses.append(self)
                print(f"{next_student.name} has been enrolled from the waiting list.")


class User:
    def __init__(self, name, user_id, phone, password):
        self.name = name
        self.user_id = user_id
        self.phone = phone
        self.__password = password
    
    def verify_password(self, password):
        return self.__password == password

    @staticmethod
    def validate_name(name):
        if not bool(name):
            return False, "Name cannot be empty."
        if len(name) > 20:
            return False, "Name must be 20 characters or less."
        if not all(char.isalpha() or char.isspace() for char in name):
            return False, "Name can only contain letters and spaces."
        return True, "Valid name."

    @staticmethod
    def validate_phone(phone):
        if not phone.isdigit():
            return False, "Phone number must contain only digits."
        if len(phone) != 10:
            return False, "Phone number must be exactly 10 digits."
        if phone[0] == '0':
            return False, "Phone number cannot start with zero. Please enter a valid phone number."
        return True, "Valid phone number."

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one digit."
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character."
        return True, "Valid password."

class Student(User):
    def __init__(self, name, user_id, phone, password):
        super().__init__(name, user_id, phone, password)
        self.registered_courses = []

    def register_course(self, course):
        if len(self.registered_courses) < 6 and course not in self.registered_courses:
            if course.available_seats() > 0:
                self.registered_courses.append(course)
                course.add_student(self)
                print(f"Successfully registered for {course.course_name}")
                return True
            else:
                print("Course is full.")
                if course.add_to_waiting_list(self):
                    print(f"Added to waiting list.")
                return False
        else:
            print("Maximum course limit reached (6 courses) or already registered.")
            return False

    def drop_course(self, course):
        if course in self.registered_courses:
            self.registered_courses.remove(course)
            course.remove_student(self)
            print(f"Successfully dropped {course.course_name}")
            course.process_waiting_list()
        else:
            print("You are not registered for this course.")

    def view_registered_courses(self):
        print("\nYour Registered Courses:")
        for course in self.registered_courses:
            print(f"Course ID: {course.course_id}, Name: {course.course_name}")

class Admin(User):
    course_catalog = BST()  

    def __init__(self, name, user_id, phone, password):
        super().__init__(name, user_id, phone, password)

    def add_course(self, course):
        if Admin.course_catalog.insert(course):
            print(f"Course '{course.course_name}' added successfully.")

    def remove_course(self, course_id):
        Admin.course_catalog.delete(course_id)
        print(f"Course with ID {course_id} deleted successfully.")

    def view_all_courses(self):
        Admin.course_catalog.display_courses()