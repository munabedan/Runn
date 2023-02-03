from pydoc import cli
from subprocess import call
from datetime import datetime
from pathlib import Path
import os
import time
import sys


""" check for script directory """


def checkForScriptsDirectory():
    if (Path('scripts').is_dir() == True):
        print(datetime.now().strftime(
            "[%H:%M:%S]"), " Using directory ", os.getcwd() + "/scripts")

    elif (Path('scripts').is_dir() == False):
        print(datetime.now().strftime(
            "[%H:%M:%S]"), " No scripts directory found ", )


""" list task """


def listScripts():

    print(datetime.now().strftime("[%H:%M:%S]"),
          " Tasks for ", os.getcwd() + "/scripts")

    tasks = os.listdir(os.getcwd()+"/scripts")

    for index, name in enumerate(tasks):

        if (index == (len(tasks)-1)):
            print(datetime.now().strftime(
                "[%H:%M:%S]"), " \u2514\u2500\u2500", tasks[index])

        else:
            print(datetime.now().strftime(
                "[%H:%M:%S]"), " \u251C\u2500\u2500", tasks[index])


""" run bash files"""


def runBashScript(script_name):

    print(datetime.now().strftime("[%H:%M:%S]"), f"Starting script '{script_name}' ...")

    start_time = time.perf_counter_ns()

    with open(os.getcwd() + "/scripts" + '/'+ script_name + '.sh', 'rb') as file:
        script = file.read()

    rc = call(script, shell=True)

    duration_time = time.perf_counter_ns() - start_time

    print(datetime.now().strftime(
        "[%H:%M:%S]"), f"Finished script '{script_name}' after {duration_time // 1000000} ms ")


""" run python files """


def runPythonScript(script_name):

    print(datetime.now().strftime("[%H:%M:%S]"), f"Starting script '{script_name}' ...")

    start_time = time.perf_counter_ns()

    exec(open(os.getcwd() + "/scripts" + "/"+ script_name +".py").read())

    duration_time = time.perf_counter_ns() - start_time

    print(datetime.now().strftime(
        "[%H:%M:%S]"), f"Finished script '{script_name}' after {duration_time // 1000000} ms ")


def runScript(script_name):

    script_name, script_extension = os.path.splitext(script_name)

    if (script_extension == ".py"):

        runPythonScript(script_name)

    elif (script_extension == ".sh"):

        runBashScript(script_name)


""" take cli arguments """

cli_arguments = sys.argv


if "--scripts" in cli_arguments:
    listScripts()

elif (len(cli_arguments) > 1):
    runScript(cli_arguments[1])

else:
    checkForScriptsDirectory()
