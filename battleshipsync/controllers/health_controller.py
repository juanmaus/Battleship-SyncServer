from battleshipsync import app, redis_store
from flask import jsonify
from http import HTTPStatus


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


@app.route('/api/v1/redis_status', methods=['GET'])
def get_redis_status():
    """
        in order to check current REDIS status, we will submit some data and then 
        we will try to retrieve it just to verify we can successfully create a 
        connection with the REDIS Store.
        :return: JSON object with result 
    """
    # First we save some data to a given key
    redis_store.set("Battleship Version", "v1")
    redis_store.set("Battleship Stack", "Python + Flask + REDIS + MongoDB")

    # Now we retrieve the data

    result = {
        "Battleship Version": redis_store.get("Battleship Version"),
        "Stack": redis_store.get("Battleship Stack"),
        "Redis Status": "OK"
    }
    return jsonify(result), int(HTTPStatus.OK)
