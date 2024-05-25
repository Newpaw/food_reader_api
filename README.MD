# Food Analysis Application

## Overview

This is the first version of a food analysis application which detects food items in an image and provides information about their caloric, fat, sugar, and protein content. This version is still under development, and we plan to add more features like user management in the future.

## Features

- **Image Analysis:** Analyzes images to detect food items.

- **Nutritional Information:** Provides caloric, fat, sugar, and protein content for the detected food items.

## Getting Started

### Requirements

- [Docker](https://www.docker.com/products/docker-desktop)

- [Docker Compose](https://docs.docker.com/compose/install/)

### Instructions
1. **Clone the Repository**

    ```sh

    git clone <repository-url>

    cd <repository-directory>

    ```

2. **Docker Configuration**

    Ensure you have Docker Compose installed and Docker running.

    Create a `.env` file in the `backend` directory with the following content:

    ```env

    OPENAI_API_KEY=your_openai_api_key_here

    ASSISTANT_ID=asst_EUXQgAVcCLLJ3F0i0bx1SKJs

    LOG_LEVEL=

    DATABASE_URL=postgresql+psycopg2://user:psw@postgres:5432/postgres