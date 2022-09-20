import psycopg2
flag = True

with psycopg2.connect(database="homeworkdb", user="postgres", password="051289KsV!") as conn:
    with conn.cursor() as cur:
        def create_tables():
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
        	id SERIAL PRIMARY KEY,
        	name VARCHAR(40) NOT NULL,
        	surname VARCHAR(40) NOT NULL,
        	email VARCHAR(100) UNIQUE NOT NULL
            );
            """)
            conn.commit()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
        	id SERIAL PRIMARY KEY,
        	phone INTEGER,
        	user_id INTEGER 
            );
            """)
            conn.commit()


        def add_user():
            name = input('Введите имя нового пользователя: ')
            surname = input('Введите фамилию нового пользователя: ')
            email = input('Введите email нового пользователя: ')
            cur.execute("""
            INSERT INTO phonebook (name, surname, email) VALUES
            (%s, %s, %s);
            """, (name, surname, email))
            conn.commit()
            ##тут же получаем id пользователя, чтобы использовать в таблице с номерами
            cur.execute("""
            SELECT id FROM phonebook WHERE email=%s
            """, (email,))
            user_id = cur.fetchone()[0]
            answer = input('Хотите добавить телефон? y/n ')
            if answer == 'y':
                number = input('Введите номер, не более 20 цифр ')
                cur.execute("""
                INSERT INTO phones (phone, user_id) VALUES (%s, %s);
                """, (number, user_id))
                conn.commit()
            else:
                print('Функцию добавления номера можно вызвать отдельно')


        def add_phone():
            answer = input('По какому параметру проведём поиск ID? (name, surname, email) ')
            answer = search(answer)
            if answer is not None:
                user_id = answer
                number = input('Введите номер, не более 20 цифр ')
                cur.execute("""
                INSERT INTO phones (phone, user_id) VALUES (%s, %s);
                """, (number, user_id))
                conn.commit()
            else:
                print('Повторите поиск')


        def delete_tables():
            cur.execute("""
            DROP TABLE phones;
            """)
            conn.commit()
            cur.execute("""
            DROP TABLE phonebook;
            """)
            conn.commit()


        def delete_phone():
            answer = input('Какой параметр вы знаете? (id или phone) ')
            if answer == 'id':
                user_id = input('Введите ID ')
                cur.execute("""
                DELETE FROM phones WHERE user_id = '%s';
                """, (user_id,))
                conn.commit()
            elif answer == 'phone':
                user_id = search(answer)
                cur.execute("""
                DELETE FROM phones WHERE user_id = '%s';
                """, (user_id,))
                conn.commit()
            else:
                print('Повторите поиск')


        def search(param):
            if param == 'name' or param == 'surname' or param == 'email':
                search_param = input('Введите значение ')
                cur.execute(f"""
                SELECT id FROM phonebook WHERE {param}=%s; 
                """, (search_param,))
                user_id = cur.fetchone()
                if user_id is None:
                    print(f'Пользователя с {search_param} нет в столбце {param}')
                else:
                    print(f'ID пользователя с {search_param} - {user_id[0]}')
                    return user_id[0]
            elif param == 'phone':
                search_param = input('Введите значение ')
                search_param = int(search_param)
                cur.execute(f"""
                SELECT id FROM phones WHERE {param}=%s; 
                """, (search_param,))
                user_id = cur.fetchone()
                if user_id is None:
                    print(f'Пользователя с {search_param} нет в столбце {param}')
                else:

                    print(f'ID пользователя с {search_param} - {user_id[0]}')
                    return user_id[0]
            else:
                print('По этому параметру нельзя произвести поиск')


        def update():
            answer = input('Введит параметр, который вы хотите обновить: name, surname, email или phone ')
            user_id = search(answer)
            print(user_id)
            if user_id is not None:
                if answer == 'name' or answer == 'surname' or answer == 'email':
                    updated_param = input(f'Введите новое значение {answer} ')
                    cur.execute(f"""
                    UPDATE phonebook SET {answer}=%s WHERE id={user_id}; 
                    """, (updated_param,))
                    conn.commit()
                elif answer == 'phone' and user_id is not None:
                    updated_param = str(input(f'Введите новое значение {answer} '))
                    cur.execute(f"""
                    UPDATE phonebook SET {answer}=%s WHERE user_id={user_id}; 
                    """, (updated_param,))
                    conn.commit()
            else:
                print('С таким значением параметра пользователь не найден, повторите попытку')

        def delete_user():
            search_param = input(
                'По какому параметру ищем пользователя для удаления? (id, name, surname, email или phone) ')
            if search_param == 'id':
                user_id = input('Введите значение id ')
                cur.execute("""
                DELETE FROM phones WHERE user_id =%s;
                """, (user_id, ))
                cur.execute("""
                DELETE FROM phonebook WHERE id =%s;
                """, (user_id, ))
                conn.commit()
            elif search_param == 'name' or search_param == 'surname' or search_param == 'email':
                user_id = search(search_param)
                cur.execute("""
                DELETE FROM phones WHERE user_id =%s;
                DELETE FROM phonebook WHERE id =%s;
                """, (user_id, user_id))
                conn.commit()
            else:
                print('Нельзя осуществить поиск и удалени по такому параметру')


        def show_all():
            cur.execute("""
            SELECT phone, user_id FROM phones;
            """)
            answer = cur.fetchall()
            print(answer)


        while flag == True:
            answer = input('Какое действие хотите выполнить? ')
            if answer == 'a':
                add_user()
            elif answer == 'p':
                add_phone()
            elif answer == 'dt':
                delete_tables()
            elif answer == 'c':
                create_tables()
            elif answer == 'dp':
                delete_phone()
            elif answer == 'du':
                delete_user()
            elif answer == 's':
                search_param = input('Введите 1 параметр поиска: name, surname, email или phone ')
                search(search_param)
            elif answer == 'u':
                update()
            elif answer == 'x':
                print('Всего доброго!')
                break
            elif answer == 'show':
                show_all()
            else:
                print('Такой команды нет')