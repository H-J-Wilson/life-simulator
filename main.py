import os
from urllib.request import urlopen, URLError
import json
import requests
import sys
import time
from datetime import datetime
import csv
import uvicorn
from dashboard import python_dashboard


def main():

    uvicorn.run("webpage:app", host="0.0.0.0", port=8000)

    

if __name__ == "__main__":
    main()
