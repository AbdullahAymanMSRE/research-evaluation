from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

from unistruct.models import Faculty

class UserManager(BaseUserManager):
    def create_user(self, national_id, name, doctor, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not national_id:
            raise ValueError('Users must have an email address')
        user = self.model(
            national_id=national_id,
            name=name,
            doctor=doctor,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, national_id, name, doctor, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            national_id,
            name,
            doctor,
            password=password,
        )
        user.dprtmngr = True
        user.staff = True
        user.control_head = True
        
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id,name, doctor, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            national_id,
            name,
            doctor,
            password=password,
        )
        user.dprtmngr = True
        user.staff = True
        user.control_head = True
        user.admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    # BOTH
    national_id = models.CharField(
        verbose_name='national id',
        max_length=255,
        unique=True,
    )
    name = models.CharField(verbose_name="name", max_length=300)
    tel_number = models.CharField(max_length=300, validators = [RegexValidator(regex="(201)[0-9]{9}'}", message='invalid telephone number')], null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    doctor = models.BooleanField(verbose_name="professor", default=True)
    faculty = models.ForeignKey('unistruct.Faculty', on_delete=models.CASCADE, related_name='users', null=True)
    subjects = models.ManyToManyField('unistruct.Subject', related_name='users', blank=True)
    

    # DOCTOR
    dprtmngr = models.BooleanField(verbose_name="Department Head", default=False)
    department = models.ForeignKey('unistruct.Department', on_delete=models.CASCADE, related_name='doctors', null=True, blank=True)
    control_head = models.BooleanField(verbose_name="Control Head", default=False)

    # STUDENT
    official_email = models.EmailField(verbose_name="Official Email", null=True, blank=True)
    official_email_passwd = models.CharField(verbose_name="Official Email Password", max_length=300, null=True, blank=True)
    team = models.ForeignKey('unistruct.Team', verbose_name="Group", on_delete=models.CASCADE, null=True, blank=True)


    # DJANGO RELATED STUFF
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser


    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['name', 'doctor'] # Email & Password are required by default.

    class Meta:
        ordering = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def subjects_list(self):
        return self.subjects.all()

    @property
    def last_student_researches(self):
        return self.student_researches.all().reverse()[0]


    @property
    def studnet_researches_list(self):
        return self.student_researches.all()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    
