import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import os
import pathlib
from dotenv import load_dotenv
from gpt_api import get_answer_gpt_3, get_answer_gpt_4

current_path = pathlib.Path(__file__).parent.parent.resolve()
dotenv_path = os.path.join(current_path.absolute(), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot_token = os.environ["API_TOKEN"]
bot = Bot(token=bot_token)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        """
      Доступны следующие команды:

      /ask - дать трактовку раскладку. После команды на отдельных строках нужно ввести:

      Расклад
      Тема расклада (любовь финансы)
      Информация о вопрошающем (девушка, старик, мальчик)
      Выпавшие карты
      Вопрос
      
      Будет дан ответ в следующем виде
      
      1) Описание выпавших карт и суммарный вывод
      2) Описание личности человека по картам
      3) Какие вопросы нужно задать себе
      4) Советы для улучшения ситуации.
     
      """
    )

@dp.message(Command("ask-gpt3"))
async def get_tarot_info_gpt_3(message: types.Message):
    logging.info('Get tarot layout interpreatition with GPT-3: %s', message.text)
    await get_tarot_info(message, get_answer_gpt_3)


@dp.message(Command("ask-gpt4"))
async def get_tarot_info_gpt_4(message: types.Message):
    logging.info('Get tarot layout interpreatition with GPT-3: %s', message.text)
    await get_tarot_info(message, get_answer_gpt_4)


async def get_tarot_info(message: types.Message, get_answer_method: callable):
    user_message = message.text

    if not user_message:
        await message.answer(
            "Не удалось совершить операцию: не удалось получить сообщение"
        )
        return

    request_values = user_message.split("\n")

    if len(request_values) != 6:
        await message.answer("Не удалось совершить операцию: недостаточно информации")
        return

    layout, theme, questioner_info, cards, question = request_values[1:]

    try:
        await message.answer(
            "Информация получена! Дождитесь ответа, примерно в течении 1-2 минуты."
        )
        response = await get_answer_method(questioner_info, theme, layout, cards, question)
        logging.info(f'Response is {type(response)} \n {response}')
        chat_gpt_response = response
    except Exception as e:
        chat_gpt_response = f"Извините, произошла ошибка. \n{e}"

    await message.answer(chat_gpt_response)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
