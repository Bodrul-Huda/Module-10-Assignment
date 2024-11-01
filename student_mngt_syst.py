import json

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}\nAge: {self.age}\nAddress: {self.address}")

class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []
#
    def add_grade(self, subject, grade):
        if subject in self.courses:
            self.grades[subject] = grade
            print(f"Grade {grade} added for {self.name} in {subject}.")
        else:
            print(f"{self.name} is not enrolled in {subject}.")

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            print(f"{self.name} enrolled in {course}.")
        else:
            print(f"{self.name} is already enrolled in {course}.")

    def display_student_info(self):
        self.display_person_info()
        print(f"ID: {self.student_id}\nEnrolled Courses: {', '.join(self.courses) if self.courses else 'None'}\nGrades: {self.grades}")

class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
            print(f"{student.name} (ID: {student.student_id}) enrolled in {self.course_name} (Code: {self.course_code}).")
        else:
            print(f"{student.name} is already enrolled in this course.")

    def display_course_info(self):
        print(f"Course Name: {self.course_name}\nCode: {self.course_code}\nInstructor: {self.instructor}\nEnrolled Students: {', '.join([s.name for s in self.students]) if self.students else 'None'}")
#
class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
#
    def add_student(self, name, age, address, student_id):
        if student_id not in self.students:
            student = Student(name, age, address, student_id)
            self.students[student_id] = student
            print(f"Student {name} (ID: {student_id}) added successfully.")
        else:
            print("Student ID already exists.")
#
    def add_course(self, course_name, course_code, instructor):
        if course_code not in self.courses:
            course = Course(course_name, course_code, instructor)
            self.courses[course_code] = course
            print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")
        else:
            print("Course code already exists.")

    def enroll_student_in_course(self, student_id, course_code):
        student = self.students.get(student_id)
        course = self.courses.get(course_code)
        if student and course:
            student.enroll_course(course.course_name)
            course.add_student(student)
        else:
            print("Invalid student ID or course code.")

    def add_grade_for_student(self, student_id, course_code, grade):
        student = self.students.get(student_id)
        course = self.courses.get(course_code)
        if student and course and course.course_name in student.courses:
            student.add_grade(course.course_name, grade)
        else:
            print("Student is not enrolled in the course or invalid identifiers.")

    def display_student_details(self, student_id):
        student = self.students.get(student_id)
        if student:
            student.display_student_info()
        else:
            print("Student not found.")

    def display_course_details(self, course_code):
        course = self.courses.get(course_code)
        if course:
            course.display_course_info()
        else:
            print("Course not found.")

    def save_data(self):
        data = {
            "students": {sid: {"name": s.name, "age": s.age, "address": s.address, "student_id": s.student_id, "grades": s.grades, "courses": s.courses} for sid, s in self.students.items()},
            "courses": {cid: {"course_name": c.course_name, "course_code": c.course_code, "instructor": c.instructor, "students": [s.student_id for s in c.students]} for cid, c in self.courses.items()}
        }
        with open("student_management_system.json", "w") as f:
            json.dump(data, f)
        print("All student and course data saved successfully.")

    def load_data(self):
        try:
            with open("student_management_system.json", "r") as f:
                data = json.load(f)
                for sid, s_data in data["students"].items():
                    student = Student(s_data["name"], s_data["age"], s_data["address"], s_data["student_id"])
                    student.grades = s_data["grades"]
                    student.courses = s_data["courses"]
                    self.students[sid] = student
                for cid, c_data in data["courses"].items():
                    course = Course(c_data["course_name"], c_data["course_code"], c_data["instructor"])
                    course.students = [self.students[sid] for sid in c_data["students"] if sid in self.students]
                    self.courses[cid] = course
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")

def main():
    sms = StudentManagementSystem()
    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")

        choice = input("Select Option: ")
        if choice == "1":
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
            sms.add_student(name, age, address, student_id)
        elif choice == "2":
            course_name = input("Enter Course Name: ")
            course_code = input("Enter Course Code: ")
            instructor = input("Enter Instructor Name: ")
            sms.add_course(course_name, course_code, instructor)
        elif choice == "3":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            sms.enroll_student_in_course(student_id, course_code)
        elif choice == "4":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            grade = input("Enter Grade: ")
            sms.add_grade_for_student(student_id, course_code, grade)
        elif choice == "5":
            student_id = input("Enter Student ID: ")
            sms.display_student_details(student_id)
        elif choice == "6":
            course_code = input("Enter Course Code: ")
            sms.display_course_details(course_code)
        elif choice == "7":
            sms.save_data()
        elif choice == "8":
            sms.load_data()
        elif choice == "0":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()





