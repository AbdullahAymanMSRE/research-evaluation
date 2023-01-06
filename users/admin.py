import io
import xlsxwriter

from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Q

from .models import User

class EmailListFilter(admin.SimpleListFilter):

    title = "Email"

    parameter_name = "has_email"

    def lookups(self, request, model_admin):
        all_tuple = [
            ("yes", ("Yes")),
            ("no", ("No")),
        ]

        return all_tuple

    def queryset(self, request, queryset):

        if self.value() == "yes":
            return queryset.filter(email__isnull=False).exclude(email="")

        if self.value() == "no":
            return queryset.filter(Q(email__isnull=True) | Q(email__exact=""))
        if not self.value():
            return queryset

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    actions = ["export_as_excel"]

    list_display=('name',
                  'national_id',
                  'email',
                  'official_email',
                  'official_email_passwd',
                  'doctor',
                  'faculty', 
                  'dprtmngr',
                  'department',
                  'control_head',
                  'team',
                  'active',
                  'staff',
                  'admin'
                  )

    search_fields = ('name', 'national_id', 'id')

    list_filter = (
        EmailListFilter,
        "doctor",
        "faculty",
        "dprtmngr",
        "department",
        "control_head",
        "team",
        "staff",
    )

    def export_as_excel(self, request, queryset):

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet()

        sheet.write(0, 0, "id")
        sheet.write(0, 1, "Name")
        sheet.write(0, 2, "National_id")
        sheet.write(0, 3, "Email")
        sheet.write(0, 4, "Doctor")
        sheet.write(0, 5, "Faculty")
        sheet.write(0, 6, "Dprtmngr")
        sheet.write(0, 7, "Department")
        sheet.write(0, 8, "Control_head")
        sheet.write(0, 9, "Team")
        sheet.write(0, 10, "Active")
        sheet.write(0, 11, "Staff")
        sheet.write(0, 12, 'Official Email')
        sheet.write(0, 13, 'Official Email Passwd')

        for i, usr in enumerate(queryset):
            sheet.write(i + 1, 0, i + 1)
            sheet.write(i + 1, 1, usr.name)
            sheet.write(i + 1, 2, usr.national_id)
            sheet.write(i + 1, 3, usr.email)
            sheet.write(i + 1, 4, usr.doctor)
            sheet.write(i + 1, 5, usr.faculty.name)
            sheet.write(i + 1, 6, usr.dprtmngr)
            try:
                sheet.write(i + 1, 7, usr.department.name)
                sheet.write(i + 1, 9, usr.team.name)
                sheet.write(i + 1, 12, usr.official_email)
                sheet.write(i + 1, 13, usr.official_email_passwd)
            except:
                pass
            sheet.write(i + 1, 8, usr.control_head)
            sheet.write(i + 1, 10, usr.active)
            sheet.write(i + 1, 11, usr.staff)

        workbook.close()
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f"attachment;filename=users.xlsx"
        response.write(output.getvalue())
        return response


admin.site.register(User, UsersAdmin)
