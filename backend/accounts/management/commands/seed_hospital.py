"""Seed full hospital management system demo data."""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from admissions.models import Surgery
from hospital.models import Bed, Department, Theatre, Ward
from inventory.models import SupplyBatch, SupplyCategory, SupplyItem
from laboratory.models import LabTest
from patients.models import PatientProfile
from pharmacy.models import Medication, MedicationBatch
from radiology.models import ImagingType

User = get_user_model()

STAFF = [
    {"username": "admin1", "role": "admin", "first_name": "System", "last_name": "Admin", "employee_id": "EMP001"},
    {"username": "reception1", "role": "receptionist", "first_name": "Efua", "last_name": "Addo", "employee_id": "EMP002"},
    {"username": "pharmacist1", "role": "pharmacist", "first_name": "Yaw", "last_name": "Mensah", "employee_id": "EMP003"},
    {"username": "labtech1", "role": "lab_technician", "first_name": "Akosua", "last_name": "Darko", "employee_id": "EMP004"},
    {"username": "radiologist1", "role": "radiologist", "first_name": "Kweku", "last_name": "Annan", "employee_id": "EMP005"},
    {"username": "accountant1", "role": "accountant", "first_name": "Ama", "last_name": "Osei", "employee_id": "EMP006"},
]

DEPARTMENTS = [
    ("General Medicine", "GMED", "Outpatient and general consultations"),
    ("Emergency", "ER", "Emergency and trauma care"),
    ("Surgery", "SURG", "Surgical procedures and theatre"),
    ("Laboratory", "LAB", "Diagnostic laboratory services"),
    ("Radiology", "RAD", "Medical imaging services"),
    ("Pharmacy", "PHARM", "Medication dispensing"),
    ("Maternity", "MAT", "Maternal and child health"),
]

LAB_TESTS = [
    ("Malaria RDT", "MAL-RDT", "parasitology", "Negative/Positive", "", "15.00"),
    ("Full Blood Count", "FBC", "hematology", "4.5-11.0", "x10⁹/L", "35.00"),
    ("Blood Glucose", "GLU", "biochemistry", "3.9-6.1", "mmol/L", "20.00"),
    ("Urinalysis", "URINE", "urinalysis", "Normal", "", "18.00"),
    ("Widal Test", "WIDAL", "serology", "Negative", "", "25.00"),
    ("HIV Screening", "HIV", "serology", "Negative", "", "30.00"),
    ("Liver Function", "LFT", "biochemistry", "Normal", "", "45.00"),
    ("Blood Group", "BG", "hematology", "A/B/AB/O", "", "15.00"),
]

IMAGING = [
    ("Chest X-Ray", "CXR", "xray", "Chest", "50.00"),
    ("Abdominal Ultrasound", "US-ABD", "ultrasound", "Abdomen", "80.00"),
    ("Pelvic Ultrasound", "US-PEL", "ultrasound", "Pelvis", "80.00"),
    ("Skull X-Ray", "XR-SKULL", "xray", "Head", "45.00"),
]

SUPPLIES = [
    ("Surgical Gloves", "SUP-GLV", "PPE", "box", 50),
    ("Syringes 5ml", "SUP-SYR", "Consumables", "unit", 100),
    ("IV Cannula", "SUP-CAN", "Consumables", "unit", 30),
    ("Gauze Bandage", "SUP-GAU", "Wound Care", "roll", 40),
    ("Face Masks", "SUP-MSK", "PPE", "box", 25),
]


class Command(BaseCommand):
    help = "Seed hospital departments, wards, beds, lab tests, imaging, inventory, and staff."

    def handle(self, *args, **options):
        self.stdout.write("Seeding hospital infrastructure...")

        depts = {}
        for name, code, desc in DEPARTMENTS:
            d, _ = Department.objects.get_or_create(code=code, defaults={"name": name, "description": desc})
            depts[code] = d

        wards_config = [
            ("General Ward A", "GMED", "general", 8),
            ("General Ward B", "GMED", "general", 6),
            ("Emergency Bay", "ER", "emergency", 4),
            ("ICU", "ER", "icu", 3),
            ("Maternity Ward", "MAT", "maternity", 5),
            ("Pediatric Ward", "GMED", "pediatric", 4),
        ]
        for wname, dcode, wtype, bed_count in wards_config:
            ward, _ = Ward.objects.get_or_create(
                name=wname, department=depts[dcode],
                defaults={"ward_type": wtype, "floor": "1"},
            )
            for i in range(1, bed_count + 1):
                Bed.objects.get_or_create(ward=ward, bed_number=f"{i:02d}")

        for tname, dcode in [("Theatre 1", "SURG"), ("Theatre 2", "SURG")]:
            Theatre.objects.get_or_create(name=tname, department=depts[dcode])

        for name, code, cat, nr, unit, price in LAB_TESTS:
            LabTest.objects.get_or_create(code=code, defaults={
                "name": name, "category": cat, "normal_range": nr, "unit": unit, "price": Decimal(price),
            })

        for name, code, mod, part, price in IMAGING:
            ImagingType.objects.get_or_create(code=code, defaults={
                "name": name, "modality": mod, "body_part": part, "price": Decimal(price),
            })

        categories = {}
        for sname, sku, cat, unit, reorder in SUPPLIES:
            if cat not in categories:
                categories[cat], _ = SupplyCategory.objects.get_or_create(name=cat)
            item, _ = SupplyItem.objects.get_or_create(sku=sku, defaults={
                "name": sname, "category": categories[cat], "unit": unit, "reorder_level": reorder,
            })
            SupplyBatch.objects.get_or_create(item=item, batch_number=f"B-{sku}", defaults={
                "quantity_on_hand": reorder * 3, "expiry_date": date.today() + timedelta(days=365),
            })

        for med_name, generic, unit in [("Paracetamol", "Acetaminophen", "tablet"), ("Amoxicillin", "Amoxicillin", "capsule"), ("Ibuprofen", "Ibuprofen", "tablet"), ("ORS Sachets", "Oral Rehydration", "sachet")]:
            med, _ = Medication.objects.get_or_create(name=med_name, defaults={"generic_name": generic, "unit": unit})
            MedicationBatch.objects.get_or_create(medication=med, batch_number=f"B-{med_name[:3].upper()}", defaults={
                "expiry_date": date.today() + timedelta(days=180), "quantity_on_hand": 200,
            })

        for data in STAFF:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "role": data["role"], "first_name": data["first_name"],
                    "last_name": data["last_name"], "employee_id": data["employee_id"],
                    "email": f"{data['username']}@ucc.edu.gh",
                },
            )
            if created:
                user.set_password("demo1234")
                user.save()
                self.stdout.write(f"  Staff: {user.username} ({user.role})")

        students = [
            {"username": "student1", "first_name": "Ama", "last_name": "Mensah", "student_id": "STU001"},
            {"username": "student2", "first_name": "Kofi", "last_name": "Asante", "student_id": "STU002"},
        ]
        for s in students:
            user, created = User.objects.get_or_create(
                username=s["username"],
                defaults={**s, "role": "student", "email": f"{s['username']}@ucc.edu.gh"},
            )
            if created:
                user.set_password("demo1234")
                user.save()
            PatientProfile.objects.get_or_create(user=user, defaults={
                "nhis_number": f"NHIS-{s['student_id']}", "ghana_card_number": f"GHA-{s['student_id']}",
                "blood_type": "O+", "nhis_status": "active",
            })

        for uname, role, fn, ln, eid in [
            ("nurse1", "nurse", "Abena", "Owusu", "EMP010"),
            ("doctor1", "doctor", "Kwame", "Boateng", "EMP011"),
        ]:
            user, created = User.objects.get_or_create(
                username=uname,
                defaults={"role": role, "first_name": fn, "last_name": ln, "employee_id": eid, "email": f"{uname}@ucc.edu.gh"},
            )
            if created:
                user.set_password("demo1234")
                user.save()

        self.stdout.write(self.style.SUCCESS("Hospital seed complete. All passwords: demo1234"))
