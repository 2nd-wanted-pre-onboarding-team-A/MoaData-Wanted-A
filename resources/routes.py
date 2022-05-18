from .views import JobCreatView, JobRetrieveUpdateDeleteView, JobTaskView

def initialize_routes(api):
    api.add_resource(JobCreatView, '/api/v1/jobs')
    api.add_resource(JobRetrieveUpdateDeleteView, '/api/v1/jobs/<int:pk>')
    api.add_resource(JobTaskView, '/api/v1/jobs/<int:pk>/run')
