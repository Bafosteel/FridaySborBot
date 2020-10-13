import requests
import vk_api

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

def auth():
    try:
        a = requests.get(
            'https://oauth.vk.com/access_token?client_id=6343109&client_secret=7SvmbSHf76wegBc8py7i&v=5.122&grant_type=client_credentials')
        vks = vk_api.VkApi('artemmas.96@mail.ru','BaFostEel25RANDOMIZE', auth_handler=auth_handler, app_id=6343109,
                           scope='message,messages,wall')
        vks.auth()
    except vk_api.AuthError as ex:
        print(ex.args[0])
    return vks

'''
vk_session = auth()
vk = vk_session.get_api()
params={"user_id":109340787,"v":"5.21","random_id":189525742,"peer_id":109340787,"message":"test",'access_token':'d57e2e5571d6606cc8818a6b4b206410807de6633988581f430a636a07e96598d8359d1919d4f268b6de9'}
print(vk.messages.send)

b = requests.get('https://api.vk.com/method/messages.send',params=params)
print(b.json())
'''