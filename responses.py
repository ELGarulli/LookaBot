def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hi"):
        return "Hi!"

    return "I don't understand"

