from main import bard;
from user_preferences import get_set_language_choice

BARD_INTRO = "Respond to the prompt as if your name is GereNkap created by monkeyK1n9, you are an expert in finances. You either give advices or generate SQL queries. Don't give explanation, just give the SQL query. Here is the prompt: ";

BARD_OUTRO = "Read this for a non-technical person: "

def handle_response(text: str) -> str:
    request_query = BARD_INTRO + text;

    language = get_set_language_choice(1);
    response_query = bard.get_response(request_query, language=language)

    response_user = bard.get_response(response_query, language=language)
    return response_user