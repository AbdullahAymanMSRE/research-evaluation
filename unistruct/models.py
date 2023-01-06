from django.db import models

# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    @property
    def members_list(self):
        mems = []
        for m in self.users.filter(doctor= True):
            mems.append(m)
        return mems

    @property
    def teams_list(self):
        tems = []
        for t in self.teams.all():
            tems.append(t)
        return tems

    @property
    def departments_list(self):
        deprts = []
        for d in self.departments.all():
            deprts.append(d)
        return deprts

    @property
    def subjs_number(self):
        secns = 0
        for t in self.teams.all():
            for s in t.subjects.all(): 
                secns += 1
        return secns

class Team(models.Model):
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.faculty.name}"
    
    @property
    def students_list(self):
        return self.user_set.filter(doctor=False)

    @property
    def subjects_list(self):
        secns = []
        for s in self.subjects.all():
            secns.append(s)
        return secns

    @property
    def success_percentage(self):
        a = 0
        s = 0
        for su in self.subjects.all():
            for r in su.researches.all():
                for sr in r.student_researches.filter(corrected=True):
                    a+=1
                    if sr.passed:
                        s+=1
        try:
            return (s/a)*100
        except ZeroDivisionError:
            return 0

    @property
    def sdone(self):
        val = True
        for subject in self.subjects.all():
            if not subject.done:
                val = False
                break
        return val

class Department(models.Model):
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @property
    def sections_list(self):
        secns = []
        for s in self.sections.all():
            secns.append(s)
        return secns

    @property
    def subjs_number(self):
        subjs = 0
        for se in self.sections.all():
            for s in se.subjects.all():
                subjs += 1
        return subjs

    @property
    def members_list(self):
        return self.doctors.all()

class Section(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.department}'


    @property
    def teams_list(self):
        secns = []
        for s in self.subjects.all():
            if not s.team in secns:
                secns.append(s.team)
        return secns

    @property
    def subjects_list(self):
        subjs = []
        for s in self.subjects.all():
            subjs.append(s.name)
        return subjs

class Subject(models.Model):
    section = models.ForeignKey(
        "Section", on_delete=models.CASCADE, related_name="subjects", null=True, blank=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=200)
    rseen = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def researches_list(self):
        return self.researches.all()

    @property
    def len_researches_list(self):
        return len(self.researches.all())

    @property
    def len_students(self):
        return len(self.users.filter(doctor=False).all())

    @property
    def student_researches_list(self):
        final_list = []
        for research in self.researches.all():
            for student_research in research.student_researches.all():
                final_list.append(student_research)
        return final_list

    @property
    def len_student_researches_list(self):
        final_list = []
        for research in self.researches.all():
            for student_research in research.student_researches.all():
                final_list.append(student_research)
        return len(final_list)

    @property
    def success_percentage(self):
        a = 0
        s = 0
        for r in self.researches.all():
            for sr in r.student_researches.filter(corrected=True):
                a+=1
                if sr.passed:
                    s+=1
        try:
            return (s/a)*100
        except ZeroDivisionError:
            return 0

