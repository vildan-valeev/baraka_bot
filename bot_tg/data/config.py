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
# TG_CHANNEL = env.str("TG_CHANNEL")
# HOST = env("HOST")
# DOMAIN = env.str("DOMAIN")
# TG_CHANNEL_NAME = env.str("TG_CHANNEL_NAME")
# TG_ADMIN_USERNAME = env.str("TG_ADMIN_USERNAME")
# VK_CHANNEL_NAME = env.str("VK_CHANNEL_NAME")
