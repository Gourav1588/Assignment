# Q40, Q41, Q42, Q43, Q44 - Object Oriented Programming


# Q40 - Basic class with attributes
class Student:
    """Represent a student with name, roll number, subject and marks."""

    def __init__(self, name, roll_no, subject, marks):
        """Store student details as instance attributes."""
        self.name = name
        self.roll_no = roll_no
        self.subject = subject
        self.marks = marks

    def display(self):
        """Print all student details in a readable format."""
        print(f"Name:    {self.name}")
        print(f"Roll No: {self.roll_no}")
        print(f"Subject: {self.subject}")
        print(f"Marks:   {self.marks}")


# Q41 - Class with constructor
class Car:
    """Represent a car with make, model and year."""

    def __init__(self, make, model, year):
        """Initialise car with manufacturer details."""
        self.make = make
        self.model = model
        self.year = year

    def display(self):
        """Print car details."""
        print(f"Car: {self.year} {self.make} {self.model}")

    def start(self):
        """Simulate starting the car engine."""
        print(f"{self.make} {self.model} engine started!")


# Q42 - Inheritance: Person is parent, Employee is child
class Person:
    """Represent a person with basic personal details."""

    def __init__(self, name, age):
        """Store name and age."""
        self.name = name
        self.age = age

    def introduce(self):
        """Print a basic personal introduction."""
        print(f"Hi, I am {self.name} and I am {self.age} years old.")


class Employee(Person):
    """Represent an employee who inherits from Person."""

    def __init__(self, name, age, company, salary):
        """Initialise Person fields first, then add employee-specific fields."""
        super().__init__(name, age)  # call parent __init__
        self.company = company
        self.salary = salary

    def introduce(self):
        """Override parent introduce to also show work details."""
        super().introduce()  # reuse parent method
        print(f"I work at {self.company} with salary Rs.{self.salary}")


# Q43 - Encapsulation with private variables
class BankAccount:
    """Represent a bank account with a protected balance."""

    def __init__(self, holder, balance):
        """Set account holder and make balance private."""
        self.holder = holder
        self.__balance = balance  # double underscore = private variable

    def deposit(self, amount):
        """Add money to the account if amount is positive."""
        if amount > 0:
            self.__balance += amount
            print(f"Deposited Rs.{amount}. Balance: Rs.{self.__balance}")

    def withdraw(self, amount):
        """Deduct money from account if sufficient balance exists."""
        if amount > self.__balance:
            print("Insufficient balance!")
        else:
            self.__balance -= amount
            print(f"Withdrew Rs.{amount}. Balance: Rs.{self.__balance}")

    def get_balance(self):
        """Return current balance through a controlled getter method."""
        return self.__balance


# Q44 - Polymorphism: same method name, different behaviour
class Dog:
    """Represent a dog."""

    def speak(self):
        """Make the dog produce its sound."""
        print("Dog says: Woof!")


class Cat:
    """Represent a cat."""

    def speak(self):
        """Make the cat produce its sound."""
        print("Cat says: Meow!")


class Cow:
    """Represent a cow."""

    def speak(self):
        """Make the cow produce its sound."""
        print("Cow says: Moo!")


def make_animal_speak(animal):
    """Call speak() on any animal — same call, different result each time."""
    animal.speak()


# ── Run all questions ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("--- Q40: Student ---")
    s = Student("Gourav", 101, "Data Engineering", 92)
    s.display()

    print("\n--- Q41: Car ---")
    car = Car("Maruti", "Swift", 2023)
    car.display()
    car.start()

    print("\n--- Q42: Inheritance ---")
    emp = Employee("Priya", 28, "TechCorp", 85000)
    emp.introduce()

    print("\n--- Q43: Encapsulation ---")
    account = BankAccount("Gourav", 10000)
    account.deposit(5000)
    account.withdraw(3000)
    print(f"Balance: Rs.{account.get_balance()}")

    print("\n--- Q44: Polymorphism ---")
    animals = [Dog(), Cat(), Cow()]
    for animal in animals:
        make_animal_speak(animal)