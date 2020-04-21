import os
import inject


DATABASE_URI = os.getenv('DATABASE_URI')

SERVER_ADRESS = None
SERVER_PORT = None
SERVER_LOG_LEVEL = None
SERVER_WORKER_NUMBERS = None

# override the dictConfig logging in uvicorn. 
# This config add tow FileHandler and update the existing formatter.
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s - %(name)s - %(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s - %(name)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
		"default_file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": "launcher.log",
			"mode": "w",
            "encoding": "utf-8",
        },
		"access_file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": "access.log",
			"mode": "w",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {"handlers": ["default", "default_file"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access", "access_file"], "level": "INFO", "propagate": False},
    },
}


def configure_inject():
	from src.domain.userManagment.service.userService import UserService
	from src.infrastructure.database.models.user import UserQueries

	def config(binder: inject.Binder):
		binder.bind(UserService, UserService(UserQueries()))

	inject.configure(config)