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
                <div><strong>Comnpany name:</strong> ${msg['comnpany_name']}</div>
                <div><strong>Email adress:</strong> ${msg['email_adress']}</div>
                <div><strong>Event time:</strong> ${msg['event_time']}</div>
                <div><strong>Event type:</strong> ${msg['event_type']}</div>
                <div><strong>Temporary storage:</strong> ${msg['temporary_storage']}</div>
                <div><strong>Car number:</strong> ${msg['car_number']}</div>
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