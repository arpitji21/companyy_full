from __future__ import annotations

from app.core.exceptions import NotFoundError
from app.models.department import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, OrgChartNode


class EmployeeService:
    def __init__(self, db):
        self.db = db
        self.repo = EmployeeRepository(db)

    def get(self, employee_id: str) -> Employee:
        emp = self.repo.get(employee_id)
        if not emp:
            raise NotFoundError("Employee not found.")
        return emp

    def list(self, page: int, page_size: int, department_id: str | None = None, status: str | None = None):
        return self.repo.list(page=page, page_size=page_size, department_id=department_id, status=status)

    def create(self, data: EmployeeCreate) -> Employee:
        emp = Employee(**data.model_dump())
        return self.repo.create(emp)

    def update(self, employee_id: str, data: EmployeeUpdate) -> Employee:
        emp = self.get(employee_id)
        return self.repo.update(emp, data.model_dump(exclude_unset=True))

    def terminate(self, employee_id: str) -> Employee:
        emp = self.get(employee_id)
        return self.repo.update(emp, {"status": "terminated"})

    # --- HR aggregate views ---
    def headcount_summary(self) -> dict:
        by_status = self.repo.count_by_status()
        by_department = self.repo.count_by_department()
        total = sum(by_status.values())
        return {
            "total_employees": total,
            "active": by_status.get("active", 0),
            "on_leave": by_status.get("on_leave", 0),
            "onboarding": by_status.get("onboarding", 0),
            "terminated": by_status.get("terminated", 0),
            "by_department": by_department,
        }

    def org_chart(self) -> list[OrgChartNode]:
        employees = self.repo.list_all()
        by_id = {e.id: e for e in employees}
        children: dict[str | None, list] = {}
        for e in employees:
            children.setdefault(e.manager_id, []).append(e)

        def build(emp) -> OrgChartNode:
            return OrgChartNode(
                id=emp.id,
                full_name=emp.full_name,
                job_title=emp.job_title,
                department_id=emp.department_id,
                reports=[build(child) for child in children.get(emp.id, [])],
            )

        # Roots = employees whose manager is None or whose manager isn't in this dataset.
        roots = [e for e in employees if e.manager_id is None or e.manager_id not in by_id]
        return [build(r) for r in roots]
