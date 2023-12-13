
TEMPLATE__ASSIGNED_TO_TICKET = {
    "subject": "Призначення відповідального за тікет #{ticket_id}",
    "content": """
Шановна адміністраціє,

Хочемо повідомити, що Ви були призначені відповідальним на платформі TreS.

Інформація про тікет:
Номер тікета: #{ticket_id}
Тема: {ticket_subject}

З найкращими побажаннями,
Команда TreS
"""
}

TEMPLATE__UNASSIGNED_TO_TICKET = {
    "subject": "Зняття з відповідальності за тікет #{ticket_id}",
    "content": """
Шановна адміністраціє,

Бажаємо повідомити, що з моменту цього листа відповідальність за тікет із номером #{ticket_id} на платформі TreS тепер покладена на іншого представника команди.

Інформація про тікет:
Номер тікета: #{ticket_id}
Тема: {ticket_subject}

З найкращими побажаннями,
Команда TreS
"""
}

TEMPLATE__EMAIL_NOTIFICATION = {
    "subject": "TreS #{ticket_id} \"{ticket_subject}\"",
    "content": """
Шановн(-ий/-а) користувач(-ко),

Ми хочемо Вас проінформувати, що були внесені важливі зміни до тікетів на платформі TreS. Нижче наведено деталізація цих змін:

{data}

Дякуємо за увагу!
"""
}

TEMPLATE__EMAIL_NOTIFICATION_FOR_ADMIN = {
    "subject": "Тікети в статусі NEW вже {days_count} дні",
    "content": """
Шановна адміністраціє,

Цим повідомленням нагадуємо, що наступні тікети перебувають в статусі "NEW" протягом останніх {days_count} днів:

{data}

Будь ласка, призначте відповідного співробітника для обробки цих тікетів негайно.

Дякуємо за увагу!
"""
}

TEMPLATE__ACCESS_RENEW_REQUEST_EMAIL = {
    "subject": "Запит на поновлення доступу до TreS",
    "content": """
Шановний(а) користувач(ка),

Якщо ви отримали це повідомлення, це свідчить про те, що ви виразили бажання відновити доступ до свого облікового запису.

Для відновлення доступу, будь ласка, скористайтеся наступним посиланням: {url}.

Майте на увазі, що це посилання буде активним лише протягом обмеженого періоду часу. Таким чином, рекомендуємо вам виконати процедуру відновлення якнайшвидше.

Якщо ви не здійснювали жодних змін у своєму обліковому записі, і це повідомлення вас здивувало, будь ласка, зверніться до нашої служби підтримки через платформу TreS.

Дякуємо за ваше розуміння та співпрацю.
"""
}
