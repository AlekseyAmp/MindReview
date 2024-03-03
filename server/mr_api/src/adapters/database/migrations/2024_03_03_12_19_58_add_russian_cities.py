"""add russian cities

Revision ID: d8501a2c6962
Revises: fde1cbcd48cf
Create Date: 2024-03-03 12:19:58.740918+00:00

"""
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import insert as psql_insert

# revision identifiers, used by Alembic.
revision: str = 'd8501a2c6962'
down_revision: Union[str, None] = 'fde1cbcd48cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


cities: list[dict] = [
    {
        "raw_name": "алушта",
        "original_name": "Алушта"
    },
    {
        "raw_name": "феодосия",
        "original_name": "Феодосия"
    },
    {
        "raw_name": "ялта",
        "original_name": "Ялта"
    },
    {
        "raw_name": "севастополь",
        "original_name": "Севастополь"
    },
    {
        "raw_name": "симферополь",
        "original_name": "Симферополь"
    },
    {
        "raw_name": "абакан",
        "original_name": "Абакан"
    },
    {
        "raw_name": "адлер",
        "original_name": "Адлер"
    },
    {
        "raw_name": "анапа",
        "original_name": "Анапа"
    },
    {
        "raw_name": "ангарск",
        "original_name": "Ангарск"
    },
    {
        "raw_name": "архангельск",
        "original_name": "Архангельск"
    },
    {
        "raw_name": "астрахань",
        "original_name": "Астрахань"
    },
    {
        "raw_name": "барнаул",
        "original_name": "Барнаул"
    },
    {
        "raw_name": "белгород",
        "original_name": "Белгород"
    },
    {
        "raw_name": "благовещенск",
        "original_name": "Благовещенск"
    },
    {
        "raw_name": "чебоксары",
        "original_name": "Чебоксары"
    },
    {
        "raw_name": "челябинск",
        "original_name": "Челябинск"
    },
    {
        "raw_name": "члб",
        "original_name": "Челябинск"
    },
    {
        "raw_name": "челяб",
        "original_name": "Челябинск"
    },
    {
        "raw_name": "череповец",
        "original_name": "Череповец"
    },
    {
        "raw_name": "черняховск",
        "original_name": "Черняховск"
    },
    {
        "raw_name": "чита",
        "original_name": "Чита"
    },
    {
        "raw_name": "екатеринбург",
        "original_name": "Екатеринбург"
    },
    {
        "raw_name": "екб",
        "original_name": "Екатеринбург"
    },
    {
        "raw_name": "геленджик",
        "original_name": "Геленджик"
    },
    {
        "raw_name": "иркутск",
        "original_name": "Иркутск"
    },
    {
        "raw_name": "ижевск",
        "original_name": "Ижевск"
    },
    {
        "raw_name": "кабардинка",
        "original_name": "Кабардинка"
    },
    {
        "raw_name": "калининград",
        "original_name": "Калининград"
    },
    {
        "raw_name": "казань",
        "original_name": "Казань"
    },
    {
        "raw_name": "кемерово",
        "original_name": "Кемерово"
    },
    {
        "raw_name": "хабаровск",
        "original_name": "Хабаровск"
    },
    {
        "raw_name": "хантымансийск",
        "original_name": "Ханты-Мансийск"
    },
    {
        "raw_name": "кисловодск",
        "original_name": "Кисловодск"
    },
    {
        "raw_name": "комсомольскнаамуре",
        "original_name": "Комсомольск-на-Амуре"
    },
    {
        "raw_name": "кострома",
        "original_name": "Кострома"
    },
    {
        "raw_name": "краснодар",
        "original_name": "Краснодар"
    },
    {
        "raw_name": "красноярск",
        "original_name": "Красноярск"
    },
    {
        "raw_name": "курган",
        "original_name": "Курган"
    },
    {
        "raw_name": "курск",
        "original_name": "Курск"
    },
    {
        "raw_name": "липецк",
        "original_name": "Липецк"
    },
    {
        "raw_name": "листвянка",
        "original_name": "Листвянка"
    },
    {
        "raw_name": "магадан",
        "original_name": "Магадан"
    },
    {
        "raw_name": "магнитогорск",
        "original_name": "Магнитогорск"
    },
    {
        "raw_name": "махачкала",
        "original_name": "Махачкала"
    },
    {
        "raw_name": "минеральныеводы",
        "original_name": "Минеральные Воды"
    },
    {
        "raw_name": "москва",
        "original_name": "Москва"
    },
    {
        "raw_name": "мск",
        "original_name": "Москва"
    },
    {
        "raw_name": "мурманск",
        "original_name": "Мурманск"
    },
    {
        "raw_name": "находка",
        "original_name": "Находка"
    },
    {
        "raw_name": "нальчик",
        "original_name": "Нальчик"
    },
    {
        "raw_name": "нижневартовск",
        "original_name": "Нижневартовск"
    },
    {
        "raw_name": "нижнийновгород",
        "original_name": "Нижний Новгород"
    },
    {
        "raw_name": "ноябрьск",
        "original_name": "Ноябрьск"
    },
    {
        "raw_name": "норильск",
        "original_name": "Норильск"
    },
    {
        "raw_name": "новокузнецк",
        "original_name": "Новокузнецк"
    },
    {
        "raw_name": "новороссийск",
        "original_name": "Новороссийск"
    },
    {
        "raw_name": "новосибирск",
        "original_name": "Новосибирск"
    },
    {
        "raw_name": "новыйуренгой",
        "original_name": "Новый Уренгой"
    },
    {
        "raw_name": "омск",
        "original_name": "Омск"
    },
    {
        "raw_name": "оренбург",
        "original_name": "Оренбург"
    },
    {
        "raw_name": "пенза",
        "original_name": "Пенза"
    },
    {
        "raw_name": "пермь",
        "original_name": "Пермь"
    },
    {
        "raw_name": "петропавловсккамчатский",
        "original_name": "Петропавловск-Камчатский"
    },
    {
        "raw_name": "петрозаводск",
        "original_name": "Петрозаводск"
    },
    {
        "raw_name": "псков",
        "original_name": "Псков"
    },
    {
        "raw_name": "пятигорск",
        "original_name": "Пятигорск"
    },
    {
        "raw_name": "ростовнадону",
        "original_name": "Ростов-на-Дону"
    },
    {
        "raw_name": "рязань",
        "original_name": "Рязань"
    },
    {
        "raw_name": "салехард",
        "original_name": "Салехард"
    },
    {
        "raw_name": "самара",
        "original_name": "Самара"
    },
    {
        "raw_name": "саранск",
        "original_name": "Саранск"
    },
    {
        "raw_name": "саратов",
        "original_name": "Саратов"
    },
    {
        "raw_name": "саяногорск",
        "original_name": "Саяногорск"
    },
    {
        "raw_name": "сочи",
        "original_name": "Сочи"
    },
    {
        "raw_name": "санктпетербург",
        "original_name": "Санкт-Петербург"
    },
    {
        "raw_name": "питер",
        "original_name": "Санкт-Петербург"
    },
    {
        "raw_name": "спб",
        "original_name": "Санкт-Петербург"
    },
    {
        "raw_name": "петербург",
        "original_name": "Санкт-Петербург"
    },
    {
        "raw_name": "ставрополь",
        "original_name": "Ставрополь"
    },
    {
        "raw_name": "сургут",
        "original_name": "Сургут"
    },
    {
        "raw_name": "суздаль",
        "original_name": "Суздаль"
    },
    {
        "raw_name": "светлогорск",
        "original_name": "Светлогорск"
    },
    {
        "raw_name": "сыктывкар",
        "original_name": "Сыктывкар"
    },
    {
        "raw_name": "таганрог",
        "original_name": "Таганрог"
    },
    {
        "raw_name": "тольятти",
        "original_name": "Тольятти"
    },
    {
        "raw_name": "томск",
        "original_name": "Томск"
    },
    {
        "raw_name": "тула",
        "original_name": "Тула"
    },
    {
        "raw_name": "тверь",
        "original_name": "Тверь"
    },
    {
        "raw_name": "тюмень",
        "original_name": "Тюмень"
    },
    {
        "raw_name": "уфа",
        "original_name": "Уфа"
    },
    {
        "raw_name": "углич",
        "original_name": "Углич"
    },
    {
        "raw_name": "ухта",
        "original_name": "Ухта"
    },
    {
        "raw_name": "уланудэ",
        "original_name": "Улан-Удэ"
    },
    {
        "raw_name": "ульяновск",
        "original_name": "Ульяновск"
    },
    {
        "raw_name": "великийновгород",
        "original_name": "Великий Новгород"
    },
    {
        "raw_name": "владикавказ",
        "original_name": "Владикавказ"
    },
    {
        "raw_name": "владимир",
        "original_name": "Владимир"
    },
    {
        "raw_name": "владивосток",
        "original_name": "Владивосток"
    },
    {
        "raw_name": "волгоград",
        "original_name": "Волгоград"
    },
    {
        "raw_name": "воркута",
        "original_name": "Воркута"
    },
    {
        "raw_name": "воронеж",
        "original_name": "Воронеж"
    },
    {
        "raw_name": "выборг",
        "original_name": "Выборг"
    },
    {
        "raw_name": "якутск",
        "original_name": "Якутск"
    },
    {
        "raw_name": "ярославль",
        "original_name": "Ярославль"
    },
    {
        "raw_name": "йошкарола",
        "original_name": "Йошкар-Ола"
    },
    {
        "raw_name": "южносахалинск",
        "original_name": "Южно-Сахалинск"
    },
    {
        "raw_name": "химки",
        "original_name": "Химки"
    },
    {
        "raw_name": "калуга",
        "original_name": "Калуга"
    },
    {
        "raw_name": "елабуга",
        "original_name": "Елабуга"
    },
    {
        "raw_name": "азов",
        "original_name": "Азов"
    },
    {
        "raw_name": "александров",
        "original_name": "Александров"
    },
    {
        "raw_name": "брянск",
        "original_name": "Брянск"
    },
    {
        "raw_name": "вологда",
        "original_name": "Вологда"
    },
    {
        "raw_name": "выкса",
        "original_name": "Выкса"
    },
    {
        "raw_name": "грозный",
        "original_name": "Грозный"
    },
    {
        "raw_name": "иваново",
        "original_name": "Иваново"
    },
    {
        "raw_name": "киров",
        "original_name": "Киров"
    },
    {
        "raw_name": "муром",
        "original_name": "Муром"
    },
    {
        "raw_name": "набережныечелны",
        "original_name": "Набережные Челны"
    },
    {
        "raw_name": "челны",
        "original_name": "Набережные Челны"
    },
    {
        "raw_name": "нижнекамск",
        "original_name": "Нижнекамск"
    },
    {
        "raw_name": "переславльзалесский",
        "original_name": "Переславль-Залесский"
    },
    {
        "raw_name": "ростоввеликий",
        "original_name": "Ростов Великий"
    },
    {
        "raw_name": "сергиевпосад",
        "original_name": "Сергиев Посад"
    },
    {
        "raw_name": "смоленск",
        "original_name": "Смоленск"
    },
    {
        "raw_name": "стараярусса",
        "original_name": "Старая Русса"
    },
    {
        "raw_name": "тамбов",
        "original_name": "Тамбов"
    },
    {
        "raw_name": "тобольск",
        "original_name": "Тобольск"
    },
    {
        "raw_name": "шахты",
        "original_name": "Шахты"
    },
    {
        "raw_name": "стрельна",
        "original_name": "Стрельна"
    },
    {
        "raw_name": "петергоф",
        "original_name": "Петергоф"
    },
    {
        "raw_name": "пушкин",
        "original_name": "Пушкин"
    },
    {
        "raw_name": "обнинск",
        "original_name": "Обнинск"
    },
    {
        "raw_name": "армавир",
        "original_name": "Армавир"
    },
    {
        "raw_name": "гатчина",
        "original_name": "Гатчина"
    },
    {
        "raw_name": "зеленогорск",
        "original_name": "Зеленогорск"
    },
    {
        "raw_name": "репино",
        "original_name": "Репино"
    },
    {
        "raw_name": "солнечное",
        "original_name": "Солнечное"
    },
    {
        "raw_name": "шлиссельбург",
        "original_name": "Шлиссельбург"
    },
    {
        "raw_name": "воскресенское",
        "original_name": "Воскресенское"
    },
    {
        "raw_name": "коломна",
        "original_name": "Коломна"
    },
    {
        "raw_name": "рождествено",
        "original_name": "Рождествено"
    },
    {
        "raw_name": "октябрьский",
        "original_name": "Октябрьский"
    },
    {
        "raw_name": "всеволожск",
        "original_name": "Всеволожск"
    },
    {
        "raw_name": "бузулук",
        "original_name": "Бузулук"
    },
    {
        "raw_name": "ессентуки",
        "original_name": "Ессентуки"
    },
    {
        "raw_name": "кировск",
        "original_name": "Кировск"
    },
    {
        "raw_name": "новокуйбышевск",
        "original_name": "Новокуйбышевск"
    },
    {
        "raw_name": "приозерск",
        "original_name": "Приозерск"
    },
    {
        "raw_name": "рыбинск",
        "original_name": "Рыбинск"
    },
    {
        "raw_name": "серпухов",
        "original_name": "Серпухов"
    },
    {
        "raw_name": "стерлитамак",
        "original_name": "Стерлитамак"
    },
    {
        "raw_name": "ступино",
        "original_name": "Ступино"
    },
    {
        "raw_name": "туапсе",
        "original_name": "Туапсе"
    },
    {
        "raw_name": "чайковский",
        "original_name": "Чайковский"
    },
    {
        "raw_name": "энгельс",
        "original_name": "Энгельс"
    },
    {
        "raw_name": "шуя",
        "original_name": "Шуя"
    },
    {
        "raw_name": "сорочинск",
        "original_name": "Сорочинск"
    },
    {
        "raw_name": "терскол",
        "original_name": "Терскол"
    },
    {
        "raw_name": "кропоткин",
        "original_name": "Кропоткин"
    },
    {
        "raw_name": "дзержинск",
        "original_name": "Дзержинск"
    },
    {
        "raw_name": "тихвин",
        "original_name": "Тихвин"
    },
    {
        "raw_name": "шатура",
        "original_name": "Шатура"
    },
    {
        "raw_name": "златоуст",
        "original_name": "Златоуст"
    },
    {
        "raw_name": "горноалтайск",
        "original_name": "Горно-Алтайск"
    },
    {
        "raw_name": "великиелуки",
        "original_name": "Великие Луки"
    },
    {
        "raw_name": "биробиджан",
        "original_name": "Биробиджан"
    },
    {
        "raw_name": "волгодонск",
        "original_name": "Волгодонск"
    },
    {
        "raw_name": "волжский",
        "original_name": "Волжский"
    },
    {
        "raw_name": "ейск",
        "original_name": "Ейск"
    },
    {
        "raw_name": "белокуриха",
        "original_name": "Белокуриха"
    },
    {
        "raw_name": "кировочепецк",
        "original_name": "Кирово-Чепецк"
    },
    {
        "raw_name": "майкоп",
        "original_name": "Майкоп"
    },
    {
        "raw_name": "нягань",
        "original_name": "Нягань"
    },
    {
        "raw_name": "саров",
        "original_name": "Саров"
    },
    {
        "raw_name": "северодвинск",
        "original_name": "Северодвинск"
    },
    {
        "raw_name": "старыйоскол",
        "original_name": "Старый Оскол"
    },
    {
        "raw_name": "троицк",
        "original_name": "Троицк"
    },
    {
        "raw_name": "шадринск",
        "original_name": "Шадринск"
    },
    {
        "raw_name": "подольск",
        "original_name": "Подольск"
    },
    {
        "raw_name": "дмитров",
        "original_name": "Дмитров"
    },
    {
        "raw_name": "дагомыс",
        "original_name": "Дагомыс"
    },
    {
        "raw_name": "краснаяполяна",
        "original_name": "Красная Поляна"
    },
    {
        "raw_name": "лазаревское",
        "original_name": "Лазаревское"
    },
    {
        "raw_name": "лоо",
        "original_name": "Лоо"
    },
    {
        "raw_name": "хоста",
        "original_name": "Хоста"
    },
    {
        "raw_name": "зеленоградск",
        "original_name": "Зеленоградск"
    },
    {
        "raw_name": "балашиха",
        "original_name": "Балашиха"
    },
    {
        "raw_name": "лысково",
        "original_name": "Лысково"
    },
    {
        "raw_name": "витязево",
        "original_name": "Витязево"
    },
    {
        "raw_name": "вельск",
        "original_name": "Вельск"
    },
    {
        "raw_name": "великийустюг",
        "original_name": "Великий Устюг"
    },
    {
        "raw_name": "кингисепп",
        "original_name": "Кингисепп"
    },
    {
        "raw_name": "звенигород",
        "original_name": "Звенигород"
    },
    {
        "raw_name": "северобайкальск",
        "original_name": "Северобайкальск"
    },
    {
        "raw_name": "первоуральск",
        "original_name": "Первоуральск"
    },
    {
        "raw_name": "ногинск",
        "original_name": "Ногинск"
    },
    {
        "raw_name": "электросталь",
        "original_name": "Электросталь"
    },
    {
        "raw_name": "тихорецк",
        "original_name": "Тихорецк"
    },
    {
        "raw_name": "ломоносов",
        "original_name": "Ломоносов"
    },
    {
        "raw_name": "дубна",
        "original_name": "Дубна"
    },
    {
        "raw_name": "брейтово",
        "original_name": "Брейтово"
    },
    {
        "raw_name": "железноводск",
        "original_name": "Железноводск"
    },
    {
        "raw_name": "голубицкая",
        "original_name": "Голубицкая"
    },
    {
        "raw_name": "грязи",
        "original_name": "Грязи"
    },
    {
        "raw_name": "эстосадок",
        "original_name": "Эсто-Садок"
    },
    {
        "raw_name": "ангелово",
        "original_name": "Ангелово"
    },
    {
        "raw_name": "знаменский",
        "original_name": "Знаменский"
    },
    {
        "raw_name": "архипоосиповка",
        "original_name": "Архипо-Осиповка"
    },
    {
        "raw_name": "горячийключ",
        "original_name": "Горячий Ключ"
    },
    {
        "raw_name": "домбай",
        "original_name": "Домбай"
    },
    {
        "raw_name": "животино",
        "original_name": "Животино"
    },
    {
        "raw_name": "королёв",
        "original_name": "Королёв"
    },
    {
        "raw_name": "курово",
        "original_name": "Курово"
    },
    {
        "raw_name": "мышкин",
        "original_name": "Мышкин"
    },
    {
        "raw_name": "небуг",
        "original_name": "Небуг"
    },
    {
        "raw_name": "никола",
        "original_name": "Никола"
    },
    {
        "raw_name": "сукко",
        "original_name": "Сукко"
    },
    {
        "raw_name": "шерегеш",
        "original_name": "Шерегеш"
    },
    {
        "raw_name": "янтарный",
        "original_name": "Янтарный"
    },
    {
        "raw_name": "морское",
        "original_name": "Морское"
    },
    {
        "raw_name": "гурзуф",
        "original_name": "Гурзуф"
    },
    {
        "raw_name": "евпатория",
        "original_name": "Евпатория"
    },
    {
        "raw_name": "керчь",
        "original_name": "Керчь"
    },
    {
        "raw_name": "коктебель",
        "original_name": "Коктебель"
    },
    {
        "raw_name": "курпаты",
        "original_name": "Курпаты"
    },
    {
        "raw_name": "черноморскоекрым",
        "original_name": "Черноморское, Крым"
    },
    {
        "raw_name": "одинцово",
        "original_name": "Одинцово"
    },
    {
        "raw_name": "жуковский",
        "original_name": "Жуковский"
    },
    {
        "raw_name": "конаково",
        "original_name": "Конаково"
    },
    {
        "raw_name": "петроводальнее",
        "original_name": "Петрово-Дальнее"
    },
    {
        "raw_name": "городец",
        "original_name": "Городец"
    },
    {
        "raw_name": "иноземцево",
        "original_name": "Иноземцево"
    },
    {
        "raw_name": "тургояк",
        "original_name": "Тургояк"
    }
]

SCHEMA_NAME: str = 'data'

TABLE: dict[str, list] = {
    'cities': cities
}


def upgrade() -> None:
    # Конвертируем текущее время в строковый формат
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ### commands auto generated by Alembic - please adjust! ###
    conn: sa.Connection = op.get_bind()
    metadata = sa.MetaData(schema=SCHEMA_NAME)
    metadata.reflect(bind=conn)

    for table_name, table_data in TABLE.items():
        table: sa.Table = metadata.tables[f"{SCHEMA_NAME}.{table_name}"]

        # Добавляем поле "id" начиная с 1 и поле "dt"
        #   к каждому городу в словарях
        for i, city in enumerate(table_data, start=1):
            city['id'] = i
            city['dt'] = current_time

        insert_stmt = psql_insert(table).values(table_data)
        insert_stmt = insert_stmt.on_conflict_do_nothing()
        conn.execute(insert_stmt)
    # ### end Alembic commands ###


def downgrade() -> None:
    conn: sa.Connection = op.get_bind()
    metadata = sa.MetaData(schema=SCHEMA_NAME)
    metadata.reflect(bind=conn)

    for table_name, table_data in TABLE.items():
        table: sa.Table = metadata.tables[f"{SCHEMA_NAME}.{table_name}"]

        # Добавляем временный id к каждой строке в словаре
        for i, row in enumerate(table_data, start=1):
            row['id'] = i

        # Удаляем строки из таблицы по временному id
        for row in table_data:
            id_value = row['id']
            delete_stmt = table.delete().where(table.c.id == id_value)
            conn.execute(delete_stmt)
