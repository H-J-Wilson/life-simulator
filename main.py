import os
from urllib.request import urlopen, URLError
import json
import requests
import sys
import time
from datetime import datetime
import csv
from dashboard import python_dashboard
import uvicorn


def main():
    uvicorn.run("webpage:app", host="127.0.0.1", port=8000)
    


if __name__ == "__main__":
    main()
