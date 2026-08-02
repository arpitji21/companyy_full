"""
Run once after the first migration to populate baseline reference data:

    python -m app.db.seed

Creates the roles/permissions from the spec and the departments that match
the existing orbit-dashboard frontend's planets, so /api/departments and
/api/roles aren't empty on a fresh database.
"""
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.department import Department
from app.models.user import Permission, Role, User

ROLE_NAMES = [
    "CEO", "Admin", "Manager", "HR", "Finance", "Sales", "Marketing",
    "Research", "Quality", "Regulatory", "Employee", "Viewer", "Compliance", "Investor",
]

DEPARTMENTS = [
    ("CEO", "ceo", "👑"),
    ("Finance", "finance", "💰"),
    ("HR", "hr", "👥"),
    ("Sales", "sales", "📈"),
    ("Marketing", "marketing", "📢"),
    ("Research", "research", "🔬"),
    ("Compliance", "compliance", "⚖️"),
    ("Manufacturing", "manufacturing", "🏭"),
    ("Clinical", "clinical", "🧪"),
    ("Analytics", "analytics", "📊"),
    ("Patent", "patent", "🛡️"),
    ("Docs", "docs", "📝"),
    ("Regulatory", "regulatory", "📋"),
    ("Grant", "grant", "🎯"),
    ("Investor", "investor", "🤝"),
    ("Tender", "tender", "📄"),
    ("Customer", "customer", "💬"),
    ("Procurement", "procurement", "🚚"),
    ("Quality", "quality", "✅"),
    ("Supply Chain", "supplychain", "🔗"),
]

# code format: "<module>:<action>" — kept intentionally small; expand as
# real endpoints in each department module go live.
PERMISSION_CODES = [
    "users:read", "users:write",
    "departments:read", "departments:write",
    "finance:read", "finance:write",
    "hr:read", "hr:write",
]


# Single demo login that can see every department's data. `is_superuser=True`
# and the CEO role both already bypass every `require_roles(...)` check in
# app/api/v1/*, so this one account is all that's needed to explore the
# whole console — no per-department accounts required.
DEMO_CEO_EMAIL = "ceo@larkhealthcare.demo"
DEMO_CEO_PASSWORD = "OrbitDemo!2026"


def seed() -> None:
    db = SessionLocal()
    try:
        for name in ROLE_NAMES:
            if not db.query(Role).filter(Role.name == name).first():
                db.add(Role(name=name))

        for code in PERMISSION_CODES:
            if not db.query(Permission).filter(Permission.code == code).first():
                db.add(Permission(code=code))

        db.commit()

        for name, slug, icon in DEPARTMENTS:
            if not db.query(Department).filter(Department.slug == slug).first():
                db.add(Department(name=name, slug=slug, icon=icon))

        db.commit()

        if not db.query(User).filter(User.email == DEMO_CEO_EMAIL).first():
            ceo_role = db.query(Role).filter(Role.name == "CEO").first()
            ceo_department = db.query(Department).filter(Department.slug == "ceo").first()
            db.add(
                User(
                    email=DEMO_CEO_EMAIL,
                    hashed_password=hash_password(DEMO_CEO_PASSWORD),
                    full_name="Demo CEO",
                    role_id=ceo_role.id if ceo_role else None,
                    department_id=ceo_department.id if ceo_department else None,
                    is_active=True,
                    is_email_verified=True,
                    is_superuser=True,
                )
            )
            db.commit()

        print(f"Seeded {len(ROLE_NAMES)} roles, {len(PERMISSION_CODES)} permissions, {len(DEPARTMENTS)} departments.")
        print(f"Demo login -> email: {DEMO_CEO_EMAIL}  password: {DEMO_CEO_PASSWORD}")
        print("This one account has CEO role + is_superuser, so it can open every department in the console.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
