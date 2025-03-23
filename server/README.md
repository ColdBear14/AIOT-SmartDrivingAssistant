# Running the Python Server

To run the Python server, follow these steps:

1. **Install Dependencies**: Make sure you have Python installed on your machine. You can check this by running `python --version` in your terminal. You also need to install the required packages. You can do this with pip:

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server**: Navigate to the directory where your server's main script is located and run the following command:

   ```bash
   uvicorn app.main:app --host=127.0.0.1 --port=8000 --reload
   ```

   This will start the server on `http://127.0.0.1:8000` and enable auto-reloading.