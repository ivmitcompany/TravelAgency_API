from django.core.management.base import BaseCommand
from travel_api.models import *

tours = [
    {
        "name": "Пікнік на г. Близниця",
        "name_ru": "Пикник на г. Близница",
        "description": "Запрошуємо вас на незабутній пікнік на горі Близниця! Цей тур заповнений пригодами та красою Карпатських гір, включаючи відвідування озера Бренскули та чаювання біля озера. Вечори ви проведете, насолоджуючись вечерею з кальяном, а також розслабляючись у чані чи бані. Другий день буде присвячений підйому на вершину Близниця, де вас чекають чарівні краєвиди та водоспад Піп Іван. Завершиться тур вечерею на вогнищі та відпочинком у чанах.",
        "description_ru": "Приглашаем вас на незабываемый пикник на горе Близница! Этот тур наполнен приключениями и красотой Карпатских гор, включая посещение озера Бренскулы и чаепитие у озера. Вечера вы проведете, наслаждаясь ужином с кальяном, а также расслабляясь в чане или бане. Второй день будет посвящен подъему на вершину Близница, где вас ждут волшебные пейзажи и водопад Пип Иван. Тур завершится ужином у костра и отдыхом в чанах.",
        "places": 0,
        "free_places": 0,
        "date_start": "2024-01-01",
        "date_end": "2024-01-01",
        "price": 0
    },
    {
        "name": "Підкорюємо Жандарми",
        "name_ru": "Покоряем Жандармы",
        "description": "Цей захоплюючий тур веде вас через мальовничі Карпати до гір Жандарм. Ви відвідуєте сироварню для дегустації, насолоджуєтесь їздою на квадроциклах, а вечори проведете біля вогню з кальяном. Також ви відвідуєте масив Свидовець та насолоджуєтесь пікніком на вершинах. Ваш пригодницький досвід завершиться чаюванням з неймовірним краєвидом біля озера Апшпинець і відвідуванням Труфанецького водоспаду.",
        "description_ru": "Этот увлекательный тур ведет вас через живописные Карпаты к горам Жандарм. Вы посетите сыроварню для дегустации, насладитесь поездкой на квадроциклах, а вечера проведете у костра с кальяном. Также вы посетите массив Свидовец и насладитесь пикником на вершинах. Ваше приключенческое путешествие завершится чаепитием с невероятным пейзажем у озера Апшпинец и посещением Труфанецкого водопада.",
        "places": 0,
        "free_places": 0,
        "date_start": "2024-01-01",
        "date_end": "2024-01-01",
        "price": 0
    },
    {
        "name": "Синевир",
        "name_ru": "Синевир",
        "description": "Відправляйтеся в неймовірну подорож до озера Синевир. Відвідайте оленячу ферму, термальні води та насолоджуйтеся вечерею з кальяном. Тур також включає чаювання з краєвидами озера, дегустацію сиру та м'ясних виробів. Третій день пропонує прогулянку Закарпаттям і відвідування Хустського замку.",
        "description_ru": "Отправляйтесь в невероятное путешествие к озеру Синевир. Посетите оленью ферму, термальные воды и наслаждайтесь ужином с кальяном. Тур также включает чаепитие с видами озера, дегустацию сыра и мясных изделий. Третий день предлагает прогулку по Закарпатью и посещение Хустского замка.",
        "places": 0,
        "free_places": 0,
        "date_start": "2024-01-01",
        "date_end": "2024-01-01",
        "price": 0,
    },
    {
        "name": "Тіні забутих предків",
        "name_ru": "Тени забытых предков",
        "description": "Цей тур занурить вас у світ кінофільму 'Тіні забутих предків'. Ви відвідаєте хату-музей фільму, музей гуцульської магії та насолодитесь прогулянкою Карпатами. Вечори будуть наповнені BBQ вечерями та кальяном. Ви також підете на г. Піп Іван, насолоджуючись пікніком на вершині.",
        "description_ru": "Этот тур погрузит вас в мир кинофильма 'Тени забытых предков'. Вы посетите дом-музей фильма, музей гуцульской магии и насладитесь прогулкой по Карпатам. Вечера будут наполнены BBQ ужинами и кальяном. Вы также отправитесь на г. Пип Иван, наслаждаясь пикником на вершине.",
        "places": 0,
        "free_places": 0,
        "date_start": "2024-01-01",
        "date_end": "2024-01-01",
        "price": 0,
    },
    {
        "name": "Підкорюємо Хом'яка",
        "name_ru": "Покоряем Хомяка",
        "description": "Цей тур дозволить вам підкорити гору Хом'як, де вас очікують незабутні краєвиди. Вас чекає прогулянка Карпатами, відвідування Жинецького водоспаду, обід в колибі та ловля форелі. Вечірній час пропонує вечерю на вогні, кальян та відпочинок у чані чи бані.",
        "description_ru": "Этот тур позволит вам покорить гору Хомяк, где вас ждут незабываемые пейзажи. Вас ждет прогулка по Карпатам, посещение Жинецкого водопада, обед в колыбе и ловля форели. Вечернее время предлагает ужин у костра, кальян и отдых в чане или бане.",
        "places": 0,
        "free_places": 0,
        "date_start": "2024-01-01",
        "date_end": "2024-01-01",
        "price": 0
    },
    {
        "name": "Велична Говерла",
        "name_ru": "Величественная Говерла",
        "description": "Приєднуйтесь до нас у захоплюючому поході на найвищу вершину України - Говерлу. По дорозі вас чекають прогулянки Карпатами, відвідування Прутського водоспаду та вечері біля вогню. Ви насолодитесь пікніком на вершині, катанням на джипах та дегустацією наливок.",
        "description_ru": "Присоединяйтесь к нам в увлекательном походе на самую высокую вершину Украины - Говерлу. По пути вас ждут прогулки по Карпатам, посещение Прутского водопада и ужины у костра. Вы насладитесь пикником на вершине, катанием на джипах и дегустацией настоек.",
        "places": 0,
        "free_places": 0,
        "date_start": "2024-01-01",
        "date_end": "2024-01-01",
        "price": 0
    },
    {
        "name": "Кам'янець",
        "name_ru": "Каменец",
        "description": "Відкрийте для себе історичне місто Кам'янець з його вражаючим замком і старовинною архітектурою. Тур включає відвідування Кришталевої печери та замку Хотин. Ви насолодитесь прогулянкою старим містом, відчувши дух історії та культури. Тур завершується оглядовою екскурсією та поверненням додому.",
        "description_ru": "Откройте для себя исторический город Каменец с его впечатляющим замком и древней архитектурой. Тур включает посещение Кристальной пещеры и замка Хотин. Вы насладитесь прогулкой по старому городу, почувствовав дух истории и культуры. Тур завершается обзорной экскурсией и возвращением домой.",
        "places": 0,
        "free_places": 0,
        "date_start": "2024-01-01",
        "date_end": "2024-01-01",
        "price": 0
    }
]


class Command(BaseCommand):
    help = 'Generate fake data for tours'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='Number of fake entries to generate')

    def handle(self, *args, **kwargs):
        num_entries = kwargs['num_entries']

        for i in tours:
            Tour.objects.create(
                name=i['name'],
                name_ru=i['name_ru'],
                description=i['description'],
                description_ru=i['description_ru'],
                price=i['price'],
                places=i['places'],
                free_places=i['free_places'],
                # is_featured=random.choice([True, False]),
                date_start=i['date_start'],
                date_end=i['date_end'],
                # status=random.choice(Status.objects.all()),
                # season=random.choice(Season.objects.all())
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_entries} fake data entries'))
