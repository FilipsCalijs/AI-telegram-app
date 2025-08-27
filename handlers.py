import os
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from function import *
from fsm_states import UserStates
from runpod.call_runpod import call_runpod_api 
from keyboards import main_menu, send_photo_menu, buy_credits_menu
<<<<<<< HEAD
from payments_stars import router as payments_router, buy_credits_keyboard
=======
from logs import log_message

>>>>>>> a907a8bd2dff48629764987fc5627ebfc127e782

async def send_user_agreement(message: types.Message):
    await message.answer(
        "📜 *User Agreement*\n\n" +
        """
By using this bot, you agree to the following terms:
1. You will not use this bot for any illegal activities.
2. You will not attempt to hack or disrupt the bot's services.

🎁 As a gift, you will receive 20 free credits upon agreeing to these terms.

        """,
        reply_markup=get_user_agreement_keyboard(),
        parse_mode="Markdown"
    )

def register_handlers(dp: Dispatcher, bot: Bot):
    dp.include_router(payments_router)

    @dp.message(Command("start"))
    async def start_handler(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        if is_user_agreed(user_id):
            await state.set_state(UserStates.MAIN_MENU)
            await message.answer("Welcome back! Choose an option:", reply_markup=main_menu)
        else:
            await send_user_agreement(message)

    @dp.callback_query(lambda c: c.data == "agree")
    async def on_agree(callback: types.CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        if not is_user_agreed(user_id):
            user_agreed.add(user_id)
            save_agreed_users(user_agreed)
<<<<<<< HEAD
=======
            await log_message("User agreed to the terms", user_id)

>>>>>>> a907a8bd2dff48629764987fc5627ebfc127e782
            add_credits(user_id, 20)
            await callback.message.answer("🎉 Thank you for agreeing! You have been credited with 20 free credits.")

        await state.set_state(UserStates.MAIN_MENU)
        await callback.message.edit_text("You agreed! ✅")
        await callback.message.answer(
            'Click "📸 Send photo" to upload an image and I\'ll process it for you.',
            reply_markup=main_menu
        )
        await callback.answer()

    @dp.message()
    async def global_handler(message: types.Message, state: FSMContext):
        user_id = message.from_user.id

        # Игнорируем бота и уведомления о повышении кредитов
        if message.from_user.is_bot:
            return
        if "Ваши кредиты увеличились" in (message.text or ""):
            return

        if not is_user_agreed(user_id):
            await send_user_agreement(message)
            return

        current_state = await state.get_state()
        if current_state is None:
            current_state = UserStates.MAIN_MENU.state

        # Основные меню и команды
        if message.text == "💰 Show my credits":
            user_credits = get_user_credits(user_id)
            await message.answer(f"💰 You have {user_credits} credits.")
            return

<<<<<<< HEAD
=======
        if message.text == "🛒 Buy credits" and current_state == UserStates.BUY_CREDITS.state:
            add_credits(user_id, 10)
            user_credits = get_user_credits(user_id)
            await log_message(f"User bought 10 credits and has {user_credits} credits", user_id)
            await message.answer(f"🛒 You bought 10 credits! Now you have {user_credits} credits.")
            return

        current_state = await state.get_state()
        if current_state is None:
            current_state = UserStates.MAIN_MENU.state

        if message.text == "📸 Send photo":
            await state.set_state(UserStates.SEND_PHOTO)
            await message.answer("Please upload a photo and I'll process it.", reply_markup=send_photo_menu)
            return

>>>>>>> a907a8bd2dff48629764987fc5627ebfc127e782
        if message.text == "💳 Buy credits":
            await state.set_state(UserStates.BUY_CREDITS)
            await message.answer("Select an option:", reply_markup=buy_credits_menu)
            return

        if message.text == "🛒 Buy credits" and current_state == UserStates.BUY_CREDITS.state:
            await message.answer("Select a package to buy:", reply_markup=buy_credits_keyboard())
            return

        if message.text == "📸 Send photo":
            await state.set_state(UserStates.SEND_PHOTO)
            await message.answer("Please upload a photo and I'll process it.", reply_markup=send_photo_menu)
            return

        if message.text == "⬅️ Back to menu":
            await state.set_state(UserStates.MAIN_MENU)
            await message.answer("Back to main menu:", reply_markup=main_menu)
            return

        if message.text == "🌐 Language":
            await message.answer("🌐 Language selection coming soon!")
            return

        if message.text == "👤 Profile":
            await message.answer("👤 Profile section coming soon!")
            return

<<<<<<< HEAD
        # Обработка фото
        if message.photo and current_state == UserStates.SEND_PHOTO.state:
            user_credits = get_user_credits(user_id)
            if user_credits < 10:
                await message.answer("⚠️ You don't have enough credits (10 required) to process the photo. Please buy credits.")
=======
        if message.photo:
            if current_state == UserStates.SEND_PHOTO.state:
                user_credits = get_user_credits(user_id)
                if user_credits < 10:
                    await message.answer("⚠️ You don't have enough credits (10 required) to process the photo. Please buy credits.")
                    return

                success = spend_credits(user_id, 10)
                if not success:
                    await message.answer("⚠️ Could not spend credits. Try again later.")
                    return

                await message.answer("✅ Got your photo. Processing... 10 credits spent.")
                file_path = await save_photo(message, bot)

                file_full_path = os.path.abspath(file_path)
                file_name = file_path.replace("photos/", "")

                time_start = time.time()
                processed_image = await call_runpod_api(IMAGE_PATH=file_full_path, image_name=file_name, user_id=user_id)
                end_time = time.time()

                if processed_image is None:
                    await message.answer("❌ Error processing the image. Please try again later.")
                    add_credits(user_id, 10)
                    return
                
                await log_message(f"Processed image in {end_time - time_start:.2f} seconds", user_id)

                # Path to blurred image
                blured_image = await blur_image(processed_image)

                file_send_2 = FSInputFile(blured_image)
                await bot.send_photo(chat_id=message.chat.id, photo=file_send_2, caption="Here is your blured image!")
                os.remove(blured_image)


                file_send = FSInputFile(processed_image)
                await bot.send_photo(chat_id=message.chat.id, photo=file_send, caption="Here is your image!")


                return
            else:
                await message.answer("⚠️ Photo processing is only available in the 'Send photo' section.")
>>>>>>> a907a8bd2dff48629764987fc5627ebfc127e782
                return

            success = spend_credits(user_id, 10)
            if not success:
                await message.answer("⚠️ Could not spend credits. Try again later.")
                return

            await message.answer("✅ Got your photo. Processing... 10 credits spent.")
            file_path = await save_photo(message, bot)
            file_full_path = os.path.abspath(file_path)
            file_name = os.path.basename(file_path)

            processed_image = await call_runpod_api(IMAGE_PATH=file_full_path, image_name=file_name, user_id=user_id)
            if processed_image is None:
                await message.answer("❌ Error processing the image. Please try again later.")
                return

            # Отправляем размытую версию
            blured_image = await blur_image(processed_image)
            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(blured_image), caption="Here is your blured image!")
            os.remove(blured_image)

            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(processed_image), caption="Here is your image!")
            return

        # Всё остальное игнорируем без сообщения об ошибке
        return
