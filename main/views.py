from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from .utils import video_infos, get_video, get_audio
import os
import requests

# Status codes and messages
codes = {
    # Informational.
    100: ("continue",),
    101: ("switching_protocols",),
    102: ("processing",),
    103: ("checkpoint",),
    122: ("uri_too_long", "request_uri_too_long"),
    200: ("ok", "okay", "all_ok", "all_okay", "all_good", "\\o/", "✓"),
    201: ("created",),
    202: ("accepted",),
    203: ("non_authoritative_info", "non_authoritative_information"),
    204: ("no_content",),
    205: ("reset_content", "reset"),
    206: ("partial_content", "partial"),
    207: ("multi_status", "multiple_status", "multi_stati", "multiple_stati"),
    208: ("already_reported",),
    226: ("im_used",),
    # Redirection.
    300: ("multiple_choices",),
    301: ("moved_permanently", "moved", "\\o-"),
    302: ("found",),
    303: ("see_other", "other"),
    304: ("not_modified",),
    305: ("use_proxy",),
    306: ("switch_proxy",),
    307: ("temporary_redirect", "temporary_moved", "temporary"),
    308: (
        "permanent_redirect",
        "resume_incomplete",
        "resume",
    ),  # "resume" and "resume_incomplete" to be removed in 3.0
    # Client Error.
    400: ("bad_request", "bad"),
    401: ("unauthorized",),
    402: ("payment_required", "payment"),
    403: ("forbidden",),
    404: ("not_found", "-o-"),
    405: ("method_not_allowed", "not_allowed"),
    406: ("not_acceptable",),
    407: ("proxy_authentication_required", "proxy_auth", "proxy_authentication"),
    408: ("request_timeout", "timeout"),
    409: ("conflict",),
    410: ("gone",),
    411: ("length_required",),
    412: ("precondition_failed", "precondition"),
    413: ("request_entity_too_large",),
    414: ("request_uri_too_large",),
    415: ("unsupported_media_type", "unsupported_media", "media_type"),
    416: (
        "requested_range_not_satisfiable",
        "requested_range",
        "range_not_satisfiable",
    ),
    417: ("expectation_failed",),
    418: ("im_a_teapot", "teapot", "i_am_a_teapot"),
    421: ("misdirected_request",),
    422: ("unprocessable_entity", "unprocessable"),
    423: ("locked",),
    424: ("failed_dependency", "dependency"),
    425: ("unordered_collection", "unordered"),
    426: ("upgrade_required", "upgrade"),
    428: ("precondition_required", "precondition"),
    429: ("too_many_requests", "too_many"),
    431: ("header_fields_too_large", "fields_too_large"),
    444: ("no_response", "none"),
    449: ("retry_with", "retry"),
    450: ("blocked_by_windows_parental_controls", "parental_controls"),
    451: ("unavailable_for_legal_reasons", "legal_reasons"),
    499: ("client_closed_request",),
    # Server Error.
    500: ("internal_server_error", "server_error", "/o\\", "✗"),
    501: ("not_implemented",),
    502: ("bad_gateway",),
    503: ("service_unavailable", "unavailable"),
    504: ("gateway_timeout",),
    505: ("http_version_not_supported", "http_version"),
    506: ("variant_also_negotiates",),
    507: ("insufficient_storage",),
    509: ("bandwidth_limit_exceeded", "bandwidth"),
    510: ("not_extended",),
    # Templates folder
    511: ("network_authentication_required", "network_auth", "network_authentication"),
}


path = os.path.join(os.path.dirname(__file__), "templates")


# Homepage
def home(request):
    response = HttpResponse(render(request, os.path.join(path, "home.html")))
    host = request.META.get("HTTP_HOST", "")
    response["Access-Control-Allow-Origin"] = f"http://{host}"
    return response


# About
def about(request):
    return render(request, os.path.join(path, "about.html"))


# Contact
def contact(request):
    return render(request, os.path.join(path, "contact.html"))


# video info
def video_info(request):
    if request.method == "POST":
        url = request.POST.get("url", None)
        if url:
            info = video_infos(url)
            return JsonResponse(info)

    return HttpResponse("", status_code=401)


def download_video(request):
    if request.method == "GET":
        url = request.GET.get("url")
        resolution = request.GET.get("res")
        if url and resolution:
            video = get_video(url, resolution, "mp4")
            url = video.url
            r = requests.get(url, stream=True)

            def generate():
                try:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            yield chunk
                except Exception as e:
                    print("Error :", e)
                finally:
                    r.close()

            response = StreamingHttpResponse(generate(), content_type="video/mp4")
            response["Content-Disposition"] = f"attachment; filename={video.title}.mp4"
            response["Content-Length"] = str(video.filesize)
            return response
        else:
            return
    else:
        return HttpResponse("Method Not Allowed", status_code=405)


def download_audio(request):
    if request.method == "GET":
        url = request.GET.get("url")
        if url:
            audio = get_audio(url, "mp3")
            if audio:
                url = audio.url
                r = requests.get(url, stream=True)

                def generate():
                    try:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                yield chunk
                    except Exception as e:
                        print("Error :", e)
                    finally:
                        r.close()

                response = StreamingHttpResponse(generate(), content_type="audio/mpeg")
                response[
                    "Content-Disposition"
                ] = f"attachment; filename={audio.title}.mp3"
                response["Content-Length"] = str(audio.filesize)
                return response
        else:
            return "Please include the url to download"
    else:
        return HttpResponse("Method Not Allowed", status_code=405)


def custom_exception_handler(request, exception):
    if exception:
        print(exception)

    status_code = 500
    if isinstance(exception, HttpResponse):
        status_code = exception.status_code()
    elif hasattr(exception, "status_code"):
        status_code = exception.status_code()
    return reverse("custom_error_handler", kwargs={"status_code": status_code})


def custom_error_handler(request, status_code):
    message = codes[status_code][0]
    context = {"error_code": status_code, "error_message": message}
    return render(request, os.path.join(path, "errors.html"), context=context)
