import os
import sys
import pickle

class Instagram:
    def __init__(self, driver) -> None:
        self.__driver = driver

    def login(self):
        self.__driver.get('https://www.instagram.com/accounts/login/')
        if os.path.exists('cookie.pkl'):
            with open('cookie.pkl', 'rb') as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    self.__driver.add_cookie(cookie)
        else:
            input('Press enter when your login is done')
            with open('cookie.pkl', 'wb') as f:
                pickle.dump(self.__driver.get_cookies(), f)
        raise NotImplementedError

    def open_profile(self, username):
        self.__driver.get(f'https://www.instagram.com/{username}/')

    def unfollow(self, username):
        raise NotImplementedError

    def remove_follower(self, username):
        raise NotImplementedError