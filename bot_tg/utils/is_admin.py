from data.config import ADMINS


def is_admin(tg_id: int) -> bool:
    print(ADMINS, tg_id)
    return True if str(tg_id) in ADMINS else False
