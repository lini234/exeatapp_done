from datetime import datetime
from  flask import request


ttl = request.form.get('exeatDate')
print(ttl)
