def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
	resp = "hi"
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        resp = request.args.get('message') + " sup"
    elif request_json and 'message' in request_json:
        resp = request_json['message'] + " yo"
    print(resp)
    return resp
