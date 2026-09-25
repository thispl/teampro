"""
Proxy module to allow both:
- teampro.jobpro_export.get_project_for_jobpro
- teampro.api.jobpro_export.get_project_for_jobpro
"""
from teampro.jobpro_export import (
    get_candidates_for_jobpro,
    get_customer_for_jobpro,
    get_project_for_jobpro,
    get_task_opening_for_jobpro,
)

