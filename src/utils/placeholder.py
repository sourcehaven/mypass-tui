from src.settings import settings


def placeholder_selector(key: str):
    if settings["placeholders"]:
        match key:
            case "signin_username":
                return "Enter signin username..."
            case "signin_password":
                return "Enter signin password..."
            case "signup_username":
                return "Enter your username..."
            case "signup_password":
                return "Enter your password..."
            case "signup_firstname":
                return "Enter your firstname..."
            case "signup_lastname":
                return "Enter your lastname..."
            case "signup_email":
                return "Enter your email..."
            case "new_username":
                return "..."
            case "new_password":
                return "..."
            case "new_title":
                return ".."
            case "new_website":
                return "..."
            case "new_folder":
                return "..."
            case _:
                return ""
    else:
        return ""
