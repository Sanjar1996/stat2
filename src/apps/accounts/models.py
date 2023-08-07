from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, Group, PermissionsMixin)
from ..core.models import TimestampedModel

USER_STATUSES = (
    (1, 'New'),
    (2, 'Active'),
    (3, 'Deleted')
)
ADDRESS_STATUSES = (
    (1, 'Active'),
    (2, 'Deleted')
)

ADDRESS_TYPES = (
    (1, 'Home'),
    (2, 'Office'),
)

GENDER_TYPES = (
    (1, "Male"),
    (2, "Female"),
    (3, "NOT PREFERRED")
)
CRIPPLE_TYPE = (
    (1, "Yoq"),
    (2, "Xa")
)
STATES_STATUSES = (
    (1, "Active"),
    (2, "Delete"),
    (3, 'In Active')
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_staffuser(self, email, password):
        if not password:
            raise ValueError('staff/admins must have a password.')
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password):
        if not password:
            raise ValueError('superusers must have a password.')
        user = self.create_user(email, password=password, is_superuser=True)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Nation(TimestampedModel):
    """Millati"""
    name = models.CharField(max_length=50, blank=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "nation"
        verbose_name_plural = "Nation"


class Position(TimestampedModel):
    """Lavozimi"""
    name = models.CharField(max_length=120, blank=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "position"
        verbose_name_plural = "Position"


class Region(TimestampedModel):
    name = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)
    sort = models.IntegerField(blank=True, null=True, verbose_name='SORT NUMBER')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort',)
        db_table = "region"
        verbose_name_plural = "Region"


class Department(TimestampedModel):
    parent_id = models.ForeignKey("self", on_delete=models.SET_NULL, related_name='department_child', null=True,
                                  blank=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="department_region")
    sort = models.IntegerField(blank=True, null=True, verbose_name='SORT NUMBER')
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort', )
        db_table = "department"
        verbose_name_plural = "Department"


class Information(models.Model):
    """Ma'lumoti"""
    name = models.CharField(max_length=50, blank=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "information"
        verbose_name_plural = "Information"


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    email = models.EmailField(verbose_name='email address', max_length=255, db_index=True, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mid_name = models.CharField(max_length=255, blank=True, null=True)
    information = models.ForeignKey(
        Information, verbose_name="Ma'lumotu", on_delete=models.SET_NULL, max_length=120, blank=True, null=True,
        related_name="user_information")
    position = models.ForeignKey(Position,
                                 on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Lavozimi",
                                 related_name="user_position")
    temporary_work = models.CharField(max_length=255, blank=True, null=True,
                                      verbose_name="Вақтинча меҳнатга лаёқатсизлиги (соҳада ишлаган вақтида неча маротаба)")
    national = models.ForeignKey(Nation, on_delete=models.SET_NULL, blank=True, null=True, related_name="user_national")

    groups = models.ManyToManyField(Group, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="user_department", blank=True, null=True)
    status = models.IntegerField(choices=USER_STATUSES, default=1)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email and password required by default

    objects = UserManager()

    def __int__(self):
        return self.id

    def __str__(self):
        return str(self.email)

    def role(self):
        return " | ".join(item.name for item in self.groups.all())

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return True  # does user have a specific permision, simple answer - yes
    #
    # def has_module_perms(self, app_label):
    #     return True  # does user have permission to view the app 'app_label'?

    def get_absolute_url(self):
        return reverse('accounts:accounts_update', kwargs={'pk': self.pk})


class UserInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_information")
    year_of_graduation = models.DateTimeField(verbose_name="OTM tugatgan yili", blank=True, null=True)
    name_of_graduation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Oliy talim nomi va joyi")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Tugilgan yili")
    birth_place = models.CharField(max_length=400, blank=True, null=True, verbose_name="Tugilgan joyi")
    specialization = models.CharField(max_length=400, blank=True, null=True, verbose_name="Mutahasislik")
    passport_number = models.CharField(
        max_length=500, verbose_name="Pasport seriya va raqami qachon kim tomonidan berilganligi",
        blank=True, null=True)
    start_position_date = models.DateTimeField(verbose_name="Lavozim boshlangan vaqt", blank=True, null=True)
    end_position_date = models.DateTimeField(verbose_name="Lavozim tugallagan vaqt", blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_TYPES, default=1)
    residence_address = models.CharField(max_length=400, blank=True, null=True, verbose_name="Yashash joyi MFY")
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    academic_degree = models.CharField(max_length=255, blank=True, null=True, verbose_name="ilmiy daraja,unvon,diplom raqami")
    diploma_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Diplom raqami")
    tour = models.CharField(max_length=255, blank=True, null=True, verbose_name="Qaysi chet ellarda bolgansiz qachon qayerda")
    favorite_party = models.CharField(max_length=400, blank=True, null=True, verbose_name="Qaysi partiya a'zosi")
    languages = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="Qaysi chet tillarini bilasiz qay darajada")
    family_number = models.PositiveIntegerField(blank=True, null=True, verbose_name="oilangiz nech kishidan iborat")
    people_deputy = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="Xalq deputatat azosimi agar bolsa toliq malumot")
    state_award = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="Давлат мукофотлари билан тақдирланганми (қанақа)")
    cripple = models.IntegerField(choices=CRIPPLE_TYPE, default=1, verbose_name="Ногиронлиги")
    military_service = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="Ҳарбий хизматга муносабати ва ҳарбий унвони")
    judicial = models.CharField(max_length=400, blank=True, null=True,
        verbose_name="Суд жавобгарлигига тортилган бўлсангиз, қачон ва нима учун")

    is_judicial = models.BooleanField(default=False)
    resume = models.FileField(upload_to='files/', null=True, blank=True)

    class Meta:
        db_table = "user_information"
        verbose_name_plural = "UserInformation"

    def __int__(self):
        return self.id


class UserDepartment(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    regions = models.ManyToManyField(Region)
    departments = models.ManyToManyField(Department)

    def __str__(self):
        return f"{self.user.email}"

    @property
    def region(self):
        return " | ".join(reg.name for reg in self.regions.all())

    @property
    def department(self):
        return " | ".join(f'{dep.name[:10]}...' for dep in self.departments.all())

    class Meta:
        db_table = "user_departments"
        verbose_name_plural = "User Departments"


class Address(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    home_number = models.CharField(max_length=50, blank=True, null=True)
    home_no = models.CharField(max_length=50, blank=True, null=True)
    type = models.IntegerField(choices=ADDRESS_TYPES)
    status = models.IntegerField(choices=ADDRESS_STATUSES)

    def __int__(self):
        return self.id

    def __str__(self):
        if self.address1 is not None:
            return f"{self.address1}"
        else:
            return f"{self.address2}"

    class Meta:
        db_table = "address"
        verbose_name_plural = "Addresses"
