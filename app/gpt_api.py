import multiprocessing
from multiprocessing.pool import AsyncResult
import g4f
import logging

g4f.debug.logging = True  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking

prompt = """
Act as professional tarot reader. Context: person came to you and asked you a question. You give answer through tarot cards.
Questioner info: {0}.
Layout Theme: {1}.
Layout: {2}.
Cards that fell out: {3}.
Question: {4}

You should answer this questions (give answers in Russian):

1. What cards can tell about theme of layout? Analyze relationships between cards (or card itself if there olny one card) and give answer for the questioner's question with information from layout.
2. If there a cards like Knight, Queen, King or Page - analyze characteristics of people that can appear in the future in question's context.
3. Give questions that questioner should ask herself/himself about to solve future problems.
4. Give advices to solve problems and evade trouble in future.

Try your best to get higher tip from questioner.
"""


async def get_answer_gpt_3(questioner_info: str, layout_theme: str, layout: str, cards: str, question: str) -> str:
    """
    Asynchronously gets the answer to a question using GPT-3.

    Args:
        questioner_info (str): Information about the questioner.
        layout_theme (str): The layout theme.
        layout (str): The layout.
        cards (str): The cards.
        question (str): The question.

    Returns:
        str: The answer to the question, or an error message if the response is empty.
    """
    logging.info("Getting answer for question: %s", question)
    messages = [
        {
            "role": "user",
            "content": prompt.format(questioner_info, layout_theme, layout, cards, question),
        }
    ]
    response = await g4f.ChatCompletion.create_async(model=g4f.models.default, messages=messages)
    logging.info("Response: '%s', type: <%s>", response, type(response))
    return response or "Извините, произошла ошибка (система вернула пустой ответ)."


async def get_answer_gpt_4(questioner_info: str, layout_theme: str, layout: str, cards: str, question: str) -> str:
    """
    Generates a function comment for the given function body in a markdown code block with the correct language syntax.

    Args:
        questioner_info (str): The information about the questioner.
        layout_theme (str): The layout theme.
        layout (str): The layout.
        cards (str): The cards.
        question (str): The question.

    Returns:
        str: The generated function comment in a markdown code block with the correct language syntax.
    """

    logging.info("Getting answer for question: %s", question)
    messages = [
        {
            "role": "user",
            "content": prompt.format(questioner_info, layout_theme, layout, cards, question),
        }
    ]
    response = await g4f.ChatCompletion.create_async(model=g4f.models.gpt_4, messages=messages)
    logging.info("Response: '%s', type: <%s>", response, type(response))
    return response


if __name__ == "__main__":
    questioner_info = "девочка"
    layout_theme = "love and relationships"
    layout = "three cards"
    cards = "10 of Cups, Knight of Wands, 3 of Pentacles"
    question = "какие отношения у нас будут в ближайшее время?"
