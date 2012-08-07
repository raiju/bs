from bs.lib import constants, base, util
from repoze.what.predicates import has_permission
from tg import request, expose, url, flash, redirect, response
from bs.widgets.request import request_list, request_object
from bs.model import DBSession, Request, Result, Task
import os


class RequestController(base.BaseController):



    @expose('bs.templates.request')
    def index(self):
        req_data = DBSession.query(Request).all()
        dg = util.to_datagrid(request_list, req_data, "Requests", len(req_data)>0)
        return {'page' : 'requests', 'request_list' : [dg]}


    @expose('json')
    def status(self, task_id):
        t = DBSession.query(Task).filter(Task.task_id == task_id).first()
        if t is None:
            return {'status' : 'PENDING'}
        return {'status' : t.status}

    @expose('json')
    def get(self, task_id):
        req_data = DBSession.query(Request).join(Result).filter(Result.task_id == task_id).first()
        return {'result' : request_object(req_data)}

    @expose('bs.templates.results')
    def result(self, task_id, name=None):
        req_data = DBSession.query(Request).join(Result).filter(Result.task_id == task_id).first()

        if not req_data:
            flash('wrong task identifier : %s' % task_id, 'error')
            raise redirect(url("/"))
        if req_data.result.task is None: status = 'PENDING'
        else :                           status = req_data.result.task.status
        if status == 'SUCCESS':

            out = os.path.join(req_data.result.path, task_id)
            print out

            results = os.listdir(out)
            print results
            if len(results) == 0:
                return 'no result'

            if len(results) == 1:
                name = results[0]
            if name is not None:

                if name in results:
                    ext = os.path.splitext(name)[1]
                    if ext.lower() in ['pdf', 'gz', 'gzip']:
                        response.content_type = 'application/' + ext.lower()
                    elif ext.lower() in ['png', 'jpeg']:
                        response.content_type = 'image/' + ext.lower()
                    else :
                        response.content_type = "text/plain"
                    out_file = os.path.normpath(os.path.join(out, name))
                    print out_file
                    if not out_file.startswith(out):
                        return "Are you kidding me?"
                    return open(out_file).read()

            return {'page' : 'request', 'results' : results, 'linkto' : url('/requests/result', {'task_id' : task_id})}

        elif status == 'FAILURE':
            return req_data.result.task.traceback

        return "Data being processed"

