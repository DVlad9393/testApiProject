from microservice.models import UserData, SupportData

users_db = {
    1: UserData(
        id=1,
        email='george.bluth@reqres.in',
        first_name='George',
        last_name='Bluth',
        avatar='https://reqres.in/img/faces/1-image.jpg'
    ),
    2: UserData(
        id=2,
        email='janet.weaver@reqres.in',
        first_name='Janet',
        last_name='Weaver',
        avatar='https://reqres.in/img/faces/2-image.jpg'
    ),
    3: UserData(
        id=3,
        email='emma.wong@reqres.in',
        first_name='Emma',
        last_name='Wong',
        avatar='https://reqres.in/img/faces/3-image.jpg'
    ),
    4: UserData(
        id=4,
        email='eve.holt@reqres.in',
        first_name='Eve',
        last_name='Holt',
        avatar='https://reqres.in/img/faces/4-image.jpg'
    ),
    5: UserData(
        id=5,
        email='charles.morris@reqres.in',
        first_name='Charles',
        last_name='Morris',
        avatar='https://reqres.in/img/faces/5-image.jpg'
    ),
    6: UserData(
        id=6,
        email='tracey.ramos@reqres.in',
        first_name='Tracey',
        last_name='Ramos',
        avatar='https://reqres.in/img/faces/6-image.jpg'
    ),
    7: UserData(
        id=7,
        email='michael.lawson@reqres.in',
        first_name='Michael',
        last_name='Lawson',
        avatar='https://reqres.in/img/faces/7-image.jpg'
    ),
    8: UserData(
        id=8,
        email='lindsay.ferguson@reqres.in',
        first_name='Lindsay',
        last_name='Ferguson',
        avatar='https://reqres.in/img/faces/8-image.jpg'
    ),
    9: UserData(
        id=9,
        email='tobias.funke@reqres.in',
        first_name='Tobias',
        last_name='Funke',
        avatar='https://reqres.in/img/faces/9-image.jpg'
    ),
    10: UserData(
        id=10,
        email='byron.fields@reqres.in',
        first_name='Byron',
        last_name='Fields',
        avatar='https://reqres.in/img/faces/10-image.jpg'
    ),
    11: UserData(
        id=11,
        email='george.edwards@reqres.in',
        first_name='George',
        last_name='Edwards',
        avatar='https://reqres.in/img/faces/11-image.jpg'
    ),
    12: UserData(
        id=12,
        email='rachel.howell@reqres.in',
        first_name='Rachel',
        last_name='Howell',
        avatar='https://reqres.in/img/faces/12-image.jpg'
    ),
    13: UserData(
        id=13,
        email='olivia.coleman@reqres.in',
        first_name='Olivia',
        last_name='Coleman',
        avatar='https://reqres.in/img/faces/13-image.jpg'
    ),
    14: UserData(
        id=14,
        email='liam.wilson@reqres.in',
        first_name='Liam',
        last_name='Wilson',
        avatar='https://reqres.in/img/faces/14-image.jpg'
    ),
    15: UserData(
        id=15,
        email='ava.jones@reqres.in',
        first_name='Ava',
        last_name='Jones',
        avatar='https://reqres.in/img/faces/15-image.jpg'
    ),
    16: UserData(
        id=16,
        email='noah.brown@reqres.in',
        first_name='Noah',
        last_name='Brown',
        avatar='https://reqres.in/img/faces/16-image.jpg'
    ),
    17: UserData(
        id=17,
        email='mia.davis@reqres.in',
        first_name='Mia',
        last_name='Davis',
        avatar='https://reqres.in/img/faces/17-image.jpg'
    ),
    18: UserData(
        id=18,
        email='lucas.garcia@reqres.in',
        first_name='Lucas',
        last_name='Garcia',
        avatar='https://reqres.in/img/faces/18-image.jpg'
    ),
    19: UserData(
        id=19,
        email='sophia.martinez@reqres.in',
        first_name='Sophia',
        last_name='Martinez',
        avatar='https://reqres.in/img/faces/19-image.jpg'
    ),
    20: UserData(
        id=20,
        email='benjamin.rodriguez@reqres.in',
        first_name='Benjamin',
        last_name='Rodriguez',
        avatar='https://reqres.in/img/faces/20-image.jpg'
    ),
}

support_info = SupportData(
    url="https://reqres.in/#support-heading",
    text="To keep ReqRes free, contributions towards server costs are appreciated!"
)