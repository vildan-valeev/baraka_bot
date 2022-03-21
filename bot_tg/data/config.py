from environs import Env

DEBUG = True

if DEBUG:
    env = Env()
    env.read_env(".env.dev", recurse=False)
else:
    env = Env()
    env.read_env()

ADMINS = env.list("ADMINS")
TG_TOKEN = env.str("TG_TOKEN")

