# Hospital LLM

This project is designed to run tests using various LLMs and embedding models on a given document. The results are saved in a JSON file.

## Prerequisites

- Python 3.8 or higher
- Install the required packages using `pip install -r requirements.txt`
- Ensure you have the necessary environment variables set in a `.env` file

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

1. Create the ChromaDB instances:

   ```sh
   python vectordb.py
   ```

2. Run the tests:

   ```sh
   python main.py
   ```

3. Check the results in the `results.json` file.

## Project Structure

- `data.py`: Contains the data for the tests.
- `vectordb.py`: Functions to create and load ChromaDB instances.
- `logger.py`: Simple colored logging function.
- `main.py`: Main script to run the tests.
- `.env`: Environment variables.
- `requirements.txt`: List of dependencies.
