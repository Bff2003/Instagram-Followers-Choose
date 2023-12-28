import sys
import os
import logging
import argparse
from selenium import webdriver
from Instagram import Instagram
import pickle
import json
from Session import Session
import traceback
# uuid
import uuid

class Main:
    def __init__(self, followers: set[str], following: set[str], last_session_file=None) -> None:
        self.__setLogger()
        self.__logger.info("Starting...")  
        self.__logger.info("Loading session...")  
        if last_session_file != None: # Load session from file
            self.__logger.info("Loading session from file: " + last_session_file)
            self.__session = Session(last_session_file)
        else: # Create new session
            self.__logger.info("Creating new session...")
            self.__session = Session()
            self.__session.create_new_session(not_following=Main.not_following(following, followers), not_following_back=Main.not_following_back(following, followers), mutual=Main.mutual(following, followers))
            self.__session.save_session()
        self.__logger.info("Session created")

        # self.__logger.info("Loading Instagram...")
        # options = webdriver.EdgeOptions()
        # self.__driver = webdriver.Edge(options=options)
        # self.__instagram = Instagram(self.__driver)
        # self.__logger.info("Instagram loaded")

    def __setLogger(self) -> None:
        self.__logger = self.create_logger(__name__)
    
    def create_logger(self, name: str) -> logging.Logger:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        return logger

    def not_following_back(following: set[str], followers: set[str]) -> list[str]:
        """Identify users you're following but who don't follow you back."""
        return set(following - followers)

    def not_following(following: set[str], followers: set[str]) -> list[str]:
        """Identify users following you whom you're not following back."""
        return set(followers - following)

    def mutual(following: set[str], followers: set[str]) -> list[str]:
        """Identify users you're following and who are following you back."""
        return set(followers.intersection(following))

    def get_all_users(following: set[str], followers: set[str]) -> list[str]:
        """Get the union of followers and following."""
        return set(followers.union(following))

    def start_processing(self) -> None: 
        print("Not following back: " + str(len(self.__session.get_unprocessed()["not_following_back"])))
        for user in self.__session.get_unprocessed()["not_following_back"]:
            option = self.user_questionary(user, pre_text="Not following back:")
            self.process_user(user, option, "followers")
            self.__session.get_unprocessed()["not_following_back"].remove(user)
        
        print("Not following: " + str(len(self.__session.get_unprocessed()["not_following"])))
        for user in self.__session.get_unprocessed()["not_following"]:
            self.user_questionary(user, pre_text="Not following:")
            self.process_user(user, option, "following")
            self.__session.get_unprocessed()["not_following"].remove(user)

        
        print("Mutual: " + str(len(self.__session.get_unprocessed()["mutual"])))
        for user in self.__session.get_unprocessed()["mutual"]:
            i = 0
            option1 = self.user_questionary(user, pre_text="For following:")
            if option1 == "quit":
                self.save_session()
                sys.exit(0)
            
            if option1 == "best_friends":
                self.__session.get_processed()["best_friends"].append(user)
                self.__session.get_unprocessed()["mutual"].remove(user)
                continue
            
            i += 1
            option2 = self.user_questionary(user, pre_text="For followers:", allow_best_friend=False)

            if i == 2:
                self.process_user(user, option1, "following")
                self.process_user(user, option2, "followers", allow_best_friend=False)
                
            
    def process_user(self, user: str, option: str, type_user: str, allow_best_friend = True) -> None:
        if option == "keep":
            self.__session.get_processed()[type_user]["keep"].append(user)
        elif option == "remove":
            self.__session.get_processed()[type_user]["remove"].append(user)
        elif option == "skip":
            pass
        elif option == "best_friends" and allow_best_friend:
            self.__session.get_processed()["best_friends"].append(user)
        elif option == "quit":
            sys.exit(0)
        else:
            raise ValueError("Invalid option")

    def user_questionary(self, user: str, pre_text: str = None, allow_best_friend = True) -> str:
        while True:
            if pre_text != None:
                print(pre_text)
            print("User: " + user)
            print("Options:")
            print("- \"K\" to keep this user")
            print("- \"R\" to remove this user")
            print("- \"S\" to skip this user")
            if allow_best_friend:
                print("- \"B\" to add this user to your \"Best Friends\" list")
            print("- \"Q\" to quit the script")
            option = input("Option: ").upper()
            options_out = {"K": "keep", "R": "remove", "S": "skip", "B": "best_friends", "Q": "quit"}
            if (option != "Q" and option != "S" and option != "B" and option != "K" and option != "R"):
                print("Invalid option")
            elif option == "B" and not allow_best_friend:
                print("Invalid option")
            else:
                return options_out[option]
    
    def get_session(self):
        return self.__session
        
if __name__ == "__main__":
    
    main = None
    try:
        argparse = argparse.ArgumentParser()
        argparse.add_argument("-F", "--followers-path", help="Followers file path")
        argparse.add_argument("-f", "--following-path", help="Following file path")
        argparse.add_argument("-s", "--session-file", help="""Session file path. If this argument is passed, the program will load the session from the file and will not process the followers and following files.""")
        args = argparse.parse_args()

        # create folder sessions if not exists
        if not os.path.exists("sessions"):
            os.makedirs("sessions")
        
        with open(args.followers_path, "r") as followers:
            followers = followers.readlines()
            followers = [x.strip() for x in followers]
            followers = set(followers)
        with open(args.following_path, "r") as following:
            following = following.readlines()
            following = [x.strip() for x in following]
            following = set(following)
        
        main = Main(followers, following, last_session_file=args.session_file)

        main.start_processing()
        
    except (Exception, KeyboardInterrupt) as e:
        if main != None:
            main.get_session().save_session()
        
        if isinstance(e, KeyboardInterrupt):
            sys.exit(0)
        
        print(e)
        traceback.print_exc()
        sys.exit(1)