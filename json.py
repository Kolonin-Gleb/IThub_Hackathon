# Номер транспортного средства №....(номер);
# Склад временного хранения ...(название);
# Вермя и дата прибытия ....(дата и время);         / убытия
# Название получателя товаров (название компании)

# event_time = datetime(year=1992, month=10, day= 6, hour=9, minute=40, second=23) # JSON не поддерживает datetime

import json


while True: # Пока есть письма в файле .eml
    # Пока идёт обработка текущего письма

    # Взять от Софии собранные значения в переменные
    car_number = "number"
    temporary_storage = "temporary_storage"
    event_type = "departure/arrival"
    event_time = "1992-10-06 09:40:23"
    comnpany_name = "company_name"
    data = {'car_number': car_number, 'temporary_storage': temporary_storage, "event_type": event_type, 'event_time': event_time, 'comnpany_name': comnpany_name}

    file_name = f'{event_time}.json'.replace(':', '-')
    with open(file_name, 'w') as file:
        json.dump(data, file)
    break
