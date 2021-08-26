from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import UploadTSVForm
from .models import Tsv
from .parsing_functions import open_file_and_call_parser


@require_http_methods(["POST", "GET"])
@login_required(login_url="/admin/login/")
@user_passes_test(lambda user: user.is_superuser)
def upload_file_view(request):
    """
    Displays form for uploading tsv file. Fetches the uploaded
    file from the database and calls the file reading function
    read_name_and_call_parser

    Args:
        request (): http request

    Returns:
        None
    """

    form = UploadTSVForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = UploadTSVForm()
        uploaded_file = Tsv.objects.get(activated=False)

        uploaded_file.activated = True
        uploaded_file.save()

        open_file_and_call_parser(uploaded_file.file_name)

    return render(
        request, "upload.html", {"form": form, "title": "Upload File"}
    )
