import csv
import os
import random
from datetime import datetime

class CSVCreator:
    """
    Interactive CSV file creator for Email Sender Bot
    """
    
    def __init__(self):
        self.filename = "recipients.csv"
        
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("CSV FILE CREATOR - EMAIL SENDER BOT")
        print("="*60)
        print("\nChoose an option:")
        print("1. Create sample CSV with test data")
        print("2. Create CSV with custom data")
        print("3. Create large CSV (for testing)")
        print("4. View current CSV file")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        return choice
    
    def create_sample_csv(self):
        """Create CSV with sample test data"""
        print("\n" + "-"*40)
        print("Creating sample CSV file...")
        
        # Sample data with realistic emails and companies
        companies = ["TechCorp", "DataSystems", "InnovateInc", "CloudTech", 
                    "DigitalNexus", "FutureSoft", "ByteCraft", "AlphaAnalytics"]
        
        departments = ["Engineering", "Marketing", "Sales", "HR", 
                      "Finance", "IT", "Operations", "Research"]
        
        data = [["email", "name", "company", "department", "employee_id"]]
        
        # Generate 10 sample records
        for i in range(1, 11):
            first_names = ["John", "Jane", "Michael", "Sarah", "David", 
                          "Emily", "Robert", "Lisa", "William", "Maria"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones",
                         "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
            
            first = random.choice(first_names)
            last = random.choice(last_names)
            company = random.choice(companies)
            dept = random.choice(departments)
            
            email = f"{first.lower()}.{last.lower()}@{company.lower()}.com"
            name = f"{first} {last}"
            emp_id = f"EMP{1000 + i}"
            
            data.append([email, name, company, dept, emp_id])
        
        return self.save_csv(data, "Sample data created successfully!")
    
    def create_custom_csv(self):
        """Create CSV with user-provided data"""
        print("\n" + "-"*40)
        print("Creating custom CSV file")
        print("-"*40)
        
        # Get headers from user
        print("\nEnter column headers (comma separated):")
        print("Example: email,name,company,department,phone")
        headers_input = input("Headers: ").strip()
        
        if not headers_input:
            headers = ["email", "name", "company"]
        else:
            headers = [h.strip() for h in headers_input.split(',')]
        
        # Get number of records
        while True:
            try:
                num_records = int(input("\nNumber of records to create: ").strip())
                if num_records > 0:
                    break
                else:
                    print("Please enter a positive number")
            except ValueError:
                print("Please enter a valid number")
        
        data = [headers]
        
        print(f"\nEnter {num_records} records:")
        print("For each record, enter values separated by commas")
        print(f"Example: john@company.com,John Doe,TechCorp,Engineering")
        
        for i in range(num_records):
            while True:
                record_input = input(f"\nRecord {i+1}: ").strip()
                values = [v.strip() for v in record_input.split(',')]
                
                # Check if number of values matches headers
                if len(values) == len(headers):
                    data.append(values)
                    break
                else:
                    print(f"Error: Expected {len(headers)} values, got {len(values)}")
                    print(f"Headers: {headers}")
        
        return self.save_csv(data, "Custom CSV created successfully!")
    
    def create_large_csv(self):
        """Create a large CSV file for testing"""
        print("\n" + "-"*40)
        print("Creating large CSV file for testing...")
        
        # Get number of records
        while True:
            try:
                num_records = int(input("\nHow many records? (1-1000): ").strip())
                if 1 <= num_records <= 1000:
                    break
                else:
                    print("Please enter between 1 and 1000")
            except ValueError:
                print("Please enter a valid number")
        
        # Data structures
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer",
                      "Michael", "Linda", "William", "Elizabeth", "David", "Susan"]
        
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                     "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez"]
        
        companies = ["TechCorp Solutions", "DataSystems Inc", "InnovateWorks Global",
                    "CloudTech Enterprises", "Digital Nexus Corp", "FutureSoft Tech",
                    "ByteCraft Systems", "Alpha Analytics", "Omega Dynamics"]
        
        domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com", "corp.com"]
        
        departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", 
                      "IT Support", "Operations", "Research & Development"]
        
        # Create data
        data = [["email", "name", "company", "department", "join_date"]]
        
        print(f"\nGenerating {num_records} records...")
        
        for i in range(1, num_records + 1):
            first = random.choice(first_names)
            last = random.choice(last_names)
            company = random.choice(companies)
            dept = random.choice(departments)
            domain = random.choice(domains)
            
            # Create email (different formats)
            email_format = random.choice([1, 2, 3])
            if email_format == 1:
                email = f"{first.lower()}.{last.lower()}@{domain}"
            elif email_format == 2:
                email = f"{first[0].lower()}{last.lower()}@{domain}"
            else:
                email = f"{first.lower()}{random.randint(1,99)}@{domain}"
            
            name = f"{first} {last}"
            
            # Random join date
            year = random.randint(2018, 2023)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            join_date = f"{year}-{month:02d}-{day:02d}"
            
            data.append([email, name, company, dept, join_date])
            
            # Show progress for large files
            if num_records > 50 and i % (num_records // 10) == 0:
                print(f"  Generated {i}/{num_records} records...")
        
        return self.save_csv(data, f"Large CSV with {num_records} records created!")
    
    def save_csv(self, data, success_message):
        """Save data to CSV file"""
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            
            # Get file info
            file_size = os.path.getsize(self.filename)
            num_records = len(data) - 1  # Exclude header
            
            print(f"\n {success_message}")
            print(f" File: {self.filename}")
            print(f" Path: {os.path.abspath(self.filename)}")
            print(f" Records: {num_records}")
            print(f" Size: {file_size} bytes")
            
            # Show preview
            print("\n DATA PREVIEW (first 5 records):")
            print("-" * 60)
            for i, row in enumerate(data[:6]):  # Show header + 5 records
                if i == 0:
                    print(f"Headers: {row}")
                else:
                    print(f"Row {i}: {row}")
            
            if len(data) > 6:
                print(f"... and {len(data)-6} more records")
            
            return True
            
        except Exception as e:
            print(f"\n Error saving CSV file: {e}")
            return False
    
    def view_current_csv(self):
        """View contents of current CSV file"""
        if not os.path.exists(self.filename):
            print(f"\n File not found: {self.filename}")
            return False
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"\n📄 CONTENTS OF {self.filename}:")
            print("="*60)
            print(content)
            print("="*60)
            
            # Count lines
            lines = content.strip().split('\n')
            print(f"Total records: {len(lines)-1} (excluding header)")
            
            return True
            
        except Exception as e:
            print(f"\n Error reading file: {e}")
            return False
    
    def run(self):
        """Run the CSV Creator application"""
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.create_sample_csv()
            elif choice == '2':
                self.create_custom_csv()
            elif choice == '3':
                self.create_large_csv()
            elif choice == '4':
                self.view_current_csv()
            elif choice == '5':
                print("\n Thank you for using CSV Creator!")
                print("Created for SYNTECXHUB Email Sender Bot Project")
                break
            else:
                print("\n Invalid choice. Please enter 1-5.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    creator = CSVCreator()

    creator.run()
