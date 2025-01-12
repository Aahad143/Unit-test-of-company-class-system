import re

separator = "-"*70

class ITMagazineStaff:
    _used_staff_ids = set()  # Class-level registry to keep track of all staff IDs

    def __init__(self, staff_id: int, salary: int, dept: str):
        # OCL: staff_id must be a 6-digit integer
        if not isinstance(staff_id, int) or len(str(staff_id)) != 6:
            raise ValueError("Staff ID must be a 6-digit integer.")
        # OCL: salary must be between 10,000 and 1,000,000
        if not (10000 <= salary <= 1000000):
            raise ValueError("Salary must be between 10,000 and 1,000,000.")
        # OCL: dept must be one of the defined departments
        valid_departments = ["Marketing", "Editing", "Processing Centre"]
        if dept not in valid_departments:
            raise ValueError(f"Department must be one of {valid_departments}.")
        
        # OCL: staff_id must be unique
        if staff_id in ITMagazineStaff._used_staff_ids:
            raise ValueError(f"Staff ID {staff_id} is already in use.")

        self.staff_id = staff_id
        self.salary = salary
        self.dept = dept
        ITMagazineStaff._used_staff_ids.add(staff_id)
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Helper method to validate email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    @staticmethod
    def _validate_password(password: str) -> bool:
        """Helper method to validate password strength."""
        # Password must have at least 8 characters, including one uppercase, one lowercase, one digit, and one special character.
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return bool(re.match(password_regex, password))

    def login(self, email: str, password: str) -> bool:
        """Validate email and password and perform login."""
        if not self._validate_email(email):
            print(f"Invalid email format: {email}")
            return False

        if not self._validate_password(password):
            print("Password must be at least 8 characters long, including an uppercase letter, a lowercase letter, a digit, and a special character.")
            return False

        print(f"{self.__class__.__name__} (ID: {self.staff_id}) successfully logged in.")
        return True

    def logout(self):
        print(f"{self.__class__.__name__} (ID: {self.staff_id}) logged out.")

    def display_info(self):
        print(f"Staff ID: {self.staff_id}, Department: {self.dept}, Salary: {self.salary}")

    @classmethod
    def remove_staff_id(cls, staff_id: int):
        """Allows removing a staff ID when an object is deleted."""
        cls._used_staff_ids.discard(staff_id)

    def __del__(self):
        """Automatically clean up the staff ID when the object is deleted."""
        try:
            ITMagazineStaff.remove_staff_id(self.staff_id)
            # print(f"{self.__class__.__name__} (ID: {self.staff_id}) has been deleted.")
        except AttributeError:
            # In case the attribute is not available at the time of deletion
            pass


class MarketingDeptStaff(ITMagazineStaff):
    def __init__(self, staff_id: int, salary: int, dept: str):
        super().__init__(staff_id, salary, dept)
        self.adverts = {}  # Dictionary to store adverts by their ID

    def create_advert(self, advert_id, client_name, size, placement, publication_date):
        # OCL: Ad details must not be empty
        # Validate input
        if not advert_id:
            raise ValueError("Advert ID cannot be empty.")
        if not client_name:
            raise ValueError("Client name cannot be empty.")
        if size not in ["Full Page", "Half Page", "Quarter Page"]:
            raise ValueError(f"Invalid size: {size}. Must be one of ['Full Page', 'Half Page', 'Quarter Page'].")
        if not placement:
            raise ValueError("Placement cannot be empty.")
        if not self._is_valid_date(publication_date):
            raise ValueError(f"Invalid publication date: {publication_date}. Must be in YYYY-MM-DD format.")
        
        # Create advert
        if advert_id in self.adverts:
            raise ValueError("Advert ID already exists.")
        advert = Advert(advert_id, client_name, size, placement, publication_date)
        self.adverts[advert_id] = advert
        return advert

    def _is_valid_date(self, date_string):
        from datetime import datetime
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def update_advert(self, advert_id, size=None, placement=None, publication_date=None):
        # OCL: advert_id must exist
        if advert_id not in self.adverts:
            raise ValueError("Advert ID does not exist.")
        self.adverts[advert_id].update_details(size, placement, publication_date)
        return f"Advert {advert_id} updated successfully."

    def cancel_advert(self, advert_id):
        # OCL: advert_id must exist
        if advert_id not in self.adverts:
            raise ValueError("Advert ID does not exist.")
        self.adverts[advert_id].cancel_advert()
        return f"Advert {advert_id} cancelled successfully."

class Editor(ITMagazineStaff):
    def __init__(self, staff_id: int, salary: int, dept: str):
        super().__init__(staff_id, salary, dept)
        self.magazine_issues = {}  # Dictionary to store magazine issues by their date

    def update_advert_in_issue(self, advert, issue_date):
        if advert.status == "Cancelled":
            raise ValueError("Cannot add or update a cancelled advert in the magazine.")
        if issue_date not in self.magazine_issues:
            self.magazine_issues[issue_date] = []

        # OCL: Advertisement must exist and be active
        # Check if advert exists in the issue
        existing_advert = next((ad for ad in self.magazine_issues[issue_date] if ad.advert_id == advert.advert_id), None)

        if existing_advert:
            # Update existing advert
            existing_advert.update_details(
                size=advert.size, placement=advert.placement, publication_date=advert.publication_date
            )
            print(f"Advert {advert.advert_id} updated in issue {issue_date} by Editor {self.staff_id}.")
        else:
            # Add new advert
            self.magazine_issues[issue_date].append(advert)
            advert.status = "Approved"
            print(f"Advert {advert.advert_id} added to issue {issue_date} by Editor {self.staff_id}.")

    def remove_advert_from_issue(self, advert_id, issue_date):
        if issue_date not in self.magazine_issues:
            raise ValueError("Issue date does not exist.")
        self.magazine_issues[issue_date] = [ad for ad in self.magazine_issues[issue_date] if ad.advert_id != advert_id]

class ProcessingCentreStaff(ITMagazineStaff):
    def __init__(self, staff_id: int, salary: int, dept: str):
        super().__init__(staff_id, salary, dept)
        self.stored_adverts = []  # List of all adverts stored in the system

    def store_advert(self, advert):
        # OCL: Only approved advertisements can be stored
        if advert.status != "Approved":
            raise ValueError("Only approved adverts can be stored.")
        self.stored_adverts.append(advert)
        print(f"Advert {advert.advert_id} stored successfully.")

class Advert:
    def __init__(self, advert_id, client_name, size, placement, publication_date, status="Pending"):
        self.advert_id = advert_id  # Unique ID for the advert
        self.client_name = client_name  # Advertiser's name
        self.size = size  # Size of the advert
        self.placement = placement  # Placement in the magazine
        self.publication_date = publication_date  # Date when the advert is scheduled to appear
        self.status = status  # Status: "Pending", "Approved", "Cancelled", "Published"

    def update_details(self, size=None, placement=None, publication_date=None):
        if size:
            self.size = size
        if placement:
            self.placement = placement
        if publication_date:
            self.publication_date = publication_date

    def cancel_advert(self):
        self.status = "Cancelled"

    def __str__(self):
        return (
            f"Advert(ID: {self.advert_id}, Client: {self.client_name}, "
            f"Size: {self.size}, Placement: {self.placement}, "
            f"Date: {self.publication_date}, Status: {self.status})"
        )


from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class CreateAdvertCommand(Command):
    def __init__(self, marketing_dept, advert_details):
        self.marketing_dept = marketing_dept
        self.advert_id = advert_details["advert_id"]
        self.client_name = advert_details["client_name"]
        self.size = advert_details["size"]
        self.placement = advert_details["placement"]
        self.publication_date = advert_details["publication_date"]

    def execute(self):
        return self.marketing_dept.create_advert(
            self.advert_id, self.client_name, self.size, self.placement, self.publication_date
        )

class UpdateAdvertCommand(Command):
    def __init__(self, marketing_dept, advert_id, size=None, placement=None, publication_date=None):
        self.marketing_dept = marketing_dept
        self.advert_id = advert_id
        self.size = size
        self.placement = placement
        self.publication_date = publication_date

    def execute(self):
        return self.marketing_dept.update_advert(
            self.advert_id, self.size, self.placement, self.publication_date
        )

class CancelAdvertCommand(Command):
    def __init__(self, marketing_dept, advert_id):
        self.marketing_dept = marketing_dept
        self.advert_id = advert_id

    def execute(self):
        return self.marketing_dept.cancel_advert(self.advert_id)

# Editor Commands

class UpdateAdvertInIssueCommand(Command):
    def __init__(self, editor, advert, issue_date):
        self.editor = editor
        self.advert = advert
        self.issue_date = issue_date

    def execute(self):
        self.editor.update_advert_in_issue(self.advert, self.issue_date)
        return f"Advert {self.advert.advert_id} updated or added to issue {self.issue_date}."

class RemoveAdvertFromIssueCommand(Command):
    def __init__(self, editor, advert_id, issue_date):
        self.editor = editor
        self.advert_id = advert_id
        self.issue_date = issue_date

    def execute(self):
        self.editor.remove_advert_from_issue(self.advert_id, self.issue_date)
        return f"Advert {self.advert_id} removed from issue {self.issue_date}."


# ProcessingCentreStaff Commands

class StoreAdvertCommand(Command):
    def __init__(self, processing_centre, advert):
        self.processing_centre = processing_centre
        self.advert = advert

    def execute(self):
        self.processing_centre.store_advert(self.advert)
        return f"Advert {self.advert.advert_id} stored successfully."


class CommandInvoker:
    def __init__(self):
        self.command_queue = []  # Stores a queue of commands

    def add_command(self, command):
        self.command_queue.append(command)

    def execute_commands(self):
        if len(self.command_queue) == 0:
            print("No commands to execute")

        results = []
        while self.command_queue:
            command = self.command_queue.pop(0)
            results.append(command.execute())
        return results
    
    def clear_command_queue(self):
        self.command_queue = []


if __name__ == "__main__":
    # Create the receiver (MarketingDeptStaff)
    marketing = MarketingDeptStaff(staff_id=100000, salary=50000, dept="Marketing")
    editor = Editor(staff_id=200000, salary=20000, dept="Editing")
    processing_staff =ProcessingCentreStaff(staff_id=300000, salary=20000, dept="Processing Centre")

    advert_details = {"advert_id": "AD001",
                      "client_name": "Client A",
                      "size": "Full Page",
                      "placement": "Back Cover",
                      "publication_date": "2025-01-15"}
    # Create the invoker
    invoker = CommandInvoker()

    # Create commands
    create_command = CreateAdvertCommand(
        marketing, advert_details
    )
    update_command = UpdateAdvertCommand(
        marketing, "AD001", size="Half Page", placement="Front Cover"
    )
    cancel_command = CancelAdvertCommand(marketing, "AD001")

    print("Commands for MarketingDeptStaff:")
    # Add commands to the invoker
    invoker.add_command(create_command)
    invoker.add_command(update_command)

    # Execute all commands
    marketing_dept_cmd_results = invoker.execute_commands()
    advert001 = marketing_dept_cmd_results[0]

    # print("marketing_dept_cmd_results:", marketing_dept_cmd_results)
    for result in marketing_dept_cmd_results:
        print(result)
    print("advert001.status:", advert001.status)

    print(separator)
    invoker.clear_command_queue()
    

    print("Commands for advert in issue by editor:")

    update_advert_in_issue_command = UpdateAdvertInIssueCommand(editor, advert001, "2025-03-01")
    remove_advert_from_issue_command = RemoveAdvertFromIssueCommand(editor, "AD001", "2025-03-01")

    # Add commands to the invoker
    invoker.add_command(update_advert_in_issue_command)
    invoker.add_command(remove_advert_from_issue_command)
    
    # Execute all commands
    configure_ad_in_issue_cmd_results = invoker.execute_commands()

    # print("marketing_dept_cmd_results:", marketing_dept_cmd_results)
    for result in configure_ad_in_issue_cmd_results:
        print(result)
    print("advert001.status:", advert001.status)

    print(separator)
    invoker.clear_command_queue()

    print("Command for storing advert")

    storing_advert_command = StoreAdvertCommand(processing_staff, advert001)

    # Add commands to the invoker
    invoker.add_command(storing_advert_command)

    store_ad_cmd_results = invoker.execute_commands()

    for result in store_ad_cmd_results:
        print(result)

    print(separator)
    invoker.clear_command_queue()

    print("Commands for updating cancelled advert in issue by editor:")

    # Add commands to the invoker
    invoker.add_command(cancel_command)
    invoker.add_command(update_advert_in_issue_command)

    try:
        update_ad_in_issue_cmd_results = invoker.execute_commands()
    except Exception as e:
        print("Error updating advert in issue by editor : " + str(e))
    
    invoker.clear_command_queue()