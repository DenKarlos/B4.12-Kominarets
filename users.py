import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

# CREATE TABLE user("id" integer primary key autoincrement, "first_name" text,
# "last_name" text, "gender" text, "email" text, "birthdate" text, "height" real);


class User(Base):
    """
    Описывает структуру таблицы user для хранения записей регистрационных данных пользователей
    """
    __tablename__ = "user"

    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)


def connect_db():
    return sessionmaker(sa.create_engine(DB_PATH))()


def fomat_input(correct_words, phrase=''):
    """
    Проверяет формат ввода данных согласно списку и возвращает одно из полученных значений.
    Ввод повторяется, пока пользователь не введёт правильное значение из предложенных
    """
    while True:
        try:
            word = input(
                '{} ({} - необходимый формат ввода): '.format(phrase, '/'.join(correct_words)))
            if word not in correct_words:
                raise Exception('Не соблюдён формат ввода!')
            else:
                return word
        except Exception as ex:
            print(ex)
            print('Попробуйте ещё...')


def email_input():
    """
    Валидатор введённого e-mail
    """
    while True:
        try:
            email = input('Введите e-mail: ')
            if email.count('.') >= 1 and email.count('@') == 1:
                if email.find('@') >= 1:
                    if email.find('.', email.find('@')) >= 2 and email[-1] != '.':
                        return email
            else:
                raise Exception('Такой e-mail навряд ли существует!')
        except Exception as ex:
            print(ex)
            print('Попробуйте ввести ещё раз...')


def date_input(phrase):
    """
    Валидатор введённой даты в предлагаемом формате.
    """
    while True:
        try:
            date_str = input(phrase + ' (в формате "ГГГГ-MM-ДД"): ')
            date = dt.datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except Exception as ex:
            print(ex)
            print('Неверный формат даты. Попробуйте ещё...')


def float_input(phrase, min, max):
    while True:
        try:
            num = float(input(phrase))
            if num < min:
                raise Exception('Число не может быть меньше ' + str(min))
            if num > max:
                raise Exception('Число не может быть больше ' + str(max))
            return num
        except Exception as ex:
            print(ex)
            print('Некорректный ввод данных. Попробуйте ещё...')


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список user
    """
    # выводим приветствие
    print("Здравствуйте! Я запишу персональные данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    gender = fomat_input(('муж', 'жен'), 'Введите пол')
    email = email_input()
    birthdate = date_input('Введите дату рождения')
    height = float_input('Введите рост(см.):', 50, 300)
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def main():
    """
    Осуществляется пользовательский ввод
    """
    main_continue = '1'
    while main_continue == '1':
        session = connect_db()
        # запрашиваем данные пользователя
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
        main_continue = input(
            'Если хотите продолжить ввод данных, то введите "1"')


if __name__ == "__main__":
    main()
