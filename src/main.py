import os
from flask import Flask, request, json
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = app.config['CELERY_BROKER_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(result_backend=app.config['CELERY_BROKER_URL'])

@app.route('/status', methods=['POST'])
def index():
    data = request.args.get('data', '') 
    task = async_task.delay(data)
    return json.jsonify({
        'data': data,
        'task': task.id
    })


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = async_task.AsyncResult(task_id)    
    return json.jsonify(task.as_tuple())

@celery.task(bind=True)
def async_task(self, data):
    if data == 'error':
        raise Error('unexpected error')
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)