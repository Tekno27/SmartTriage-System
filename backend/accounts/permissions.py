from rest_framework.permissions import BasePermission

STAFF_ROLES = {"admin", "nurse", "doctor", "receptionist", "pharmacist", "lab_technician", "radiologist", "accountant"}
CLINICAL_ROLES = {"admin", "nurse", "doctor"}
ADMIN_ROLES = {"admin", "receptionist", "accountant"}


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"nurse", "admin"}


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"doctor", "admin"}


class IsNurseOrDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in CLINICAL_ROLES


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in STAFF_ROLES


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"receptionist", "admin"}


class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"pharmacist", "admin"}


class IsLabTech(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"lab_technician", "admin"}


class IsRadiologist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"radiologist", "admin"}


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"accountant", "admin"}


class IsClinicalOrLab(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in CLINICAL_ROLES | {"lab_technician"}


class IsClinicalOrRadiologist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in CLINICAL_ROLES | {"radiologist"}


class IsClinicalOrPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in CLINICAL_ROLES | {"pharmacist"}
