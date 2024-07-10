# Enhancing Patient Data Management in Private Home Care: Developing a Mobile App Prototype for Licensed Physiotherapists in India

## Overview

This project aims to enhance patient data management in private home care by developing a mobile app prototype specifically for licensed physiotherapists in India. The app uses MongoDB for data storage and includes an AI assistant for additional functionality.

## Requirements

1. **MongoDB Account**: To run this project, you need a MongoDB account.
2. **Virtual Environment**: Create a virtual environment (venv) locally for this project.
3. **Python Packages**: Install the required Python packages:
   - `kivymd==1.1.1`
   - `pymongo`
   - `dotenv`
4. **.env File**: Create a `.env` file with your MongoDB credentials.
5. **Docker**: Install Docker to use the AI assistant functionality.
6. **Open Source LLM Model**: Follow the steps to install and run the open-source LLM model from [this link](https://hub.docker.com/r/ollama/ollama). The project uses the `gemma:2b` model by default, but you can change it in the `ai_assistant.py` file.

## Project Setup

### Database Setup

1. **MongoDB Database**: The database used in this project is named `rehab`.
2. **Collections**:
   - `license`: This initial collection contains sample physiotherapist data with license numbers and names.
   - `user_data`: This collection is created after successful account creation.
   - `patient_data`: This collection stores all patient data for later retrieval.

### Installation Steps

1. **Clone the Repository**: Clone the project repository to your local machine.
2. **Create Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install Dependencies**:
    ```bash
    pip install kivymd==1.1.1
    pip install pymongo
    pip install dotenv
    ```
4. **Create .env File**: Create a `.env` file with your MongoDB credentials as shown below:
    ```env
    MONGO_URI=your_mongodb_uri
    ```
5. **Run the Project**: Execute the main script to run the project:
    ```bash
    python main.py
    ```

### AI Assistant Setup

1. **Install Docker**: Make sure Docker is installed on your machine.
2. **Download and Run LLM Model**: Follow the instructions provided in [this link](https://hub.docker.com/r/ollama/ollama) to install and run the open-source LLM model. The project uses the `gemma:2b` model by default.
3. **Modify AI Model (Optional)**: You can change the AI model in the `ai_assistant.py` file to your preferred model.

## Important Notes

- **License Collection**: The initial sample database with license numbers and names is provided in `account_creation.py`. Modify this with real data as required.
- **Login Credentials**: Use the license number and password created during account creation for login. If you forget these, they can be accessed in the `user_data` collection.
- **Patient Data**: All patient data is stored in the `patient_data` collection.

## Summary

This project is designed to facilitate patient data management for licensed physiotherapists in India. By following the setup instructions and ensuring all requirements are met, you can successfully run and utilize the app. The addition of an AI assistant provides enhanced functionality, leveraging modern AI capabilities to further support physiotherapists in their practice.

Feel free to modify and extend the project as per your requirements. If you encounter any issues or have questions, please refer to the documentation or seek assistance from me through my linkedin.
