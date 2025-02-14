
import _mysql_connector
import mysql.connector


class InvalidNameError(Exception):pass
class SpaceError(Exception):pass
class ZeroLengthNameError(Exception):pass

class Employee():
    def __init__(self,empno:int,name:str,salary:float):
        self.empno=empno
        self.name=self.validate_name(name)
        self.salary=salary


    def __str__(self):
        return f"Employee[ID: {self.empno}, Name: {self.name}, Salary: {self.salary}]"
    @staticmethod
    def validate_name(name:str):
        if len(name)==0:
            raise ZeroLengthNameError("Name cannot be empty")
        elif name.isspace():
            raise SpaceError("Name cannot contain contain only spaces.")
        elif not all(word.isalpha() for word in name.split()):
            raise InvalidNameError("Name should contain only alphabets.")
        return name

class EmployeeManager:
    def __init__(self):
        self.conn=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="12345",
            database="employee_db"
        )
        self.cursor=self.conn.cursor()
    def add_empployees(self,emp:Employee):
        try:
            self.cursor.execute("INSERT INTO employees (id, name, salary) VALUES (%s, %s, %s)",
                                (emp.empno, emp.name, emp.salary))
            self.conn.commit()
            print("Employee added Successfully")
        except mysql.connector.IntegrityError:
            print("Employee Id {} already exist".format(emp.empno))

    def view(self):
        self.cursor.execute("select*from employees")
        employees=self.cursor.fetchall()
        if not employees:
            print("No employees found:")
        else :
            print("\n Employees record")
            for emp in employees:
                print("ID:{},Name:{},Salary:{}".format(emp[0],emp[1],emp[2]))
    def find_employee(self, empno):
        """Find and display employee details by empno (id)."""
        self.cursor.execute("SELECT * FROM employees WHERE id = %s", (empno,))
        emp = self.cursor.fetchone()

        if emp:
            print("\nEmployee Found:")
            print(f"ID: {emp[0]}")
            print(f"Name: {emp[1]}")
            print(f"Salary: {emp[2]}")
        else:
            print("Employee not found!")


    def update_employee(self,empno,new_salary):
        self.cursor.execute("update employees set salary=%s where id=%s ",new_salary,empno)
        if self.cursor.rowcount>0:
            self.conn.commit()
            print("Salary Updated Succesfully.")
        else:
            print("Employee Not Found.")

    def delete_employee(self,empno):
        self.cursor.execute("delete from employees where id=%s",(empno,))
        if self. cursor.rowcount >0:
            self.conn.commit()
            print("Employee deleted successfully.")
        else:
            print("Employee Not found.")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()


manager=EmployeeManager()
while(True):
    print("\n" + "-" * 40)
    print(" Employee Management System")
    print("-" * 40)
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee.")
    print("4. Update Salary")
    print("5. Delete Employee")
    print("6. Exit")
    print("-" * 40)

    ch=int(input("Enter your choice   :"))
    match(ch):
        case 1:
            try:
                empno=int(input("Enter Employee Number:"))
                name=input("Enter Employee Name:")
                salary=float(input("Enter Salary :"))
                emp=Employee(empno,name,salary)
                manager.add_empployees(emp)
            except ValueError:
                print("Invalid input.Employee Number and  Salary Must be numbers ")
            except (InvalidNameError,SpaceError,ZeroLengthNameError)as e:
                print(e)
        case 2:
            manager.view()
        case 3:
            empno = int(input("Enter Employee Number to search: "))
            manager.find_employee(empno)

        case 4:
            try:
                empno = int(input("Enter Employee Number to update salary: "))
                new_salary = float(input("Enter new salary: "))
                manager.update_employee(empno, new_salary)
            except ValueError:
                print("Invalid input! Salary must be a number.")
        case 5:
            try:
                empno = int(input("Enter Employee Number to delete: "))
                manager.delete_employee(empno)
            except ValueError:
                print("Invalid input! Employee number must be a number.")

        case 6:
            manager.close()
            print("Exiting... Goodbye!")
            break

        case _:
            print("Invalid choice! Please try again.")





















