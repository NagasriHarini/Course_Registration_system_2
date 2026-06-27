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
            
