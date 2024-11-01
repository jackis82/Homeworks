import json
import os.path

def check_opened():
    global opened
    global open_path
    global ph_list
    global max_fio_length

    if opened == 0:
        # fl_name = active_path
        # print(open_path)
        print('Открываем справочник...')
        new_name = input('Введите имя файла справочника (текущее имя: '+open_path+'): ')
        if new_name != '':
            if os.path.exists(new_name):
                open_path = new_name
                ph_list = read_contacts(open_path)
                max_fio_length = get_max_fio_length()
                opened = 1
            else:
                print('Файл отсутствует!')
                print_continue()
        else:
            if os.path.exists(open_path):
                ph_list = read_contacts(open_path)
                max_fio_length = get_max_fio_length()
                opened = 1
            else:
                print('Файл отсутствует!')
                print_continue()

    # print('Справочник открыт')

def print_continue():
    print('\n--- для продолжения нажмите Enter ---')
    input()
    print_menu(0)


# функция отображает меню
def print_menu(n: int, prev_n: int=0) -> int:
    global path
    global open_path
    global new_path
    global save_path

    global opened
    global ph_list
    global sel_contact
    global req_save

    if n == 0:
        print('\nМЕНЮ:')
        print('-------------------------------------------')
        print('1. Открыть справочник...')
        print('2. Показать все контакты...')
        print('3. Показать данные выбранного контакта...')
        print('4. Найти контакт...')
        print('5. Создать контакт...')
        print('6. Изменить контакт...')
        print('7. Удалить контакт...')
        print('8. Сохранить данные...')
        print('9. ВЫХОД')
        print('-------------------------------------------')
        print('')
        n = input('ВЫБЕРИТЕ ПУНКТ МЕНЮ: ')
        while not n.isdigit():
            n = input('ВЫБЕРИТЕ ПУНКТ МЕНЮ: ')
        n_menu = int(n)

    else:
        n_menu = int(n)

    # print('n_menu='+str(n_menu))
    # print(type(n_menu))
    # 1. Открыть справочник...
    if n_menu == 1:
        print('------ пункт 1 (Открыть справочник)')
        if opened:
            print('Справочник уже открыт ('+open_path+').')
            if input('Открыть его заново (для отмены - Enter)? '):
                opened = 0
                check_opened()
                is_changes = 0
                print('Справочник открыт (' + open_path + ')')
        else:
            check_opened()
            print('Справочник открыт ('+open_path+')')
        print_continue()

    # 2. Показать все контакты...
    if n_menu == 2:
        print('------ пункт 2 (Показать все контакты)')
        check_opened()
        print('перед выводом:')
        print_all_contacts(1, 1, 1)
        print_continue()


    # 3. Показать данные выбранного контакта...
    if n_menu == 3:
        print('------ пункт "Показать данные выбранного контакта"')
        check_opened()
        if need_select_contact()>0:
            print('Контакт:')
            print_contact(sel_contact, 1, 1, 1)
        else:
            print('Нет выбранного контакта!')
            print_menu(0)
        print_continue()


    # 4. Найти контакт...'
    if n_menu == 4:
        print('------ пункт "Найти контакт"')
        check_opened()
        print('ПОИСК КОНТАКТА:')
        str_to_find=input('Введите строку для поиска (для возврата - Enter): ')
        found_by_fio = []
        found_by_tel = []
        found_by_com = []

        if str_to_find:
            # функция ищет контакт по ФИО и
            # возвращает список из номеров элементов списка контактов (иначе [])
            found_by_fio=find_contact_fio(str_to_find)
            # print(found_by_fio)
            if found_by_fio != []:
                print('')
                print(f'Найдено контактов по ФИО: {len(found_by_fio)}')
                print('------------------------------------------------------')
                # input('')
                for f_item in found_by_fio:
                    # print(f'Найден контакт по ФИО: {f_item}')
                    sel_contact = select_contact(f_item)
                    print_contact(sel_contact,1,1,1)

            # функция ищет контакт по телефону и
            # возвращает список из номеров элементов списка контактов (иначе [])
            found_by_tel=find_contact_tel(str_to_find)
            # print(found_by_tel)
            # input('')
            if found_by_tel != []:
                print('')
                print(f'Найдено контактов по номеру телефона: {len(found_by_tel)}')
                print('------------------------------------------------------')
                for f_item in found_by_tel:
                    # print(f'Найден контакт по номеру телефона: {f_item}')
                    sel_contact = select_contact(f_item)
                    print_contact(sel_contact,1,1,1)

            # функция ищет контакт по названию компании и
            # возвращает список из номеров элементов списка контактов (иначе [])
            found_by_com=find_contact_com(str_to_find)
            # print(found_by_com)
            if found_by_com != []:
                print('')
                print(f'Найдено контактов по названию компании: {len(found_by_com)}')
                print('------------------------------------------------------')
                for f_item in found_by_com:
                    # print(f'Найден контакт по названию компании: {f_item}')
                    sel_contact = select_contact(f_item)
                    print_contact(sel_contact,1,1,1)


            if (found_by_fio == []) & (found_by_tel == []) & (found_by_com == []):
                print('')
                print(f'Контактов с "{str_to_find}" не найдено.')
        print_continue()


    # 5. Создать контакт...'
    if n_menu == 5:
        print('------ пункт "Создать контакт"')
        check_opened()
        print('СОЗДАНИЕ КОНТАКТА:')
        # функция добавляет контакт
        sel_contact = append_contact()
        if sel_contact != {}:
            print('Контакт  добавлен:')
            req_save = 1
            print_contact(sel_contact, 1, 1, 1)
        else:
            print('Контакт не добавлен:')
        print_continue()


    # 6. Изменить контакт...'
    if n_menu == 6:
        print('------ пункт "Изменить контакт"')
        check_opened()
        print('ИЗМЕНЕНИЕ КОНТАКТА:')

        if need_select_contact()>0:
            print('Контакт:')
            print_contact(sel_contact, 1, 1, 1)
            change_contact(sel_contact)
            req_save = 1
            print_contact(sel_contact, 1, 1, 1)
        else:
            print('Нет выбранного контакта!')
        print_continue()


    # 7. Удалить контакт...'
    if n_menu == 7:
        print('------ пункт "Удалить контакт"')
        check_opened()
        if need_select_contact()>0:
            print('Контакт:')
            print_contact(sel_contact, 1, 1, 1)

            if input(' - удалить данный контакт (для отмены - Enter): '):
                cont_num=sel_contact['номер']-1
                delete_contact(cont_num)
                req_save = 1
                print(' - контакт удалён\n')
        else:
            print('Нет выбранного контакта!')
        print_continue()


    # 8. Сохранить данные...
    if n_menu == 8:
        print('------ пункт "Сохранить данные"')
        if opened == 0:
            print('Прежде чем сохранять, нужно открыть справочник\n')
            res_inp = input('Открыть справочник? (для отмены Enter): ')
            if res_inp:
                check_opened()
        if opened == 1:
            save_contacts()
            req_save = 0
            if prev_n>0:
                print_continue()


    # 9. ВЫХОД...
    if n_menu == 9:
        print('------ пункт "Сохранить данные"')
        # запрос сохранения перед выходом
        if req_save == 1:
            res_inp = input('Сохранить данные в файл? (для отмены Enter): ')
            if res_inp:
                print_menu(8, 0)




# функция чтения из json-файла контактов в список
def read_contacts(a_fl_name: str) -> list:
    # открываем файл
    with open(a_fl_name, 'r', encoding='utf-8') as json_file:
        contacts_list = json.load(json_file)
        return contacts_list

# функция сохранения в json-файл контактов из списка
def save_contacts():
    global save_path
    global ph_list
    global max_fio_length

    print(save_path)
    new_name = input('Введите имя файла, куда сохранить (текущее имя: '+save_path+'): ')
    if new_name != '':
        save_path = new_name

    # подготавливаем данные для сохранения
    for a_dict in ph_list:
        a_dict.pop('номер')
        a_dict.pop('ФИО')

    # открываем файл
    with open(save_path, 'w', encoding='utf-8') as json_file:
        json.dump(ph_list, json_file, indent=4, ensure_ascii=0)  # ensure_ascii=0 - для записи кириллицы
        # for i in range(len(a_list)):
        #     el_dict = a_list[i]
        #     print(type(el_dict))
        #     print(el_dict)
        #     json.dump(el_dict, json_file, indent=4, ensure_ascii=0)
    print('Справочник сохранен в файл: '+save_path)

    # восстанавливаем данные для работы
    max_fio_length = get_max_fio_length()

# print(type(ph_list))       # тип словарь
# print(ph_list[0])
# print(type(ph_list[0]))       # тип словарь

# el_dict=ph_list[0]

# el_dict['ФИО']=el_dict.get('Фамилия','')+' '+el_dict.get('Имя','')+' '+el_dict.get('Отчество','')
# print(el_dict['ФИО'])



# функция определяет макс.длину ФИО контакта
def get_max_fio_length() -> int:
    global opened
    global ph_list
    global sel_contact

    max_fio_length=0
    # поиск max_fio_length (для дальнейшего выравнивания вывода списка)
    for i in range(len(ph_list)):
        el_dict=ph_list[i]
        el_dict['номер']=i+1
        el_dict['ФИО'] = el_dict.get('Фамилия', '') + ' ' + el_dict.get('Имя', '') + ' ' + el_dict.get('Отчество', '')
        if max_fio_length<len(el_dict['ФИО']):
            max_fio_length=len(el_dict['ФИО'])
        # ph_list[i]=el_dict
    return max_fio_length
    # print(f'max_fio_length={max_fio_length}')




# функция печатает информацию обо всех контактах
def print_all_contacts(print_num=1,print_fio=1,print_tel_com=0):
    global opened
    global ph_list
    global sel_contact

    for i in range(len(ph_list)):
        el_dict=ph_list[i]
        # el_dict['ФИО'] = el_dict.get('Фамилия', '') + ' ' + el_dict.get('Имя', '') + ' ' + el_dict.get('Отчество', '')
        # print(el_dict['ФИО'])

        fio=el_dict['ФИО']
        tel_com = el_dict['Телефон'] + ' (' + el_dict['Комментарий'] + ')'

        output_str = ''
        if print_num:
            output_str+=(i+1).__str__()+') '
        if print_fio:
            output_str+=fio
        if print_tel_com:
            str_spaces = ''
            if print_fio & print_tel_com:
                # определяем кол-во пробелов между ФИО и номером (для выравнивания)
                tt = max_fio_length - len(fio)
                # print(tt)
                for k in range(tt):
                    str_spaces += ' '

            output_str+=str_spaces+f'\t\t{tel_com}'
        print(output_str)


def select_contact(n: int):
    global ph_list
    return ph_list[n]



# функция печатает информацию о контакте
def print_contact(a_dict,print_num=1,print_fio=1,print_tel_com=0):
    global opened
    global ph_list
    global sel_contact

    fio = a_dict['ФИО']
    tel_com = a_dict['Телефон'] + ' (' + a_dict['Комментарий'] + ')'

    output_str = ''
    if print_num:
        output_str += str(a_dict['номер']) + ') '
    if print_fio:
        output_str += fio
    if print_tel_com:
        str_spaces = ''
        if print_fio & print_tel_com:
            # определяем кол-во пробелов между ФИО и номером (для выравнивания)
            tt = max_fio_length - len(fio)
            # print(tt)
            for k in range(tt):
                str_spaces += ' '

        output_str += str_spaces + f'\t\t{tel_com}'
    print(output_str)

# функция обновляет параметр контакта и
# возвращает 1, если значение изменилось (иначе 0)
def update_value(a_dict, var_cap, var_str):
    new_value = input(f"  {var_cap} (текущее значение: '{var_str}'). Введите новое значение (Enter - оставить текущее): ")
    if new_value:
        a_dict[var_cap]=new_value
        return 1
    else:
        return 0

# функция оставляет в строке только цифры (остальное удаляет)
def extract_digits(input_str) -> str:
    # result = ''.join(char for char in input_str if char.isdigit())
    res = ''
    for char in input_str:
        if char.isdigit():
            res +=char
    return res




# функция добавляет контакт
def append_contact() -> dict:
    global ph_list

    new_dict = {}
    print('Введите данные нового контакта:')
    new_f = input('Введите Фамилию: ')
    if new_f:
        new_i = input('Введите Имя: ')
        new_o = input('Введите Отчество: ')
        new_tel = input('Введите номер телефона: ')
        if new_tel:
            new_dict['Фамилия'] = new_f
            new_dict['Имя'] = new_i
            new_dict['Отчество'] = new_o
            new_dict['Телефон'] = new_tel

            new_com = ''
            new_com = input('Введите комментарий: ')
            new_dict['Комментарий'] = new_com
            # new_dict['Комментарий'] = new_com
            ph_list.append(new_dict)
            get_max_fio_length()
    return new_dict



# функция удаляет контакт с индексом n
def delete_contact(n: int):
    global ph_list
    global sel_contact

    el_dict = ph_list[n]
    fio = el_dict['ФИО']
    print(f'Вы уверены, что нужно удалить контакт {fio}?')
    if input('Нажмите "y", если нужно удалить...'):
        ph_list.pop(n)
        print(f'Контакт {fio} удалён')
        get_max_fio_length()
        sel_contact = {}

# функция изменяет контакт
def change_contact(a_dict) -> dict:
    t_f = update_value(a_dict,'Фамилия', a_dict['Фамилия'])
    t_i = update_value(a_dict,'Имя', a_dict['Имя'])
    t_o = update_value(a_dict,'Отчество', a_dict['Отчество'])
    a_dict['ФИО'] = a_dict.get('Фамилия', '') + ' ' + a_dict.get('Имя', '') + ' ' + a_dict.get('Отчество', '')
    # print(f't_f={t_f} t_i={t_i} t_o={t_o} ')
    t_t = update_value(a_dict,'Телефон', a_dict['Телефон'])
    t_k = update_value(a_dict,'Комментарий', a_dict['Комментарий'])
    return a_dict





# функция ищет контакт по ФИО и
# возвращает номер элемента в списке (иначе -1)
def find_contact_fio(fio_to_find: str) -> list:
    global ph_list

    # print('Ищем по ФИО: (' + fio_to_find + ')...')
    res = []
    for i in range(len(ph_list)):
        el_dict=ph_list[i]
        el_dict['ФИО']=el_dict.get('Фамилия', '') + ' ' + el_dict.get('Имя', '') + ' ' + el_dict.get('Отчество', '')
        # print(el_dict['ФИО'])
        fio_lower=el_dict['ФИО'].lower()
        fio_to_find_lower=fio_to_find.lower()
        # print(f'fio_lower={fio_lower}  fio_to_find_lower={fio_to_find_lower}')
        if fio_lower.find(fio_to_find_lower)>-1:
            res.append(i)
    return res
        # return None

# функция ищет контакт по телефону и
# возвращает номер элемента в списке (иначе -1)
def find_contact_tel(tel_to_find: str) -> list:
    global ph_list

    # print('Ищем по номеру телефона (' + tel_to_find + ')...')
    res = []
    dig_to_find = extract_digits(tel_to_find)
    if dig_to_find == '':
        return res
    for i in range(len(ph_list)):
        el_dict=ph_list[i]
        tel_digits=extract_digits(el_dict['Телефон'])
        if tel_digits.find(dig_to_find)>-1:
            res.append(i)
    return res


# функция ищет контакт по комментарию и
# возвращает номер элемента в списке (иначе -1)
def find_contact_com(com_to_find: str) -> list:
    global ph_list

    # print('\nИщем ' + com_to_find + '...')
    res = []
    for i in range(len(ph_list)):
        el_dict=ph_list[i]
        com_lower=el_dict['Комментарий'].lower()
        com_to_find_lower=com_to_find.lower()
        # print(f'fio_lower={fio_lower}  fio_to_find_lower={fio_to_find_lower}')
        if com_lower.find(com_to_find_lower)>-1:
            res.append(i)
    return res


# функция запроса и выбора контакта по индексу...
def need_select_contact() -> int:
    global sel_contact
    p = 0
    if sel_contact != {}:
        p = int(sel_contact['номер'])

    p = input(f'Введите порядковый номер контакта (текущий номер {p}) '
              '(для возврата нажмите Enter): ')
    if p>'':
        if p.isdigit():
            p = int(p)
        else:
            p = 0
            print('Некорректный номер!')
            return 0
    else:
        p = 0
        print('Некорректный номер!')
        return 0

    if (p>0) & (p<=len(ph_list)):
        sel_contact = select_contact(p-1)
        return p
            # print('Выбран контакт:')
            # print_contact(sel_contact, 1, 1, 1)
    else:
        print('Порядковый номер за пределами справочника!')
        return 0




dflt_open_path='phonedir.json'      # путь к файлу справочника (по умолчанию) для открытия
open_path = dflt_open_path          # путь к файлу справочника (заданный) для открытия

dflt_save_path='phonedir_2.json'    # путь к файлу справочника (по умолчанию) для сохранению
save_path = dflt_save_path          # путь к файлу справочника (заданный) для сохранению

opened = 0                          # признак того, что файл открыт
ph_list=[]                          # инициализируем список контактов
sel_contact={}                      # инициализируем выбранный контакт
req_save = 0                        # признак "требуется запрос сохранения"

print('-------- Телефонный справочник, версия 1.0 --------')
print_menu(0)


