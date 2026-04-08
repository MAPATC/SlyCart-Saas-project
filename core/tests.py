import pytest
from .services import create_user
from .models import TelegramUser, OwnerProfile, Tariff
# Create your tests here.


@pytest.mark.django_db # Разрешение на то, чтобы обратится к базе данных. 
# Это дает временный доступ к базе данных, после теста данные удаляются
def test_services():

    create_user(telegram_id=12345, role="owner", brand_name="kapitoshka")

    assert TelegramUser.objects.count() == 1

    assert OwnerProfile.objects.filter(owner__user_id=12345).exists()
    profile = OwnerProfile.objects.get(owner__user_id=12345) # в этом случае join-ы(в QuerySet-ах) нельзя писать через точку, только через "__"!

    assert profile.tariff.plan == "Бесплатный"
    assert profile.brand_name == "kapitoshka"

@pytest.mark.django_db 
def test_create_user_with_incorrect_role():

    with pytest.raises(ValueError) as excinfo:
        create_user(telegram_id=777, role='hacker')

    assert str(excinfo.value) == "Такой роли не существует!"

@pytest.mark.django_db
def test_create_user_duplicate_id():

    create_user(telegram_id=999, role="customer", phone_number="89991234567")
    # Здесь нам нужен менеджер контекста, чтобы обработать ошибку и тест не завершился с ошибкой даже не начавшись
    with pytest.raises(ValueError) as excinfo: # excinfo это целый объект-контейнер от pytest
        create_user(telegram_id=999, role="owner") 

    assert str(excinfo.value) == "Такой пользователь уже существует!"