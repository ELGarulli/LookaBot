def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hi"):
        return "Hi!"
    if user_message in ("who is the prettiest boy?"):
        return "Luca is!"

    if user_message in ("deuteranopia"):
        defect = "d"
        return defect
    if user_message in ("protanopia"):
        defect = "p"
        return defect
    if user_message in ("tritanopia"):
        defect = "t"
        return defect

    return "I don't understand"
