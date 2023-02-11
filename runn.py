import re
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

        listScripts()

    elif (Path('scripts').is_dir() == False):
        print(datetime.now().strftime(
            "[%H:%M:%S]"), " No scripts directory found ", )

        # provide user with y/N option to create directory
        createDirectory = input(
            datetime.now().strftime("[%H:%M:%S]") + " Create scripts directory? (y/N) ")

        if (createDirectory == "y"):
            os.mkdir("scripts")
            print(datetime.now().strftime(
                "[%H:%M:%S]"), " Created scripts directory ", os.getcwd() + "/scripts")

        elif (createDirectory == "N"):
            print(datetime.now().strftime(
                "[%H:%M:%S]"), " No scripts directory found ", )


""" create script file in the scripts directory """


def createScriptFile():

    script_extension = input(
        datetime.now().strftime("[%H:%M:%S]") + " Create script file with .py or .sh extension? (py/sh) ")

    if (script_extension == "py"):
        script_extension = ".py"

    elif (script_extension == "sh"):
        script_extension = ".sh"
        

    # ask user for script name

    script_name = input(
        datetime.now().strftime("[%H:%M:%S]") + " Enter script name: ")

    script_file = open(os.getcwd() + "/scripts" + '/' +
                       script_name + script_extension, "w+")

    script_file.close()


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

    print(datetime.now().strftime("[%H:%M:%S]"),
          f"Starting script '{script_name}' ...")

    start_time = time.perf_counter_ns()

    with open(os.getcwd() + "/scripts" + '/' + script_name + '.sh', 'rb') as file:
        script = file.read()

    rc = call(script, shell=True)

    duration_time = time.perf_counter_ns() - start_time

    print(datetime.now().strftime(
        "[%H:%M:%S]"), f"Finished script '{script_name}' after {duration_time // 1000000} ms ")


""" run python files """


def runPythonScript(script_name):

    print(datetime.now().strftime("[%H:%M:%S]"),
          f"Starting script '{script_name}' ...")

    start_time = time.perf_counter_ns()
    script_name = "/scripts" + "/" + script_name + ".py"
    print(script_name)

    exec(open(os.getcwd() + script_name).read())

    duration_time = time.perf_counter_ns() - start_time

    print(datetime.now().strftime(
        "[%H:%M:%S]"), f"Finished script '{script_name}' after {duration_time // 1000000} ms ")


def runScript(script_name):

    directory = Path("scripts")
    file_name_pattern = "^"+script_name + "\.(txt|sh|py)$"

    matches = file_exists(directory, file_name_pattern)

    if matches:
        print(matches)
        script_name, script_extension = os.path.splitext(matches)

        if (script_extension == ".py"):

            runPythonScript(script_name)

        elif (script_extension == ".sh"):

            runBashScript(script_name)

    else:
        print("Script not found")


def file_exists(directory, file_name_pattern):
    regex = re.compile(file_name_pattern)
    for filename in os.listdir(directory):
        if regex.match(filename):

            return filename
    return False


""" take cli arguments """

cli_arguments = sys.argv

if "create" in cli_arguments:
    createScriptFile()

elif (len(cli_arguments) > 1):

    runScript(cli_arguments[1])

else:
    checkForScriptsDirectory()
