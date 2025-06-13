from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import predictor_view, predict_image, result_page  # Import views

urlpatterns = [
    path('', predictor_view, name='home'),  # Home page
    path('predict/', predict_image, name='predict'),  # Prediction logic
    path('result/', result_page, name='result_page'),  # Result page
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)