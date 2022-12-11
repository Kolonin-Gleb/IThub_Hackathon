import base64
import quopri
import json

def parse(file_path, email, date, event_status):

    emails = {'no-reply@alfa-trans-smolensk.ru':'1', 'auto@ost-term.ru':'2', 'info1@severtrans.ru':'3'}

    with open(file_path, 'r', encoding='cp1251') as fh:
        with open('file.txt', 'w') as f:
            f.write(fh.read())

    with open('file.txt', 'r') as f:
        text = f.read()

    data_json = []

    texts = text.split('''------=_=-_OpenGroupware_org_NGMime-1172-1669453285.811666-7------
Content-Type: message/rfc822''')
    for text in texts[1:]:
        save = False
        letter = text.split('\n')
        for line in letter:
            if len(line) == 0:
                letter.remove(line)
        print()
        for line in letter:
            if 'Return-Path: <' in line:
                email_adress = line.split('Return-Path: <')[1].strip()[:-1]
        if email_adress == 'no-reply@alfa-trans-smolensk.ru' and email == emails[email_adress]:
            email_adress = '1'
            save = True
            for line in letter:
                if 'Выезд :' in line:
                    event_type = '2'
                    event_time = line.split('Выезд :')[1].strip()
                    enternal_date = event_time.split(' ')[0]
                    if date != enternal_date or event_status != event_type:
                        save = False
                        break
                if 'Въезд :' in line:
                    event_type = '1'
                    event_time = line.split('Въезд :')[1].strip()
                    enternal_date = event_time.split(' ')[0]
                    if date != enternal_date or event_status != event_type:
                        save = False
                        break
                if 'А/м' in line and ':' in line:
                    car_number = line.split(':')[1].strip()
                if 'СВХ' in line:
                    temporary_storage = line.split('"')[1]
                if 'Получатель:' in line:
                    comnpany_name = line.split('Получатель:')[1].strip()
        elif email_adress == 'auto@ost-term.ru' and email == emails[email_adress]:
            email_adress = '2'
            save = True
            for line in letter:
                if 'Message-Id: <' in line:
                    data = ''.join(letter[letter.index(line)+1:])
                    massage = base64.b64decode(data).decode("utf-8")
                    temporary_storage = 'absent'
                    if 'автомобиль №' in massage and ':' in line:
                        car_number = massage.split('автомобиль № ')[1].split(' ')[0].strip()
                    if 'прибыл' in massage:
                        event_type = '1'
                        event_time = massage.split('прибыл')[0].split(' в ')[2].strip()
                        enternal_date = event_time.split(' ')[0]
                        if date != enternal_date or event_status != event_type:
                            save = False
                            break
                    if 'в адрес фирмы' in massage:
                        comnpany_name = massage.split('в адрес фирмы')[1].split(' в ')[0].strip()
        elif email_adress == 'info1@severtrans.ru' and email == emails[email_adress]:
            email_adress = '3'
            save = True
            for line in letter:
                if '<html>' in line:
                    data = ''.join(letter[letter.index(line):letter.index('</html>')])
                    massage = quopri.decodestring(data).decode('Windows-1251')
                    # print(massage)
                    temporary_storage = 'absent'
                    if 'amRegNumb' in massage:
                        car_number = massage.split('amRegNumb">')[1].split('</b>')[0].strip().replace('=', '')
                    if 'Выдача<br>груза<br>клиенту' in massage:
                        event_type = '1'
                        event_time = massage.split('CarArrival=">')[1].split('</small>')[0].strip().replace('<br>', ' ')
                        enternal_date = event_time.split(' ')[0]
                        if date != enternal_date or event_status != event_type:
                            save = False
                            break
                    if 'Выезд<br>TIR<br>из ЗТК' in massage:
                        event_type = '2'
                        event_time = massage.split('CagroIssue=">')[1].split('</small>')[0].strip().replace('<br>', ' ')
                        enternal_date = event_time.split(' ')[0]
                        if date != enternal_date or event_status != event_type:
                            save = False
                            break
                    if 'pol_id' in massage:
                        comnpany_name = massage.split('pol_id">')[1].split('<')[0].strip()
        if save:
            data_json.append({
                'email_adress': email_adress, 
                'car_number': car_number, 
                'temporary_storage': temporary_storage, 
                "event_type": event_type, 
                'event_time': event_time, 
                'comnpany_name': comnpany_name})

        file_name = f'{date}.json'
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data_json, file, indent=4, ensure_ascii=False)