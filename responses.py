def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hi"):
        return "Hi!"
    if user_message in ("who is the prettiest boy?"):
        return "Luca is!"

    return "I don't understand"


