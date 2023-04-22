from http import HTTPStatus

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from services.limiter import Limiter

limiter = Limiter()

service_bp = Blueprint('service', 'service')


@service_bp.route('/ping')
class ServiceMethod(MethodView):
    @service_bp.alt_response(HTTPStatus.TOO_MANY_REQUESTS)
    @service_bp.response(HTTPStatus.OK)
    @limiter.per_second(
        3,
        lambda : request.headers.get('X-Forwarded-For') or request.remote_addr,
    )
    def get(self):
        """Проверка работоспособности сервиса

        Проверка работопособности сервиса, включая rate-limiter
        """

        return {'success': True}
