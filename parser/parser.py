import base64
import quopri
import json

def parse(file_path, email, date, event_status, indicator_letter, indicator_email, indicator_svh, indicator_car, indicator_time, indicator_receiver, indicator_status):

    emails = {'no-reply@alfa-trans-smolensk.ru':'1', 'auto@ost-term.ru':'2', 'info1@severtrans.ru':'3'}

    with open(file_path, 'r', encoding='cp1251') as fh:
        text = fh.read()

    data_json = []

    texts = text.split('''------=_=-_OpenGroupware_org_NGMime-1172-1669453285.811666-7------
Content-Type: message/rfc822''')
    for text in texts[1:]:
        save = False
        # letter = text.split('\n')
        letter = text
        # for line in letter:
        #     if len(line) == 0:
        #         letter.remove(line)
        if indicator_email.count('ХХХ') == 1:
            for_split = indicator_email.split('ХХХ')
            # email_adress = emails[letter[letter.index(for_split[0])+len(for_split[0]):letter.index(for_split[1])]]
            email_adress = letter[letter.index(for_split[0])+len(for_split[0]):]
            email_adress = email_adress[:email_adress.index(for_split[1])]
            email_num = emails[email_adress]
        if email == email_num:
            save = True
            if email_num == '2':
                if 'Message-Id: <' in letter:
                    # data = ''.join(letter[letter.index(letter)+1:])
                    data = letter.split('Message-Id: <')[1].split('>')[1].replace('\n','')
                    letter = base64.b64decode(data).decode("utf-8")
            elif email_num == '3':
                if '<html>' in letter:
                    # data = ''.join(letter[letter.index(letter):letter.index('</html>')])
                    data = letter.split('<html>')[1].split('</html>')[0].replace('\n','')
                    letter = quopri.decodestring(data).decode('Windows-1251')
            if indicator_letter not in ''.join(letter):
                save = False
                continue
            if indicator_status.count('ХХХ') == 1:
                for_split = indicator_status.split('ХХХ')
                if for_split[0] != '' and for_split[1] != '':
                    event_type = letter[letter.index(for_split[0])+len(for_split[0]):letter.index(for_split[1])]
                elif for_split[0] == '' and for_split[1] != '':
                    if indicator_letter not in ''.join(letter):
                        save = False
                        continue
                    if email_adress=='3':
                        for_split[1] = for_split[1].replace(' ', '<br>')
                    event_type = letter[:letter.index(for_split[1])]
                    # for_split[1] = for_split[1].replace(' ', '<br>')
                    event_type = event_type[event_type.rindex(' '):].replace(' ', '')
                    if '\n' in event_type:
                        event_type = event_type[event_type.rindex('\n')+len('\n'):].replace(' ', '') 
                print('TIR<br>из ЗТК' in letter)                       
                if 'TIR<br>из ЗТК' in letter or ((event_type == 'Выезд' or event_type == 'из') and event_status == '2'):
                    event_type = 'убытие'
                elif (event_type == 'Въезд' or event_type == 'прибыл'  or event_type == 'Прибытие' or event_type == 'на')and event_status == '1' and 'TIR<br>из ЗТК' not in letter:
                    event_type = 'прибытие'
                else:
                    save = False
                    continue
            if indicator_time.count('ХХХ') == 1:
                for_split = indicator_time.split('ХХХ')
                if for_split[0] != '' and for_split[1] != '':
                    event_time = letter[letter.index(for_split[0])+len(for_split[0]):letter.index(for_split[1])]
                elif for_split[0] == '' and for_split[1] != '':
                    event_time = letter[letter.split(for_split[1])[0].rindex(' '):letter.index(for_split[1])]
                    if '\n' in event_time:
                        event_time = event_time[event_time.rindex('\n')+len('\n'):]
            elif indicator_time.count('ХХХ') == 2:
                for_split = indicator_time.split('ХХХ')
                if for_split[0] != '' and for_split[2] != '':
                    ind_fst=letter.rfind(for_split[0],0, letter.rindex(for_split[2]))
                    part_1 = letter[ind_fst+len(for_split[0]):letter.find(for_split[1], ind_fst+len(for_split[0]))]
                    part_2 = letter[letter.find(for_split[1], ind_fst+len(for_split[0]))+len(for_split[1]):letter.find(for_split[2],ind_fst)]
                    event_time = part_1 + ' ' + part_2
                elif for_split[0] != '' and for_split[2] == '':
                    event_time = letter[letter.index(for_split[0])+len(for_split[0]):]
                    if '\n' in event_time:
                        end = event_time.index('\n')
                        event_time=event_time[:end]
                if event_time[:10] != date:
                    save = False
                    continue
            if indicator_car.count('ХХХ') == 1:
                for_split = indicator_car.split('ХХХ')
                if for_split[0] != '' and for_split[1] == '':
                    car_number = letter[letter.index(for_split[0])+len(for_split[0]):]
                elif for_split[0] == '' and for_split[1] != '':
                    car_number = letter[letter.index(for_split[0])+len(for_split[1]):letter.index(for_split[1])]
            elif indicator_car.count('ХХХ') == 2:
                for_split = indicator_car.split('ХХХ')
                car_number = letter[letter.index(for_split[0])+len(for_split[0]):letter.find(for_split[2],letter.index(for_split[0]))]
                car_number = car_number.split('=')
                car_number = ''.join(car_number)
            if '\n' in car_number:
                end = car_number.index('\n')
                car_number=car_number[:end]
            car_number=car_number.replace('\r','')
            car_number=car_number.replace(' ','')
            if indicator_svh.count('ХХХ') == 1:
                for_split = indicator_svh.split('ХХХ')
                if for_split[0] != '' and for_split[1] == '':
                    temporary_storage = letter[letter.index(for_split[0])+len(for_split[0]):]
                elif for_split[0] == '' and for_split[1] != '':
                    temporary_storage = letter[letter.index(for_split[0])+len(for_split[1]):letter.index(for_split[1])]
                if '\n' in temporary_storage:
                    end = temporary_storage.index('\n')
                    temporary_storage=temporary_storage[:end]
                if '.' in temporary_storage:
                    end = temporary_storage.index('.')
                    temporary_storage=temporary_storage[:end]
                else:
                    end = temporary_storage.index(' ')
                    temporary_storage=temporary_storage[:end]
                
                temporary_storage=temporary_storage.replace('\r','')
                temporary_storage=temporary_storage.replace('"','')
            if indicator_svh == 'отсутсвует':
                temporary_storage = indicator_svh
            if indicator_receiver.count('ХХХ') == 1:
                for_split = indicator_receiver.split('ХХХ')
                if for_split[0] != '' and for_split[1] == '':
                    if email_adress =='3':
                        for_split[1]='</b>'
                        start = letter.rfind('>',letter.index(for_split[0].replace(' ','')), letter.find(for_split[1],letter.index(for_split[0].replace(' ',''))))
                        company_name = letter[start+1:letter.find(for_split[1],start)]
                    else:
                        company_name = letter[letter.index(for_split[0])+len(for_split[0]):]
                if '\n' in company_name:
                    end = company_name.index('\n')
                    company_name=company_name[:end]
                if '"' in company_name:
                    end = company_name.rindex('"')
                    company_name=company_name[:end+1]
                company_name = company_name.replace('\r','')
        if save:
            data_json.append({
                'email_adress': email_adress, 
                'car_number': car_number, 
                'temporary_storage': temporary_storage, 
                "event_type": event_type, 
                'event_time': event_time, 
                'company_name': company_name})

    file_name = f'eml/{date}.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data_json, file, indent=4, ensure_ascii=False)
        return file_name