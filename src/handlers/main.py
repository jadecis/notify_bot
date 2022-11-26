from loader import bot, dp, html, Data, db
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart 
from src.others import messages as mes
from src.keyboarbs.reply import main_menu
from src.keyboarbs.inline import timezone_menu, func_menu, back_but
from datetime import datetime, time


@dp.message_handler(CommandStart(), state="*")
async def start_handler(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=mes.start_message, reply_markup=main_menu)
    
@dp.message_handler(content_types=['text'])
async def menu_handler(msg: Message, state: FSMContext):
    await state.finish()
    if msg.text == 'Меню':
        await msg.answer("Укажите ваш часовой пояс.", reply_markup=timezone_menu)

@dp.callback_query_handler(text='back', state=Data.date)     
@dp.callback_query_handler(text_contains='zone_')
async def timezone_handler(call: CallbackQuery, state: FSMContext):
    if call.data != 'back':
        await state.update_data(gmt= int(call.data.split('_')[1]))
    await call.message.edit_text("Выберите.", reply_markup=func_menu)
    await Data.Q1.set()

@dp.callback_query_handler(text='back', state=Data.time) 
@dp.callback_query_handler(text_contains='func_', state=Data.Q1)
async def func_handler(call: CallbackQuery, state: FSMContext):
    if call.data != 'back':
        await state.update_data(func= call.data.split('_')[1])
    await call.message.edit_text("Укажите дату (дд.мм.гггг)", reply_markup=back_but)
    await Data.date.set()

@dp.callback_query_handler(text='back', state=Data.remind) 
async def back_date(call: CallbackQuery, state: FSMContext):
    data= await state.get_data()
    if data.get('func') == 'alarm':
        view= 'будильника'
    if data.get('func') == 'notify':
        view= 'напоминания'
    await call.message.answer(f"Укажите время {view} в 24-ом формате (чч:мм)", reply_markup=back_but)
    await Data.time.set()

@dp.message_handler(content_types=['text'], state=Data.date)
async def date_handler(msg: Message, state: FSMContext):
    try:
        datetime.strptime(msg.text, '%d.%m.%Y')
        await state.update_data(date= msg.text)
        data= await state.get_data()
        if data.get('func') == 'alarm':
            view= 'будильника'
        if data.get('func') == 'notify':
            view= 'напоминания'
        await msg.answer(f"Укажите время {view} в 24-ом формате (чч:мм)", reply_markup=back_but)
        await Data.time.set()
    except Exception as ex:
        print(ex)
        await msg.answer(text=mes.error_input)
        await Data.date.set()
        
        
@dp.message_handler(content_types=['text'], state=Data.time)
async def time_handler(msg: Message, state: FSMContext):
    data= await state.get_data()
    dt= f"{data.get('date').strip()} {msg.text.strip()}"
    try:
        new_dt= datetime.strptime(dt, '%d.%m.%Y %H:%M')
        await state.update_data(date=new_dt)   
        if data.get('func') == 'alarm':
            gmt=data.get('gmt')
            db.add(
                user_id=msg.chat.id,
                dt=new_dt,
                gmt=gmt
            )
            await msg.answer("Пожалуйста, <b>не отключайте уведомления</b> от Бота", parse_mode=html)
            await state.finish()
        if data.get('func') == 'notify':
            await msg.answer("Введите текст напоминания.", reply_markup=back_but)
            await Data.remind.set()
    except Exception as ex:
        print(ex)
        await msg.answer(text=mes.error_input)
        await Data.time.set()
    
@dp.message_handler(content_types=['text'], state=Data.remind)
async def remind_handler(msg: Message, state: FSMContext):
    data= await state.get_data()
    gmt=data.get('gmt')
    new_dt=data.get('date')
    db.add(
        user_id=msg.chat.id,
        dt=new_dt,
        gmt=gmt,
        text=msg.text
    )
    await msg.answer("Пожалуйста, <b>не отключайте уведомления</b> от Бота", parse_mode=html)
    await state.finish()