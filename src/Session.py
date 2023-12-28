"""{
    "session":{
        "unprocessed": {
            "not_following_back": ["user4", "user5", "user6"],
            "not_following": ["user7", "user8", "user9"],
            "mutual": ["user1", "user2", "user3"]
        },
        "processed": {
            "best_friends": ["user10", "user11", "user12"],
            "following": {
                "keep": ["user1", "user2", "user3"],
                "remove": ["user4", "user5", "user6"]
            },
            "followers": {
                "keep": ["user1", "user2", "user3"],
                "remove": ["user4", "user5", "user6"]
            }
        }
    }
}"""
import os
import json
import uuid

class Session:
    def __init__(self, session_file: str = None) -> None:       
        if session_file == None:
            session_file = "sessions/session-" + str(uuid.uuid4()) + ".json"
            self.__session_file = session_file
            self.__session = self.create_new_session()
        else:
            self.__session_file = session_file
            self.__session = self.load_session(session_file)
    
    def get_session(self):
        return self.__session

    def get_unprocessed(self):
        return self.__session["unprocessed"]

    def get_processed(self):
        return self.__session["processed"]

    def create_new_session(self, not_following_back: list[str] = [], not_following: list[str] = [], mutual: list[str] = []) -> dict:
        self.__session = {
            "unprocessed": {
                "not_following_back": list(not_following_back), 
                "not_following": list(not_following),
                "mutual": list(mutual)
            },
            "processed": {
                "best_friends": [],
                "following": {
                    "keep": [],
                    "remove": []
                },
                "followers": {
                    "keep": [],
                    "remove": []
                }
            }
        }
        # self.save_session()
    
    def load_session(self, session_file: str = None):
        session_file = session_file if session_file != None else self.__session_file
        with open(self.__session_file, "r") as session_file:
            self.__session = json.load(session_file)["session"]
        return self.__session
    
    def save_session(self):
        print("Saving session to file: " + self.__session_file)
        with open(self.__session_file, "w") as f:
            json.dump({"session": self.__session}, f, indent=4)

