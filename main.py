from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import time
from config import setup_logging, get_db_creds
from url import load_url
from sitemap import load_sitemap
from embed_process import embed_docs
from memory import delete_user_memory
from pymongo import MongoClient
from Chatbot import Chatbot

# Set up logging
logger = setup_logging()

# Set up MongoDB
MONGODB_URI, MONGODB_DB_NAME = get_db_creds()
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

class Urls(BaseModel):
    urls: List[str]

class Sitemap(BaseModel):
    sitemap: str

class Question(BaseModel):
    user_id: str
    message_input: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SupportBudyyX is running..."}

@app.post('/addUrl')
async def process_url(urls: Urls):
    start_time = time.time()
    for url in urls.urls:
        if not db.urls.find_one({'url': url}):
            logger.info(f'Processing {url}...')
            urls_data = load_url([url])
            embed_docs(urls_data)
            db.urls.insert_one({'url': url})
        else:
            logger.info(f'URL {url} already processed')
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000  # convert to milliseconds
    logger.info(f'Successfully handled {urls} in {processing_time:.0f} milliseconds')
    return {'message': 'URLs handled successfully'}

@app.post('/addSiteMap')
async def process_sitemap(sitemap: Sitemap):
    start_time = time.time()
    if not db.sitemaps.find_one({'sitemap': sitemap.sitemap}):
        sitemap_data = load_sitemap(sitemap.sitemap)
        embed_docs(sitemap_data)
        db.sitemaps.insert_one({'sitemap': sitemap.sitemap})
    else:
        logger.info(f'Sitemap {sitemap.sitemap} already processed')
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000  # convert to milliseconds
    logger.info(f'Successfully handled {sitemap.sitemap} in {processing_time:.0f} milliseconds')
    return {'message': 'Sitemap handled successfully'}

@app.post('/askQuestion')
async def process_question(question: Question):
    start_time = time.time()
    try:
        user_id = question.user_id
        message_input = question.message_input

        if not user_id or not message_input:
            raise ValueError('user_id and message_input are required')
        logger.info(f'Received message from user {user_id}')

        chatbot = Chatbot()
        user = chatbot.get_user(user_id)
        if not user:
            chatbot.create_user(user_id)
            user = chatbot.get_user(user_id)
        result = None  # Initialize result to a default value

        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # convert to milliseconds
        result = chatbot.ask_user_question(user_id, message_input)
        logger.info(f'Successfully processed message from user {user_id} in {processing_time:.0f} milliseconds')

        return result
    except ValueError as e:
        logger.error(f'Bad request: {e}')
        raise HTTPException(status_code=400, detail='Bad request')
    except Exception as e:
        logger.error(f'Server error: {e}')
        raise HTTPException(status_code=500, detail='Server error')

@app.post('/deleteUserMemory')
async def process_delete_user_memory(user: Question):
    start_time = time.time()
    try:
        user_id = user.user_id

        if not user_id:
            raise ValueError('user_id is required')
        logger.info(f'Deleting memory of user {user_id}')

        delete_user_memory(user_id)

        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # convert to milliseconds
        logger.info(f'Successfully deleted memory of user {user_id} in {processing_time:.0f} milliseconds')

        return {'message': 'User memory deleted successfully'}
    except ValueError as e:
        logger.error(f'Bad request: {e}')
        raise HTTPException(status_code=400, detail='Bad request')
    except Exception as e:
        logger.error(f'Server error: {e}')
        raise HTTPException(status_code=500, detail='Server error')
