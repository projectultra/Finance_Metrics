# Stock Prediction Web Application

This is a web application built with Django that fetches live stock data, processes the data, and predicts stock prices using a TensorFlow Keras model.

## Description

The Stock Prediction Web Application allows users to access real-time stock data and obtain predictions for specific stocks. The application fetches live stock data from an API, preprocesses the data, and utilizes a trained TensorFlow Keras model to make predictions. The predicted stock prices are then displayed to the user on a webpage.

## Features

- Fetches live stock data from an API
- Preprocesses the data for model input
- Imports a trained TensorFlow Keras model for stock price prediction
- Displays predicted stock prices on a webpage

## Technologies Used

- Python
- Django
- TensorFlow
- Keras
- HTML/CSS

## Setup and Installation

To use the project, you have two options:<br>
Deployed Version<br>
The project is deployed to Azure using a CI/CD pipeline with GitHub Actions. You can access the deployed version by going to the site https://financemetrics.azurewebsites.net/. Please note that due to usage of the free plan, the site may take some time to load initially.

Local Installation<br>
1. Clone the repository:

```sh
git clone https://github.com/projectultra/Finance_Metrics.git
```

2. Install the required dependencies:

```sh
pip install -r requirements.txt
```

3. Configure the application:

   - Update the API credentials to fetch live stock data.

4. Start the Django development server:

```sh
python manage.py runserver
```

5. Access the web application:

   - Open your web browser and visit `http://localhost:8000` to access the Stock Prediction Web Application.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to contribute to this project. Just follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your modifications.
4. Submit a pull request.

## Authors

- [Jonas Ferrao](https://github.com/projectultra)
