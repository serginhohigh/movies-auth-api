from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def init_jaeger_tracing(
        app: Flask,
        endpoint_url: str | None = None,
    ) -> None:
    """Отложенный запуск трассировки с помощью OTLP-Jaeger.

    Все переменные, включая адрес и порт OTLP коллектора назначаются
    через переменные окружения.
    """

    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter()),
    )
    trace.get_tracer_provider().add_span_processor(
       BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint_url)),
    )
    FlaskInstrumentor.instrument_app(app)
