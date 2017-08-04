from battleshipsync import app
from flask import jsonify


# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE API
# --------------------------------------------------------------------------
#
@app.route('/', methods=['GET'])
def get_api_root():
    app.logger.info('Server health status summary requested...')
    return jsonify({
        "platform": "Garnet API 1.1",
        "version": "1.0",
        "message": "Server is running",
        "redis-status": "up and running",
        "mongo-status": "up and running"
    })
