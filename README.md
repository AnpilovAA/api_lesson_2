# Terminal with VKontakte API: 


## In this project I made a terminal that works with the VKontakte API

![Card](https://s12.gifyu.com/images/SZp4k.gif)

## Shorten link
Receives a token and URL, sends a get request and returns a short URL. 

## Count clicks
Receives a token and URL, sends a get request and returns the number of clicks on the link.

## Is shorten link
Checks whether the received URL is short?

# Installation guide

### First step clone this project
 ```git clone https://github.com/AnpilovAA/api_lesson_2```

### Second step install virtual environment

For Windows

 ```py -m venv env``` 

For Unix or MacOS

```python3 -m venv env```

### Third step activate virtual environment

For Windows

```path\to\env\Scripts\activate```

For Unix or MacOS

```source path/to/env/bin/activate```

### Fourth step install dependencies

For Windows

```py -m pip install -r requirement.txt```

For Unix/Linux you have to install pip
https://pip.pypa.io/en/stable/installation/#

```python -m pip install -r requirements.txt```

### Fifth step dependency file
- create a .env file
- create in to .env 1 globals variable
- `VK_TOKEN="Your token VK API"`
### Sixth step launch the program

For Windows

```py main.py```

For Unix or MacOS

```python3 main.py```