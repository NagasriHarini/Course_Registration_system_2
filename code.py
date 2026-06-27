import re
class Node:
    def __init__(self, student):
        self.student = student
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, student):                               
        new_node = Node(student)
        if self.head is None:
            self.head = new_node
            self.size +=1
            return 
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
        self.size += 1

    def get_first(self):
        if self.head:
            student = self.head.student
            self.head = self.head.next
            self.size -= 1
            return student
        return None
        
    def remove(self, student):
        current = self.head
        if current is not None and current.student == student:
            self.head = current.next
            current = None
            self.size -= 1
            return
        temp = None
        while current is not None and current.student != student:
            temp = current
            current = current.next
        if current is None:
            return
        temp.next = current.next
        current = None
        self.size -= 1
        
    def __len__(self):
        return self.size

class queue:
    def __init__(self):
        self.Queue = LinkedList()

    def enqueue(self, student):
        self.Queue.append(student)

    def front(self):
        return self.Queue.get_first()

    def __len__(self):
        return len(self.Queue)
        
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

class BSTNode:
    def __init__(self, course):
        self.course = course
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, course):
        if self.search(course.course_id):
            print(f"Error: Course with ID {course.course_id} already exists!")
            return False

        if not self.root:
            self.root = BSTNode(course)
        else:
            self._insert(self.root, course)
        return True

    def _insert(self, node, course):
        if course.course_id < node.course.course_id:
            if node.left is None:
                node.left = BSTNode(course)
            else:
                self._insert(node.left, course)
        else:
            if node.right is None:
                node.right = BSTNode(course)
            else:
                self._insert(node.right, course)

    def search(self, course_id):
        return self._search(self.root, course_id)

    def _search(self, node, course_id):
        if not node:
            return None
        if node.course.course_id == course_id:
            return node.course
        elif course_id < node.course.course_id:
            return self._search(node.left, course_id)
        else:
            return self._search(node.right, course_id)

    def delete(self, course_id):
        self.root = self._delete(self.root, course_id)

    def _delete(self, node, course_id):
        if not node:
            return node
        if course_id < node.course.course_id:
            node.left = self._delete(node.left, course_id)
        elif course_id > node.course.course_id:
            node.right = self._delete(node.right, course_id)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.course = temp.course
            node.right = self._delete(node.right, temp.course.course_id)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def display_courses(self):
        if not self.root:
            print("No courses available.")
        else:
            self._display_recursive(self.root)

    def _display_recursive(self, node):
        if node:
            self._display_recursive(node.left)
            print(f"\nCourse ID: {node.course.course_id}")
            print(f"Course Name: {node.course.course_name}")
            print(f"Available Seats: {node.course.available_seats()}/{node.course.max_seats}")
            print(f"Waiting List: {len(node.course.waiting_list)} students")
            self._display_recursive(node.right)
            
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


admin_users = []
student_users = []
users = []
def register_user(user_type):
    print(f"\nRegistering as {user_type.capitalize()}")
    
    while True:
        name = input("Enter full name: ")
        valid_name, name_message = User.validate_name(name)
        if valid_name:
            break
        print(name_message)

    while True:
        user_id = input("Enter user ID: ")
        existing_users = admin_users if user_type == 'admin' else student_users
        if any(user.user_id == user_id for user in users):
            print("User ID already exists. Please choose a different ID.")
            continue
        if user_id:  
            break
        print("User ID cannot be empty.")

    while True:
        phone = input("Enter phone number: ")
        valid_phone, phone_message = User.validate_phone(phone)
        if valid_phone:
            break
        print(phone_message)

    while True:
        password = input("Enter password: ")
        valid_password, password_message = User.validate_password(password)
        if valid_password:
            break
        print(password_message)

    if user_type == 'admin':
        new_user = Admin(name, user_id, phone, password)
        admin_users.append(new_user)
    else: 
        new_user = Student(name, user_id, phone, password)
        student_users.append(new_user)
    users.append(new_user)
    return new_user

def login():
    user_id = input("Enter User ID: ")
    password = input("Enter Password: ")

    for admin in admin_users:
        if admin.user_id == user_id and admin.verify_password(password):
            print(f"Welcome, Admin {admin.name}!")
            return admin, 'admin'

    for student in student_users:
        if student.user_id == user_id and student.verify_password(password):
            print(f"Welcome, Student {student.name}!")
            return student, 'student'

    print("Invalid User ID or Password.")
    return None, None

def main():
    print("Welcome to the Course Registration System!")
    
    course1 = Course(101, "Introduction to Programming", 1)
    course2 = Course(102,"Calculus", 1)
    course3 = Course(103,"Basic Linear Algebra",10)
    course4 = Course(201,"Computational physics",10)
    course5 = Course(202,"Quantum physics",10)
    course6 = Course(301,"Introduction to C - Language",10)
    course7 = Course(302,"Data structures and algorithms",10)
    course8 = Course(401,"Foundations of Indian heritage",10)
    course9 = Course(402,"Glimpse of Glorius India",10)
    course10 = Course(303,"System designing",10)    

    default_admin = Admin("System Admin", "admin001", "1234567890", "Admin@123")
    default_admin.add_course(course1)
    default_admin.add_course(course2)
    default_admin.add_course(course3)
    default_admin.add_course(course4)
    default_admin.add_course(course5)
    default_admin.add_course(course6)
    default_admin.add_course(course7)
    default_admin.add_course(course8)
    default_admin.add_course(course9)
    default_admin.add_course(course10)
    admin_users.append(default_admin)

    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Register as Student")
        print("3. Register as Admin")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            user, user_type = login()
            if user_type == 'admin':
                while True:
                    print("\nAdmin Menu:")
                    print("1. Add New Course")
                    print("2. Remove Course")
                    print("3. View All Courses")
                    print("4. Logout")
                    
                    admin_choice = input("Enter your choice (1-4): ")
                    
                    if admin_choice == '1':
                        course_id = int(input("Enter course ID: "))
                        course_name = input("Enter course name: ")
                        max_seats = int(input("Enter maximum seats: "))
                        new_course = Course(course_id, course_name, max_seats)
                        user.add_course(new_course)
                    
                    elif admin_choice == '2':
                        course_id = int(input("Enter course ID to remove: "))
                        user.remove_course(course_id)
                    
                    elif admin_choice == '3':
                        user.view_all_courses()
                    
                    elif admin_choice == '4':
                        print("Logging out.")
                        break
                    
                    else:
                        print("Invalid choice. Please try again.")

            elif user_type == 'student':
                while True:
                    print("\nStudent Menu:")
                    print("1. Register for a Course")
                    print("2. Search for a course ")
                    print("3. Drop a Course")
                    print("4. View Registered Courses")
                    print("5.View all courses")
                    print("5. Logout")
                    
                    student_choice = input("Enter your choice (1-4): ")
                    
                    if student_choice == '1':
                        course_id =int(input("Enter course ID to register: "))
                        course = default_admin.course_catalog.search(course_id)
                        
                        if course:
                            user.register_course(course)
                        else:
                            print("Course not found.")
                    elif student_choice =='2':
                        course_id = int(input("Enter the course ID: "))
                        course =  default_admin.course_catalog.search(course_id)

                        if course:
                            print(f"\nCourse ID: {course.course_id}")
                            print(f"Course Name: {course.course_name}")
                            print(f"Available Seats: {course.available_seats()}/{course.max_seats}")
                            if len(course.waiting_list) > 0:
                                print(f"Students on waiting list: {len(course.waiting_list)}")

                        else:
                            print("Course not found")
                          
                    elif student_choice == '3':
                        course_id =int(input("Enter course ID to drop: "))
                        course = default_admin.course_catalog.search(course_id)
                        
                        if course:
                            user.drop_course(course)
                        else:
                            print("Course not found.")
                    
                    elif student_choice == '4':
                        user.view_registered_courses()

                    elif student_choice == '5':
                        default_admin.veiw_all_courses()
                    
                    elif student_choice == '6':
                        print("Logging out.")
                        break
                    
                    else:
                        print("Invalid choice. Please try again.")

        elif choice == '2':
            register_user('student')

        elif choice == '3':
            register_user('admin')

        elif choice == '4':
            print("Thank you for using the Course Registration System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
            