"""JSON handler"""
import json
import pkgutil
from jsonschema import validate, exceptions
from .. import base, error


class JSONHandler(base.Base):
    """JSON handler"""
    json_schema = {
        'POST': None,
        'PUT': None
    }
    def get_json_schema(self, method):
        return self.json_schema[method]

    def prepare(self):
        """Incorporate request JSON into arguments dictionary"""
        if self.request.method in {'PUT', 'POST'}:
            if self.request.body:
                try:
                    if self.get_json_schema(self.request.method) is None:
                        json_data = json.loads(
                            self.request.body.decode('utf-8')
                        )
                    else:
                        json_data = self.validated_json(
                            self.request.body.decode('utf-8'),
                            self.get_json_schema(self.request.method)
                        )
                    for k, v in json_data.items():
                        # Tornado expects values in the argument dict to be
                        # lists. in tornado.web.RequestHandler._get_argument
                        # the last arguments is returned.
                        json_data[k] = v
                        self.request.arguments.update(json_data)
                except error.BaseError as exc:
                    if self.debug_api:
                        self.logger.exception(exc)
                    self.send_error(
                        status_code=exc.http_status, json_error=exc
                    )

    def set_default_headers(self):
        """Set header to JSON"""
        self.set_header('Content-Type', 'application/json')

    def output(self, data):
        """output data"""
        self.write(json.dumps(data))

    @staticmethod
    def validated_json(msg, schema_pkgfile, decode=True):
        """Validate a message txt against a JSON schema file.
        Return the validated JSON or throw jsonchema exception.
        """
        if decode:
            try:
                msg_json = json.loads(msg)
            except ValueError:
                raise error.ValidationError(
                    msg='Not a valid JSON'
                )
        else:
            msg_json = msg
        validator = json.loads(pkgutil.get_data(*schema_pkgfile).decode('utf-8'))
        try:
            validate(msg_json, validator)
        except exceptions.ValidationError as exc:
            raise error.ValidationError(msg=exc.message)
        return msg_json

    def handle_error(self, exc):
        """Error handler routine"""
        if self.debug_api:
            self.logger.exception(exc)
        if exc.http_status != 200:
            self.set_status(exc.http_status)
            self.write_error(exc.http_status)
        else:
            self.write(
                json.dumps(
                    {
                        'status': exc.error_code,
                        'output': exc.construct_msg()
                    }
                )
            )
