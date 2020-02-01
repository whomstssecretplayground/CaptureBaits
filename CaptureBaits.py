import os
import sys
import threading
import time
import logging
import concurrent.futures as cf
from datetime import datetime as dt
from random import randint

import streamlink
import requests

if os.name == "nt":
    SLASH = "\\"
else:
    SLASH = "/"
CWD = os.path.dirname(os.path.realpath(__file__)) + SLASH

LOGGER = logging.getLogger('capturebaits')
LOG_FORMAT = "%(asctime)-15s | %(levelname)s | %(module)s %(name)s %(process)d %(thread)d | %(funcName)20s() - Line %(lineno)d | %(message)s"
LOGGER.setLevel(logging.DEBUG)
STRMHDLR = logging.StreamHandler(stream=sys.stdout)
STRMHDLR.setLevel(logging.INFO)
STRMHDLR.setFormatter(logging.Formatter(LOG_FORMAT))
FLHDLR = logging.FileHandler(f"{CWD}debug.log", mode="a", encoding="utf-8", delay=False)
FLHDLR.setLevel(logging.DEBUG)
FLHDLR.setFormatter(logging.Formatter(LOG_FORMAT))
LOGGER.addHandler(STRMHDLR)
LOGGER.addHandler(FLHDLR)

def uncaught_exceptions(exc_type, exc_val, exc_trace):
    """ injected function to log exceptions """
    import traceback
    if exc_type is None and exc_val is None and exc_trace is None:
        exc_type, exc_val, exc_trace = sys.exc_info()
    LOGGER.exception(f"Uncaught Exception of type {exc_type} was caught: {exc_val}\nTraceback:\n{traceback.print_tb(exc_trace)}")

    try:
        del exc_type, exc_val, exc_trace
    except Exception as excp:
        LOGGER.exception(f"Exception caught during tb arg deletion:\n{excp}")

sys.excepthook = uncaught_exceptions

CAPTURELOCATION = f"{CWD}CAPTURELOCATION{SLASH}"
SLEEPTIME = 300
MODELLIST = []
CAPTURELIST = []
WISHLIST_FILE = f"{CWD}wishlist.txt"
EXECUTOR = cf.ProcessPoolExecutor(max_workers=15)

def print_capturelist():
    LOGGER.info("----------------------------Modellist--------------------------\n\n\n")
    if len(CAPTURELIST) > 0:
        for model in CAPTURELIST:
            LOGGER.info(f"Model: {model}")
    LOGGER.info("\n\n\n----------------------------Modellist--------------------------")

def create_wishlist():
    if not os.path.exists(WISHLIST_FILE) or os.stat(WISHLIST_FILE).st_size == 0:
        open(WISHLIST_FILE, "a+").close()
        #os.chmod(WISHLIST_FILE, 0o666)
        LOGGER.error("Please enter the Modelnames of the Models you would like to capture.")
        LOGGER.error("Will now exit!")
        exit(0)
    return

def thread_cleanup(future):
    LOGGER.debug(f"{future._result}")
    CAPTURELIST.remove(future._result)

def names_from_wishlist():
    LOGGER.info("Starting Process")
    if not os.path.exists(CAPTURELOCATION):
        LOGGER.info("Creating Capture Directory")
        os.mkdir(CAPTURELOCATION)
    with open(WISHLIST_FILE, "r", encoding="utf-8") as wl:
        for model in wl:
            if not model.startswith("#") and not model == "\n":
                model = model.replace("\n", "")
                MODELLIST.append(model)

def bait_models():
    start_date = f"{dt.now().month}_{dt.now().day}_{dt.now().year}"
    for model in MODELLIST:
        if model not in CAPTURELIST:
            LOGGER.info(f"Creating Worker-Process for {model}")
            #time.sleep(randint(0,5))
            future_metadata = {EXECUTOR.submit(
                retrieve_stream, model): model}
            CAPTURELIST.append(model)
            for future, model in future_metadata.items():
                future.add_done_callback(thread_cleanup)
    LOGGER.info("All models submitted")

def retrieve_stream(modelname):
    LOGGER.info(f"{modelname}: Creating Thread")
    modelpage = f"https://en.chaturbate.com/{modelname}/"
    streamurl = None
    resp = requests.get(modelpage)

    for line in resp.text.split("\n"):
        if "m3u8" in line:
            #LOGGER.info(f"LINE:\n{line}")
            streamurl = line.split(".m3u8")[0].split("http")[1]
            streamurl = f"http{streamurl}.m3u8".replace(r"\u002D", "-")
    #LOGGER.info(f"Streamurl: {streamurl}")
    if streamurl is not None:
        try:
            start_date = f"{dt.now().month}_{dt.now().day}_{dt.now().year}"
            start_time = f"{dt.now().hour}_{dt.now().minute}"
            LOGGER.info(f"Perparing Filesystem for Streams from {modelname}")
            modeldir = f"{CAPTURELOCATION}{modelname}{SLASH}"
            if not os.path.exists(modeldir):
                os.mkdir(modeldir)
            filename = f"{modeldir}{modelname}_{start_date}_{start_time}.mp4"
            LOGGER.info(f"Saving stream for {modelname}")
            stream = streamlink.streams(streamurl)["best"]
            with open(filename, "wb") as inputstream:
                with stream.open() as stream_fd:
                    while True:
                        inputstream.write(stream_fd.read(1024))
            LOGGER.info(f"{modelname} is done")
            return modelname
        except Exception as excp:
            LOGGER.exception(f"Thread for {modelname} threw:\n{excp}")
        finally:
            return modelname
    else:
        #LOGGER.debug(f"{modelname} is offline")
        return modelname

def __main__():
    #os.umask(0)
    create_wishlist()
    names_from_wishlist()
    try:
        while True:
            bait_models()
            for num in range(0, int(SLEEPTIME/60))  :
                time.sleep(60)
                print_capturelist()
    except Exception as excp:
        LOGGER.exception(f"{excp}")
    finally:
        pass

if __name__ == "__main__":
    __main__()
