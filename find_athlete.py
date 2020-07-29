import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# Автоматическое создание классов на основе таблиц из указанной БД
Base = automap_base()
Base.prepare(sa.create_engine(DB_PATH), reflect=True)
Athelete = Base.classes.athelete

def connect_db():
    return sessionmaker(sa.create_engine(DB_PATH))()

# Описание структуры необходимой таблицы для выполнения задания
# CREATE TABLE athelete("id" integer primary key autoincrement, "age" integer,
# "birthdate" text,"gender" text,"height" real,"name" text,"weight" integer,
# "gold_medals" integer,"silver_medals" integer,"bronze_medals" integer,
# "total_medals" integer,"sport" text,"country" text);

def int_input(phrase):
    """
    Вилидатор ввода целого числа
    """
    while True:
        try:
            num = int(input(phrase))
            return num
        except Exception as ex:
            print(ex)
            print('Некорректный ввод данных. Попробуйте ещё...')


def find_neighbour(athelete_id, session):
    """
    Производит поиск атлета в таблице athelete по заданному id (если такой id cуществует)
    и вывод соседей по дате рождения и росту    
    """
    # находим запись в таблице Athelete, у которой поле Athelete.id совпадает с параметром athelete_id
    athelete = session.query(Athelete).filter(Athelete.id == athelete_id).first()
    if athelete:
        print(athelete.id, athelete.name, athelete.birthdate, athelete.height, '- найденный атлет')
        # составляем список идентификаторов пользователей упорядоченных по дате рождения
        user_ids = [user.id for user in session.query(Athelete).order_by(Athelete.birthdate).all()]
        # находим id соседа по дате рождения
        # узнаём индекс следующего соседа, но если сосед последний в очереди,
        # то узнаём индекс предыдущего соседа
        neighbour_indx = user_ids.index(athelete_id) + 1
        if neighbour_indx != len(user_ids):
            neighbour_id = user_ids[neighbour_indx]
        else:
            neighbour_id = user_ids[neighbour_indx - 2]
        neighbour = session.query(Athelete).filter(Athelete.id == neighbour_id).first()
        print(neighbour.id, neighbour.name, neighbour.birthdate, neighbour.height, '- cосед по дате рождения')
        # составляем список идентификаторов пользователей упорядоченных по росту спортсменов
        user_ids = [user.id for user in session.query(Athelete).order_by(Athelete.height).all()]
        # находим id соседа по росту
        # узнаём индекс следующего соседа, но если сосед последний в очереди,
        # то узнаём индекс предыдущего соседа
        neighbour_indx = user_ids.index(athelete_id) + 1
        if neighbour_indx != len(user_ids):
            neighbour_id = user_ids[neighbour_indx]
        else:
            neighbour_id = user_ids[neighbour_indx - 2]
        neighbour = session.query(Athelete).filter(Athelete.id == neighbour_id).first()
        print(neighbour.id, neighbour.name, neighbour.birthdate, neighbour.height, '- cосед по росту')
    else:
        print('Атлета с таким id не существует')


def main():
    """
    Осуществляется поиск атлета по id и вывод соседей по росту и дате рождения
    """
    main_continue = '1'
    while main_continue == '1':
        session = connect_db()
        athelete_id = int_input('Введите идентификатор атлета (целое число): ')
        #Производим все необходимые действия, согласно условию задачи
        find_neighbour(athelete_id, session)        
        main_continue = input('Если хотите продолжить поиск, то введите "1"')


if __name__ == "__main__":
    main()
