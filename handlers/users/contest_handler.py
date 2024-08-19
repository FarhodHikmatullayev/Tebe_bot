import asyncio
import random
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType

from keyboards.default.menu import back_menu_keyboard
from keyboards.inline.confirmation import confirm_keyboard, confirm_start_test_keyboard, test_callback_data
from keyboards.inline.test_keyboards import test_category_keyboard, send_answers_keyboard, answers_keyboard_data
from loader import dp, db, bot
from states.test_ansvers import Test
from utils.format_answers import parse_string_to_dict


async def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes} daqiqa, {seconds} soniya"


@dp.message_handler(Command('start_test'), state='*')
async def start_contest(message: Message, state: FSMContext):
    await state.finish()
    text = "Qanday test yechmoqchisiz?"
    await message.answer(text=text, reply_markup=test_category_keyboard)


@dp.callback_query_handler(text='specialist')
async def for_specialists(call: CallbackQuery):
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user = users[0]
    tests = await db.select_tests(for_who='specialists')
    if not tests:
        text = "Xali test mavjud emas"
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        results = await db.select_result(user_id=user['id'])
        results_id = []
        if results:
            for result in results:
                results_id.append(result['id'])

        test_ids = [test['id'] for test in tests]
        filtered_tests_id = [item for item in test_ids if item not in results_id]
        if not filtered_tests_id:
            await call.message.answer(text="Siz allaqachon hamma testlarda o'zingizni sinab ko'rgansiz\n"
                                           "Hozircha yangi test mavjud emas", reply_markup=back_menu_keyboard)
        else:
            random_test_id = random.choice(filtered_tests_id)
            tests = await db.select_tests(id=random_test_id)
            test = tests[0]
            duration = test['time_limit']
            format_time = await format_duration(duration)
            print('time_limit', duration)
            text = f"Siz uchun random test tanlandi\n" \
                   f"Sizga test yechish uchun {format_time} vaqt beriladi\n" \
                   f"Agarda ulgurmasangiz sizning natijangiz 0 deb hisoblanadi"
            await call.message.edit_text(text=text)
            text = "Testni boshlashga tayyormisiz?"
            markup = await confirm_start_test_keyboard(test_id=random_test_id)
            await call.message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(text='worker')
async def for_workers(call: CallbackQuery):
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user = users[0]
    tests = await db.select_tests(for_who='workers')
    if not tests:
        text = "Xali test mavjud emas"
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        results = await db.select_result(user_id=user['id'])
        print('results', results)
        results_id = []
        if results:
            for result in results:
                results_id.append(result['test_id'])
        print('results_id', results_id)
        test_ids = [test['id'] for test in tests]
        filtered_tests_id = [item for item in test_ids if item not in results_id]
        print('filtered_tests_id', filtered_tests_id)
        if not filtered_tests_id:
            await call.message.answer(text="Siz allaqachon hamma testlarda o'zingizni sinab ko'rgansiz\n"
                                           "Hozircha yangi test mavjud emas", reply_markup=back_menu_keyboard)
        else:
            random_test_id = random.choice(filtered_tests_id)
            tests = await db.select_tests(id=random_test_id)
            test = tests[0]
            duration = test['time_limit']
            format_time = await format_duration(duration)
            print('time_limit', duration)
            text = f"Siz uchun random test tanlandi\n" \
                   f"Sizga test yechish uchun {format_time} vaqt beriladi\n" \
                   f"Agarda ulgurmasangiz sizning natijangiz 0 deb hisoblanadi"
            await call.message.edit_text(text=text)
            text = "Testni boshlashga tayyormisiz?"
            markup = await confirm_start_test_keyboard(test_id=random_test_id)
            await call.message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(test_callback_data.filter())
async def start_test(call: CallbackQuery, callback_data: dict):
    test_id = callback_data.get('test_id')
    test_id = int(test_id)
    confirmation = callback_data.get('confirm')
    if confirmation == 'no':
        text = "Siz testni boshlashni rad etdingiz"
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif confirmation == 'yes':
        tests = await db.select_tests(id=test_id)
        test = tests[0]
        duration = test['time_limit']
        format_time = await format_duration(duration)
        photo = test['picture']
        red_line = test['red_line']
        title = test['title']
        current_time = datetime.datetime.now()
        deadline = current_time + duration
        text = f"Test title: {title}\n" \
               f"O'tish bali: {red_line} ta tog'ri bo'lishi kerak\n" \
               f"Vaqt: Sizga {format_time} vaqt berildi, vaqt {deadline.strftime('%Y-%m-%d %H:%M:%S')} dan keyin sizning natijangiz hisobga olinmaydi"
        await call.message.edit_text(text=text)
        await asyncio.sleep(3)  # this function will wait 3 seconds
        sent_message = await call.message.answer("Qani ketdik...1")
        await asyncio.sleep(3)  # this function will wait 3 seconds

        await bot.edit_message_text(
            text="Qani ketdik...2",
            chat_id=call.message.chat.id,
            message_id=sent_message.message_id
        )

        await asyncio.sleep(3)  # this function will wait 3 seconds
        await bot.edit_message_text(
            text="Qani ketdik...3",
            chat_id=call.message.chat.id,
            message_id=sent_message.message_id
        )

        await asyncio.sleep(3)
        await bot.edit_message_text(
            text="Boshladik...!\n"
                 "Vaqt ketdi ..⌛",
            chat_id=call.message.chat.id,
            message_id=sent_message.message_id
        )

        await asyncio.sleep(2)  # this function will wait 2 seconds

        markup = await send_answers_keyboard(test_id=test_id, time=current_time.strftime('%Y-%m-%d %H_%M_%S'))
        await call.message.answer(
            text=f"{photo}",
            reply_markup=markup
        )


@dp.callback_query_handler(answers_keyboard_data.filter())
async def get_answers(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user_id = users[0]['id']
    time = callback_data.get("time")
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H_%M_%S')
    print('time_type', type(time))
    test_id = callback_data.get('test_id')
    test_id = int(test_id)
    tests = await db.select_tests(id=test_id)
    test = tests[0]
    count_questions = test['count_questions']
    duration = test['time_limit']
    await state.update_data(
        {
            'test_id': test_id,
            'time': time
        }
    )
    if time + duration < datetime.datetime.now():
        result = await db.create_result(
            counts_true=0,
            counts_false=count_questions,
            time_duration=datetime.datetime.now() - time,
            is_successful=False,
            user_id=user_id,
            test_id=test_id,
        )
        text = "Sizning vaqtingiz allaqachon tugagan\n" \
               "Afsuski natijangiz 0 deb hisoblanadi"
        await call.message.answer(text=text)
    else:
        text = "Javobni quyidagi formatda kiriting.\n" \
               "1a2b3c4d5a6b7c....16b17d18c19c20a"
        await call.message.answer(text=text)
        await Test.answer.set()


@dp.message_handler(state=Test.answer)
async def get_answers(message: Message, state: FSMContext):
    data = await state.get_data()
    time = data.get('time')
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user_id = users[0]['id']
    data = await state.get_data()
    test_id = data.get('test_id')
    tests = await db.select_tests(id=test_id)
    test = tests[0]
    red_line = test['red_line']
    answer = message.text
    answers_dict = await parse_string_to_dict(answer)
    true_answers_dict = await parse_string_to_dict(test['answers'])
    checked_answers = dict()
    true_answers_count = 0
    false_answers_count = 0
    for key in true_answers_dict:
        if key in answers_dict:
            if answers_dict[key] == true_answers_dict[key]:
                checked_answers[key] = answers_dict[key] + "✅"
                true_answers_count += 1
            else:
                checked_answers[key] = answers_dict[key] + "❌"
                false_answers_count += 1
        else:
            checked_answers[key] = "❌"
            false_answers_count += 1

    await db.create_result(
        counts_true=true_answers_count,
        counts_false=false_answers_count,
        time_duration=datetime.datetime.now() - time,
        is_successful=true_answers_count >= red_line,
        user_id=user_id,
        test_id=test_id
    )
    text = "Sizning natijangiz qabul qilindi"
    await message.answer(text=text)

    await asyncio.sleep(3)

    text = ""
    for key in checked_answers:
        text += f"{key}. {checked_answers[key]}\n"
    await message.answer(text=text)
    if true_answers_count >= red_line:
        text = f"Siz testni {true_answers_count / (true_answers_count + false_answers_count) * 100} % natija bilan muvaffaqiyatli yakunladingiz "
    else:
        text = f"Afsuski siz {true_answers_count / (true_answers_count + false_answers_count) * 100} % natija ko'rsatdingiz va testdan o'ta olmadingiz"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
    await state.finish()
