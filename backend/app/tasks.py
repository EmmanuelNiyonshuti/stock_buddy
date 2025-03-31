"""
Background Tasks Module

This module defines Celery tasks that run in the background. 
"""
from celery import shared_task
from app.services.notification_service import send_sms

@shared_task
def send_sms_task(to, body):
    send_sms(to, body)
