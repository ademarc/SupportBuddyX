## SuppoprtBuddyX - Chatbot for Websites

This project is a web application built using Flask and subsequently migrated to FastAPI. The chatbot application leverages the Langchain library to facilitate a chatbot functionality which can interact with any website by processing its URLs and sitemaps. The chatbot uses OpenAI's GPT-3.5 model for natural language processing and comprehension. The FAISS library is utilized for efficient vector storage and MongoDB is the database of choice for data persistence, effectively storing and retrieving the chatbot's memory.

### Project Structure

The project consists of several Python scripts each serving a distinct purpose:

- `main.py`: This is the primary FastAPI application script, setting up the server and defining the application's routes.

- `Chatbot.py`: This script contains the `Chatbot` class that manages user interactions with the chatbot.

- `embed_process.py`: This script is responsible for embedding and indexing documents for the chatbot.

- `sitemap.py` and `url.py`: These scripts are tasked with loading data from sitemaps and URLs respectively.

- `User.py`: This script contains the `User` class which represents a user interacting with the chatbot.

- `memory.py`: This script is responsible for managing the chatbot's memory, allowing it to recall past user interactions.

- `config.py`: This crucial script manages tasks like loading environment variables, retrieving OpenAI API Key, MongoDB credentials, and setting up logging with both general and error log handlers. It ensures daily rotation of log files and creation of a log directory if one does not exist. It also features a custom formatter class for timestamps in logs, converting time to UTC.

### Installation

Follow these steps to install and run this project:

1. Clone the repository:

```bash
git clone https://github.com/ademarc/supportbuddyx.git
cd supportbuddyx
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Install `libmagic`:

Depending on your OS, you can install `libmagic` using your system's package manager. For Debian-based Linux systems (like Ubuntu), use `apt`:

```bash
sudo apt-get update
sudo apt-get install libmagic1
```

For macOS, use Homebrew:

```bash
brew install libmagic
```

If you're in a Python environment, you might also need to install the `python-magic` package, a Python interface to the `libmagic` file type identification library. Use `pip`:

```bash
pip install python-magic
```

4. Set up your environment variables:

Copy the `.env.sample` file to a new file named `.env` and fill in the required environment variables.

5. Run the application:

```bash
uvicorn main:app
```

The application will start running on `http://127.0.0.1:8000`.

## Usage

The application provides four main endpoints:

- `/addUrl`: This endpoint accepts a POST request with a JSON body containing a list of URLs to be processed by the chatbot.

    Example request:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"urls": ["https://example.com", "https://anotherexample.com"]}' http://127.0.0.1:8000/addUrl
    ```

- `/addSiteMap`: This endpoint accepts a POST request with a JSON body containing a sitemap to be processed by the chatbot.

    Example request:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"sitemap": "https://example.com/sitemap.xml"}' http://127.0.0.1:8000/addSiteMap
    ```

- `/askQuestion`: This endpoint accepts a POST request with a JSON body containing a user ID and a message input. The chatbot will process the message and return a response.

    Example request:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"user_id": "12345", "message_input": "Hello, chatbot!"}' http://127.0.0.1:8000/askQuestion
    ```

- `/deleteUserMemory`: This endpoint accepts a POST request with a JSON body containing a user ID. It will delete the user's memory from the chatbot.

    Example request:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"user_id": "12345"}' http://127.0.0.1:8000/deleteUserMemory
    ```

## Author

This project was created by Marcus Adebayo.

---

### .env.sample

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=langchain
OPENAI_API_KEY=your_openai_api_key
INDEX_STORE=data/indexes/global_index
```

Replace `mongodb://localhost:27017` with your MongoDB URI and `your_openai_api_key` with your OpenAI API key.
