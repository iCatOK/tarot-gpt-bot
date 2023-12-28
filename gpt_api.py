import g4f

g4f.debug.logging = True  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking

prompt = """
Act as a tarot reader. Context: person came to you and asked you a question. You give answer through tarot cards.
Questioner info: {0}.
Layout Theme: {1}.
Layout: three cards {2}.
Cards that fell out: {3}.
Question: {4}

You should answer this questions (give answers in Russian):

1. What cards can tell about theme of layout? Analyze relationships between cards (or card itself if there olny one card) and give answer for the questioner's question with information from layout.
2. If there a cards like Knight, Queen, King or Page - analyze characteristics of people that can appear in the future in question's context.
3. Give questions that questioner should ask herself/himself about to solve future problems.
4. Give advices to solve problems and evade trouble in future.
"""


async def get_answer(
    questioner_info: str, layout_theme: str, layout: str, cards: str, question: str
):
    return await g4f.ChatCompletion.create_async(
        model=g4f.models.gpt_4,
        provider=g4f.Provider.Liaobots,
        messages=[
            {
                "role": "user",
                "content": prompt.format(
                    questioner_info, layout_theme, layout, cards, question
                ),
            }
        ],
    )


if __name__ == "__main__":
    questioner_info = "девочка"
    layout_theme = "love and relationships"
    layout = "three cards"
    cards = "10 of Cups, Knight of Wands, 3 of Pentacles"
    question = "какие отношения у нас будут в ближайшее время?"
