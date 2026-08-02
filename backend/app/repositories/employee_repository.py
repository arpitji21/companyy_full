from sqlalchemy import func, select

from app.models.department import Employee
from app.repositories.base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):
    model = Employee

    def list_all(self) -> list[Employee]:
        return list(self.db.scalars(select(Employee)).all())

    def count_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(Employee.status, func.count()).group_by(Employee.status)
        ).all()
        return {status: count for status, count in rows}

    def count_by_department(self) -> dict[str, int]:
        rows = self.db.execute(
            select(Employee.department_id, func.count()).group_by(Employee.department_id)
        ).all()
        return {dept_id: count for dept_id, count in rows if dept_id}
