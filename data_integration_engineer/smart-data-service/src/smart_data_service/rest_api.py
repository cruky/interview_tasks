import decimal

import flask_restful
import flask_restful.reqparse
from flask import Flask, json, jsonify
from pydantic import ValidationError

from src.smart_data_service.config import API_PORT
from src.smart_data_service.db_operations import DbSession
from src.smart_data_service.schemas import SmartDataQuery

app = Flask(__name__)
api = flask_restful.Api(app)


class DecimalEncoder(json.JSONEncoder):
    """Convert decimal instances to strings."""

    def default(self, o):
        """convert decimal values to string"""
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)


app.json_encoder = DecimalEncoder


class SmartDataAPI(flask_restful.Resource):
    """With get request return requested smart data measurements"""

    def __init__(self):
        self.parser = flask_restful.reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("smart_meter_id", type=int, required=True, help="Invalid data: {error_msg}")
        self.parser.add_argument("start_date", type=str, required=True, help="Invalid data: {error_msg}")
        self.parser.add_argument("end_date", type=str, required=True, help="Invalid data: {error_msg}")
        super().__init__()

    def get(self):
        """Return requested smart data measurements"""
        args = self.parser.parse_args()
        try:
            smart_data = SmartDataQuery(**args)
            with DbSession() as session:
                results = session.query_smart_data_w_time_range(
                    smart_data.smart_meter_id,
                    smart_data.start_date,
                    smart_data.end_date,
                )
                return jsonify([record._asdict() for record in results])

        except ValidationError as error:
            return flask_restful.abort(400, message=error.errors())


api.add_resource(SmartDataAPI, "/smart_meter")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=API_PORT)  # on the server
    # TODO: When running publicly rather than in development, you should not use the built-in development server .
    #  The development server is provided by Werkzeug for convenience,
    #  but is not designed to be particularly efficient, stable, or secure.
