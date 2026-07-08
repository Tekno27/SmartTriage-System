from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from patients.models import PatientProfile
from pharmacy.models import Medication, MedicationBatch

User = get_user_model()

DEMO_USERS = [
    {"username": "student1", "password": "demo1234", "role": "student", "first_name": "Ama", "last_name": "Mensah", "student_id": "STU001"},
    {"username": "student2", "password": "demo1234", "role": "student", "first_name": "Kofi", "last_name": "Asante", "student_id": "STU002"},
    {"username": "nurse1", "password": "demo1234", "role": "nurse", "first_name": "Abena", "last_name": "Owusu", "student_id": ""},
    {"username": "doctor1", "password": "demo1234", "role": "doctor", "first_name": "Dr. Kwame", "last_name": "Boateng", "student_id": ""},
]

MEDICATIONS = [
    ("Paracetamol", "Acetaminophen", "tablet"),
    ("Amoxicillin", "Amoxicillin", "capsule"),
    ("Ibuprofen", "Ibuprofen", "tablet"),
]


class Command(BaseCommand):
    help = "Seed demo users, patient profiles, and pharmacy inventory."

    def handle(self, *args, **options):
        for data in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "role": data["role"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "student_id": data["student_id"],
                    "email": f"{data['username']}@ucc.edu.gh",
                },
            )
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                self.stdout.write(f"User exists: {user.username}")

            if user.role == "student":
                PatientProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        "nhis_number": f"NHIS-{user.student_id}",
                        "blood_type": "O+",
                        "allergies": "None known",
                    },
                )

        for name, generic, unit in MEDICATIONS:
            med, _ = Medication.objects.get_or_create(
                name=name,
                defaults={"generic_name": generic, "unit": unit},
            )
            MedicationBatch.objects.get_or_create(
                medication=med,
                batch_number=f"B-{name[:3].upper()}-001",
                defaults={
                    "expiry_date": date.today() + timedelta(days=180),
                    "quantity_on_hand": 200,
                },
            )
            MedicationBatch.objects.get_or_create(
                medication=med,
                batch_number=f"B-{name[:3].upper()}-002",
                defaults={
                    "expiry_date": date.today() + timedelta(days=365),
                    "quantity_on_hand": 150,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write("Login credentials: student1 / nurse1 / doctor1 — password: demo1234")
