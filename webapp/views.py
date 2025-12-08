from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from .match_utils import check_currency
from .models import UploadHistory
from django.conf import settings

def upload_note(request):
    result = None
    uploaded_image_url = None

    if request.method == "POST" and request.FILES.get("note"):
        uploaded_file = request.FILES["note"]

        # Save uploaded file to MEDIA_ROOT
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Public URL for displaying image
        uploaded_image_url = settings.MEDIA_URL + filename

        # Check if currency is real or fake
        result = check_currency(uploaded_file_path)

        # Save to history database (ImageField handles relative path)
        UploadHistory.objects.create(image=filename, result=result)

    return render(request, "upload.html", {
        "result": result,
        "uploaded_image": uploaded_image_url  # ✅ correct variable for template
    })


def history_page(request):
    # Fetch history with newest first
    history = UploadHistory.objects.all().order_by('-uploaded_at')
    return render(request, "history.html", {"history": history})
