from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('APPWRITE_API_KEY')
project_id = os.getenv('APPWRITE_PROJECT_ID')
database_id = os.getenv('APPWRITE_DATABASE_ID')
collection_id = os.getenv('APPWRITE_COLLECTION_ID')

client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project(project_id)
client.set_key(api_key)

database = Databases(client)

def createNewAnswer(id, answer):
    database.create_document(
        database_id,
        collection_id,
        document_id=id,
        data=answer
    )
