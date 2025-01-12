import unittest
from it_magazine import (
    ITMagazineStaff,
    MarketingDeptStaff,
    Editor,
    ProcessingCentreStaff,
    Advert,
    separator
)

# Test Data
test_data_for_staff = [
            # Valid Inputs
            {"staff_id": 100001, "salary": 55000, "dept": "Marketing"},
            {"staff_id": 200001, "salary": 65000, "dept": "Editing"},
            {"staff_id": 300001, "salary": 60000, "dept": "Processing Centre"},
            # Invalid Inputs
            {"staff_id": -1, "salary": 50000, "dept": "Marketing"},  # Negative staff ID
            {"staff_id": 100002, "salary": -1000, "dept": "Marketing"},  # Negative salary
            {"staff_id": 200002, "salary": 60000, "dept": ""},  # Empty department
            {"staff_id": "InvalidID", "salary": 60000, "dept": "Editing"},  # Non-integer staff ID
            {"staff_id": 300002, "salary": 1, "dept": "Processing Centre"},  # Non-numeric salary
        ]

test_data_for_advert = [
    # Valid Inputs
    {
        "advert_id": "AD001",
        "client_name": "Client A",
        "size": "Full Page",
        "placement": "Back Cover",
        "publication_date": "2025-01-15",
    },
    {
        "advert_id": "AD002",
        "client_name": "Client B",
        "size": "Half Page",
        "placement": "Front Cover",
        "publication_date": "2025-02-01",
    },
    # Invalid Inputs
    {
        "advert_id": "",
        "client_name": "Client C",
        "size": "Quarter Page",
        "placement": "Middle Page",
        "publication_date": "InvalidDate",
    },
    {
        "advert_id": "AD003",
        "client_name": "",
        "size": "InvalidSize",
        "placement": "Side Cover",
        "publication_date": "2025-03-10",
    },
    {
        "advert_id": "AD004",
        "client_name": "Client D",
        "size": "Full Page",
        "placement": "Back Cover",
        "publication_date": "2024-01-15",
    },
]

class TestITMagazineSystem(unittest.TestCase):
    def setUp(self):
        ITMagazineStaff._used_staff_ids.clear()
        # Setup instances
        self.marketing_staff = MarketingDeptStaff(staff_id=100000, salary=50000, dept="Marketing")
        self.editor = Editor(staff_id=200000, salary=60000, dept="Editing")
        self.processing_centre = ProcessingCentreStaff(staff_id=300000, salary=55000, dept="Processing Centre")
    
    def test_staff_initialization(self):
        """Test initialization of staff instances with valid and invalid data"""
        print("test_staff_initialization()\n")

        for data in test_data_for_staff:
            try:
                if data["dept"] == "Marketing":
                    staff = MarketingDeptStaff(data["staff_id"], data["salary"], data["dept"])

                    # Assert valid staff creation
                    self.assertIsInstance(staff, MarketingDeptStaff)
                elif data["dept"] == "Editing":
                    staff = Editor(data["staff_id"], data["salary"], data["dept"])

                    # Assert valid staff creation
                    self.assertIsInstance(staff, Editor)
                elif data["dept"] == "Processing Centre":
                    staff = ProcessingCentreStaff(data["staff_id"], data["salary"], data["dept"])

                    # Assert valid staff creation
                    self.assertIsInstance(staff, ProcessingCentreStaff)
                else:
                    print(f"Invalid department for staff: {data}")
                    continue

                print(f"Created Staff: {staff}")
            except ValueError as e:
                print(f"Failed to create staff with ID {data['staff_id']}: {e}")
        
        print(separator)

    def test_create_advert(self):
        """Test creating adverts with valid and invalid data"""
        print("test_create_advert()\n")

        for data in test_data_for_advert:
            try:
                advert = self.marketing_staff.create_advert(
                    advert_id=data["advert_id"],
                    client_name=data["client_name"],
                    size=data["size"],
                    placement=data["placement"],
                    publication_date=data["publication_date"],
                )
                # Assert valid advert creation
                self.assertIsInstance(advert, Advert)
                self.assertEqual(advert.advert_id, data["advert_id"])
                print(f"Created Advert: {advert}")
            except ValueError as e:
                print(f"Failed to create advert with ID {data['advert_id']}: {e}")
        print(separator)

    def test_update_advert_in_issue(self):
        """Test updating or adding adverts in an issue"""
        print("test_update_advert_in_issue()\n")

        for data in test_data_for_advert:
            try:
                advert = self.marketing_staff.create_advert(**data)
                self.editor.update_advert_in_issue(advert, "2025-02-01")
                # Assert advert added to issue
                self.assertIn(advert, self.editor.magazine_issues["2025-02-01"])
                self.assertEqual(advert.status, "Approved")
            except ValueError as e:
                print(f"Failed to update advert with ID {data['advert_id']}: {e}")
        
        print(separator)

    def test_store_approved_advert(self):
        """Test storing approved adverts in the processing centre"""
        print("test_store_approved_advert()\n")

        for data in test_data_for_advert:
            try:
                advert = self.marketing_staff.create_advert(**data)
                self.editor.update_advert_in_issue(advert, "2025-02")
                self.processing_centre.store_advert(advert)
                # Assert advert is stored
                self.assertIn(advert, self.processing_centre.stored_adverts)
            except Exception as e:
                print(f"Failed to store advert with ID {data['advert_id']}: {e}")

        print(separator)

    def test_prevent_store_non_approved_advert(self):
        """Test preventing storage of non-approved adverts"""
        print("test_prevent_store_non_approved_advert()\n")

        for data in test_data_for_advert:
            try:
                advert = self.marketing_staff.create_advert(**data)
                self.processing_centre.store_advert(advert)
            except Exception as e:
                print(f"Failed to store advert with ID {data['advert_id']}: {e}")
        
        print(separator)

    def test_cancel_advert(self):
        """Test cancelling an advert"""
        print("test_cancel_advert()\n")

        for data in test_data_for_advert:
            try:
                advert = self.marketing_staff.create_advert(**data)

                # Capture the return value of cancel_advert
                cancel_message = self.marketing_staff.cancel_advert(advert.advert_id)

                # Assert the advert status
                self.assertEqual(advert.status, "Cancelled")

                # Print the message from cancel_advert
                print(cancel_message)

                # Step 4: Attempt to update the issue with the cancelled advert
                try:
                    self.editor.update_advert_in_issue(advert, "2025-02-01")
                    print(f"Editor updated issue with cancelled advert ID {advert.advert_id}. This should not happen.")
                except ValueError as e:
                    print(f"Editor could not update issue with cancelled advert ID {advert.advert_id}: {e}")
                    self.assertTrue("cancelled" in str(e).lower())  # Ensure error mentions cancellation or invalid status

            except Exception as e:
                print(f"Failed to cancel advert with ID {data['advert_id']}: {e}")
        
        print(separator)
    

    def tearDown(self):
        ITMagazineStaff._used_staff_ids.clear()

if __name__ == "__main__":
    unittest.main()