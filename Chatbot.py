from config import setup_logging, get_db
from User import User

# Set up logging
logger = setup_logging()

class Chatbot:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['users']

    def create_user(self, user_id):
        logger.info(f"Creating new user {user_id}.")
        new_user = User(user_id)
        # Save the new user to the database
        self.collection.insert_one({'user_id': user_id})
        return new_user

    def get_user(self, user_id):
        user_data = self.collection.find_one({'user_id': user_id})
        if user_data:
            return User(user_id)
        else:
            logger.info(f"User {user_id} does not exist in database. Creating new user.")
            return self.create_user(user_id)

    def delete_user(self, user_id):
        user_data = self.collection.find_one({'user_id': user_id})
        if user_data:
            # Delete the user's data from the MongoDB database
            self.collection.delete_one({'user_id': user_id})
            logger.info(f"User {user_id} deleted.")
        else:
            logger.error(f"User {user_id} does not exist.")

    def ask_user_question(self, user_id, question):
        user = self.get_user(user_id)
        if user:
            response = user.ask_question(question)
            return response
        else:
            logger.error(f"User {user_id} does not exist.")
