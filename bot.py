import asyncio
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
import requests
from fake_useragent import UserAgent
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard import menu, tarif_num, menu_admin, cancel, cat, next
from aiogram.fsm.context import FSMContext
from loader import scheduler


list_num = []
list_new = []
ua = UserAgent()
router = Router()


class FiltresSearch(StatesGroup):
    tarif = State()
    maska_num = State()
    categories = State()


@router.message(CommandStart())
async def comand_start_handler(message: Message):

    await message.answer(f"Hello, {message.from_user.full_name}!\n", reply_markup=menu)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена поиска")
async def cmd_cancel(message: Message, state: FSMContext):

    await state.clear()
    flag = False
    await message.answer('Поиск отменен', reply_markup=menu_admin)


@router.message(F.text == 'Выберите тариф')
async def rate(message: Message, state: FSMContext):

    await state.set_state(FiltresSearch.tarif)
    await message.answer("Выберите тариф", reply_markup=tarif_num)


@router.message(FiltresSearch.tarif)
async def tariff(message: Message, state: FSMContext):

    if message.text == 'Пропустить':
        await state.update_data(tarif='')
    else:
        await state.update_data(tarif=message.text)

    await message.answer("Введите маску - например NNNAAABBB или номер или нажмите пропустить", reply_markup=next)
    await state.set_state(FiltresSearch.maska_num)


@router.message(FiltresSearch.maska_num)
async def mask(message: Message, state: FSMContext):

    if message.text == 'Пропустить':
        await state.update_data(maska_num='')
    else:
        await state.update_data(maska_num=message.text)

    await message.answer("Выберите категорию или нажмите пропустить", reply_markup=cat)
    await state.set_state(FiltresSearch.categories)


@router.message(FiltresSearch.categories)
async def cat_num(message: Message, state: FSMContext):

    if message.text == 'Пропустить':
        await state.update_data(categories='')
    else:
        await state.update_data(categories=message.text)

    data = await state.get_data()
    tarif_phone = data['tarif']
    maska_phone = data['maska_num']
    cat_phone = data['categories']
    dict_cat = {
        'gold': 'gold',
        'brilliant': 'brilliant,brilliant_super',
        'platinum': 'platinum,platinum_lite',
        'silver': 'silver,silver_special,silver_special_2',
        'bronze': 'ordinary,bronze,bronze_vip,bronze+AAA',
        '': ''
    }
    cat_phone = dict_cat[cat_phone]
    await message.answer("Приступаю к поиску!", reply_markup=cancel)
    await base_set(tarif_phone, maska_phone, cat_phone)
    await search(message, tarif_phone, maska_phone, cat_phone)
    scheduler.add_job(search, "interval", seconds=2, args=(message, tarif_phone, maska_phone, cat_phone))


async def base_set(tarif_phone, maska_phone, cat_phone):

    headers = {'User-agent': ua.random}
    session = requests.Session()
    session.headers.update(headers)

    res_num = session.get(
        f"https://api.store.bezlimit.ru/v2/super-link/phones/mask-category?mask-category={cat_phone}&service_limit={tarif_phone}&"
        f"group_by=mask-category&expand=tariff,region&per_page=200")  # bezlimit

    dict_num = res_num.json()
    # print(dict_num) # ['ordinary,bronze,bronze_vip,bronze AAA'] ['platinum,platinum_lite'] ['brilliant,brilliant_super']

    for i in dict_num[cat_phone]['items']:

        if i['phone'] not in list_num:
            list_num.append(i['phone'])
        else:
            continue
    print(list_num)
    return dict_num


async def search(message, tarif_phone, maska_phone, cat_phone):

    headers = {'User-agent': ua.random}
    session = requests.Session()
    session.headers.update(headers)

    res_num = session.get(f"https://api.store.bezlimit.ru/v2/super-link/phones/mask-category?service_limit={tarif_phone}&"
                            f"group_by=mask-category&expand=tariff,region&per_page=200") #bezlimit

    # data_num = {
    #     'sort': '-tariff_price',
    #     'type': 'standard',
    #     'service_limit': tarif_phone,
    #     'is_reserved': 'true',
    #     'per_page': 6,
    #     'expand': 'reservation,tariff,region,mask,priceParams'
    # }

    # res_num = session.get(f"https://api.store.bezlimit.ru/v2/phones?sort=-tariff_price&type=standard&"
    #                       f"service_limit={tarif_phone}&is_reserved=true&per_page=6&expand=reservation,tariff,region,mask,priceParams") #bezlimit_store
    # res_num = session.get(
    #     f'https://www.anncom.ru/dialer/lendingbezlimit/main.py?tariff={tarif_phone}&'
    #     f'phone_pattern={maska_phone}&region=&pattern=categories&phone_categories={cat_phone}&pageLimit=1000'
    # ) #bezlimit_club

    dict_num = res_num.json()
    # print(dict_num) # ['ordinary,bronze,bronze_vip,bronze AAA'] ['platinum,platinum_lite'] ['brilliant,brilliant_super']

    # for i in dict_num['platinum,platinum_lite']['items']:
    #
    #     if i['phone'] not in list_num:
    #         list_num.append(i['phone'])
    #     else:
    #         continue
        # data_num = {'phone': i['phone'],
        #             'tariff_id': '13101',
        #             'type': 'store',
        #             'user_id': 486739,
        #             'filter': 'professional'
        #             }
        # tar = session.post('https://api.store.bezlimit.ru/v2/super-link/reservations?expand=tariff', data=data_num)
        # reservetion = session.options(
        #     f"https://api.store.bezlimit.ru/v2/super-link/reservations?phone={i['phone']}&user_id=486739") #480524
        # await message.answer(f"Номер - {i['phone']} забронирован!")

    return await publication(message, dict_num)


async def publication(message, dict_num):

    for i in dict_num['platinum,platinum_lite']['items']:

        if i['phone'] not in list_num:
            list_num.append(i['phone'])
            await message.answer(f"{i['phone']}")
            continue

        await asyncio.sleep(1)