from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import UploadTSVForm
from .helpers import open_file_and_call_parser
from .models import Tsv


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

        try:
            open_file_and_call_parser(uploaded_file.file_name)
            messages.success(request, "File successfully uploaded")
        except ValueError:
            messages.error(request, "Error: File not recognized")

    return render(
        request, "upload.html", {"form": form, "title": "Upload File"}
    )
