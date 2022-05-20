class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class JobAlreadyExistsError(Exception):
    pass

class UpdatingJobError(Exception):
    pass

class DeletingJobError(Exception):
    pass

class JobNotExistsError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "JobAlreadyExistsError": {
         "message": "Job with given id already exists",
         "status": 400
     },
     "UpdatingJobError": {
         "message": "Updating Job added by other is forbidden",
         "status": 403
     },
     "DeletingJobError": {
         "message": "Deleting Job added by other is forbidden",
         "status": 403
     },
     "JobNotExistsError": {
         "message": "Job with given id doesn't exists",
         "status": 400
     }
}