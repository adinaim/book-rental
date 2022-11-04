from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string
from django.contrib.auth.backends import BaseBackend


class UserManager(BaseUserManager):
    def _create(self, username, password, email, first_name, last_name, birthday, **extra_fields):
        if not username:
            raise ValueError('User must have username')
        if not email:
            raise ValueError('User must have email')
        if not first_name:
            raise ValueError('First name must be set')
        if not last_name:
            raise ValueError('Last name must be set')
        if not birthday:
            raise ValueError('Birthday must be set')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, first_name, last_name, birthday, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        return self._create(username, password, email, first_name, last_name, birthday, **extra_fields)

    def create_superuser(self, username, password, email, first_name, last_name, birthday, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(username, password, email, first_name, last_name, birthday, **extra_fields)


class User(AbstractBaseUser):
    LOCATION_CHOICES = (
        {'bishkek': 'г. Бишкек'},
        {'osh_city': 'г. Ош'},
        {'talas': 'Талас'},
        {'naryn': 'Нарын'},
        {'ik': 'Иссык-Куль'},
        {'osh': 'Ош'},
        {'batken': 'Баткен'},
        {'chui': 'Чуй'},
        {'jalal-abad': 'Джалал-Абад'}
    )

    username = models.CharField('username', max_length=16, primary_key=True)
    first_name = models.CharField('first name', max_length=20)
    last_name = models.CharField('last name', max_length=40)
    email = models.EmailField('email', max_length=255, unique=True)
    birthday = models.DateField()                         # settings include format      # формат как проверяется, выпдает ли календарь
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=16, blank=True)
    # student/teacher/lover

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'birthday']

    def __str__(self) -> str:
        return self.username

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(length=8)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


        # проверка на возраст

# parsing -> search in the db and add to your own library, own / read, что если у него малоизвестный автор -> на проверку модераторам (содержание, не зарпщенка ли)

# books = models.CharField(blank=True)    # чтоб изначально было пусто, а потом можно было добавлять книги

# when adding books to your owning you search in the db books table, retrieve request
# when renting a book you send a retrieve request, if ok you book the book

# как можно осуществить бронировнаие книг, generate qr codes, подумать над логикой, как прохоидт оплата и подтверждение передачи книги