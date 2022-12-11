"use strict";

var get_data = function() {
    $.ajax({
        url: '/get_data',
        type: 'POST',
        dataType : 'json',
        data: {
            sender:     get('#sender-select').value,
            event_type: get('#event-type-select').value,
            date:       get('#date-input').value,
            ident_1:    get('#ident-1 input[name="ident-1"]').value,
            ident_2:    get('#ident-2 input[name="ident-2"]').value,
            ident_3:    get('#ident-3 input[name="ident-3"]').value,
            ident_4:    get('#ident-4 input[name="ident-4"]').value,
            ident_5:    get('#ident-5 input[name="ident-5"]').value,
            ident_6:    get('#ident-6 input[name="ident-6"]').value,
            ident_7:    get('#ident-7 input[name="ident-7"]').value
        },
        success: function (data) {
            show_data(data);
        },
        error: function(jqxhr, status, errorMsg) {
            alert('Server error!');
        }
    });
}

var show_data = function(data) {
    let result = get('.search-result');

    result.innerHTML = `
        <div class='caption'>
            <h2>Результаты поиска</h2>
            <a class='btn' href="/eml/data.json" download>Скачать JSON</a>
        </div>
		<div class='messages'>
            <div class='message bold'>
                <div>Название компании</div>
                <div>Тип события</div>
                <div>Дата и время</div>
            </div>
        </div>
    `

    let result_msg = get('.messages');

    let id = 0;
    Array.from(data).forEach(msg => {
        result_msg.innerHTML += `
            <div class='message' onclick='open_msg("#msg-desc-${id}")'>
                <div>${msg['comnpany_name']}</div>
                <div>${msg['event_type']}</div>
                <div>${msg['event_time']}</div>
            </div>
            <div class='msg-desc' id='msg-desc-${id}'>
                <div><strong>Название компании:</strong> ${msg['comnpany_name']}</div>
                <div><strong>Email:</strong> ${msg['email_adress']}</div>
                <div><strong>Дата и время прибытия:</strong> ${msg['event_time']}</div>
                <div><strong>Тип события:</strong> ${msg['event_type']}</div>
                <div><strong>Склад временного хранения:</strong> ${msg['temporary_storage']}</div>
                <div><strong>Номер транспортного средства:</strong> ${msg['car_number']}</div>
            </div>
        `
        id++;
    });
}

var open_msg = function(id) {
    let block = get(id);
    if (block.style.display == 'none') {
        block.style.display = 'flex';
    } else {
        block.style.display = 'none';
    }
}