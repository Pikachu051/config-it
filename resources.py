from netmiko import ConnectHandler


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "You didn't say anything!"
    elif lowered == '!connect':

