import asyncio
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
import requests
from fake_useragent import UserAgent
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard import menu, tarif_num, cancel, cat, next
from aiogram.fsm.context import FSMContext
from loader import scheduler


list_num = []
ua = UserAgent()
router = Router()
list_cat = [
        'ordinary,bronze,bronze_vip,bronze AAA', 'platinum,platinum_lite', 'brilliant,brilliant_super',
        'gold', 'silver,silver_special,silver_special_2'
    ]
dict_cat = {
    'gold': 'gold',
    'brilliant': 'brilliant,brilliant_super',
    'platinum': 'platinum,platinum_lite',
    'silver': 'silver,silver_special,silver_special_2',
    'bronze': 'ordinary,bronze,bronze_vip,bronze+AAA',
    '': ''
}


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
    await message.answer('Поиск отменен', reply_markup=menu)
    list_num.clear()
    scheduler.shutdown()


@router.message(F.text == 'Выберите тариф')
async def rate(message: Message, state: FSMContext):

    await state.set_state(FiltresSearch.tarif)
    await message.answer("Выберите тариф", reply_markup=tarif_num)


@router.message(FiltresSearch.tarif)
async def tariff(message: Message, state: FSMContext):

    if message.text == 'Пропустить':
        await state.update_data(tarif='')
    elif message.text == '2000+':
        await state.update_data(tarif='2000,2500,3000,4000')
    elif message.text != 'Пропустить' and message.text != '2000+':
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
    cat_phone = dict_cat[cat_phone]
    await base_set(tarif_phone, maska_phone, cat_phone, list_cat)
    await message.answer("Приступаю к поиску!", reply_markup=cancel)
    # await publication(message, tarif_phone, maska_phone, cat_phone, list_cat)
    scheduler.start()
    scheduler.add_job(publication, "interval", seconds=2, args=(message, tarif_phone, maska_phone, cat_phone, list_cat))


async def url_page(maska_phone, tarif_phone, cat_phone):
    page = 0
    flag = True

    while flag:
        page += 1

        headers = {'User-agent': ua.random}
        session = requests.Session()
        session.headers.update(headers)

        res_num = session.get(
            f"https://api.store.bezlimit.ru/v2/super-link/phones/mask-category?mask-category={cat_phone}"
            f"&phone_pattern={maska_phone}&service_limit={tarif_phone}&group_by=mask-category&page={page}&"
            f"expand=tariff,region&per_page=50"
        )

        dict_num = res_num.json()

        if dict_num[cat_phone]['_meta']['pageCount'] < page:
            flag = False

        yield dict_num


async def base_set(tarif_phone, maska_phone, cat_phone, list_cat):

        if cat_phone not in list_cat:

            for j in list_cat:
                async for dict_num in url_page(maska_phone, tarif_phone, j):
                    if len(dict_num[j]['items']) == 0:
                        continue

                    else:
                        for i in dict_num[j]['items']:
                            if i['phone'] not in list_num:
                                list_num.append(i['phone'])
                            else:
                                continue

                # print(f"{j}-{len(list_num)}")

        elif cat_phone in list_cat:
            async for dict_num in url_page(maska_phone, tarif_phone, cat_phone):
                if len(dict_num[cat_phone]['items']) == 0:
                    continue
                else:
                    for i in dict_num[cat_phone]['items']:
                        if i['phone'] not in list_num:
                            list_num.append(i['phone'])

        # print(f"All-{len(list_num)}")


async def publication(message, maska_phone, tarif_phone, cat_phone, list_cat):

    # while True:

        # await asyncio.sleep(2)

        if cat_phone not in list_cat:

            for j in list_cat:
                async for dict_num in url_page(tarif_phone, maska_phone, j):
                    if len(dict_num[j]['items']) == 0:
                        continue
                    else:
                        for i in dict_num[j]['items']:
                            if i['phone'] not in list_num:
                                list_num.append(i['phone'])
                                await message.answer(f"{i['phone']}")
                                await asyncio.sleep(1)
                            else:
                                continue

        elif cat_phone in list_cat:
            async for dict_num in url_page(tarif_phone, maska_phone, cat_phone):
                for i in dict_num[cat_phone]['items']:
                    if i['phone'] not in list_num:
                        list_num.append(i['phone'])
                        await message.answer(f"{i['phone']}")
                        await asyncio.sleep(1)
                    else:
                        continue