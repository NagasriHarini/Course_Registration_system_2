from data_structures import BST, LinkedList, queue
from models import Course, User, Admin, Student


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
            