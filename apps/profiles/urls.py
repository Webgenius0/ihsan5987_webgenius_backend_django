from django.urls import path
from .views import ProfileView, MyPostList, MyPostDetail, FAQList, FAQCategoryList, ContactUsList, NotificationSettingView, AppInformationView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my-posts/', MyPostList.as_view(), name='my-posts'),
    path('my-posts/<int:pk>/', MyPostDetail.as_view(), name='my-post-detail'),
    path('faqs/', FAQList.as_view(), name='faq-list'),
    path('faq-categories/', FAQCategoryList.as_view(), name='faq-category-list'),
    path('contact-us/', ContactUsList.as_view(), name='contact-us'),
    path('notifiaction/settings/', NotificationSettingView.as_view(), name='notification-settings'),
    path('app-info/', AppInformationView.as_view(), name='app-info'),
]
