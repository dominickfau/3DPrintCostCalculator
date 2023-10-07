import os

COMPANY_NAME = "DF-Software"
PROGRAM_NAME = "3D Print Cost Calculator"
PROGRAM_VERSION = "1.0.0"


USER_HOME_FOLDER = os.path.expanduser("~")
COMPANY_FOLDER = os.path.join(USER_HOME_FOLDER, "Documents", COMPANY_NAME)
PROGRAM_FOLDER = os.path.join(COMPANY_FOLDER, PROGRAM_NAME)
LOG_FOLDER = os.path.join(PROGRAM_FOLDER, "Logs")
SAVES_FOLDER = os.path.join(PROGRAM_FOLDER, 'Saves')

DATETIME_FORMAT_FILE_SAFE = "%m_%d_%Y - %I-%M %p"
DATETIME_FORMAT = "%m/%d/%Y - %H:%M:%S.%f"


if not os.path.exists(COMPANY_FOLDER):
    os.mkdir(COMPANY_FOLDER)

if not os.path.exists(PROGRAM_FOLDER):
    os.mkdir(PROGRAM_FOLDER)

if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

if not os.path.exists(SAVES_FOLDER):
    os.makedirs(SAVES_FOLDER)