# def tumba(x):
#         return abs(x) * (x + 1) / 2
#
#
#
# print(tumba(1))
# print(tumba(3))
# print(tumba(-3))
# print(tumba(5))


from Pyiiko import IikoServer
import hashlib

# login = '40a629ce'
# password = '40a629ce'
# h_login = hashlib.sha1(bytes(password, encoding='utf-8')).hexdigest()
# print(h_login)
# # i = IikoServer(ip='http://178.214.244.68:80', login='buh', password=h)
# i = IikoServer(ip='https://api-ru.iiko.services/', token=h_login)  # транспорт
# # http://api-delivery.iiko.ru:8080
# i.token()
# print(i.token())


# login = 'Zigman7777@gmail.com'
# password = 'vectra754'

login = 'buh'
password = 'buh'

h_password = hashlib.sha1(bytes(password, encoding='utf-8')).hexdigest()
print(login, h_password)

i = IikoServer(ip='https://baraka-halyal.iiko.it:443', login=login, password=h_password)  # транспорт


print(i.token())
i.quit_token()
