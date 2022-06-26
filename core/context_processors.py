
from threading import Thread
from .models import *
from django.core.mail import EmailMessage
from django.template.loader import *
def sendEmailTosub(news,user):
    template= get_template('newsletter.html').render({
        'news':news,
        'user':user
    })
    email=EmailMessage(
        'News about Nexus',
        template,
        settings.EMAIL_HOST_USER,
        [user.email] #hardd2014  user send email to user email ,email exist in order just type data.shipping_address.email
        )
    try:
        email.fail_silently=False
        email.content_subtype = "html"
        email.send()
        print("send to ",user.email)
        
        
    except Exception as ex:
        print("Error",ex)
        
def sendEmail(request):
    dict={}
    try:
        news=NewsLetter.objects.all()
        sub=Subcribers.objects.all()
        for new in news:
            for user in sub:
                send,created=SendNewsTOSUbcriber.objects.get_or_create(NewsLetter=new,subcriber=user)
                if created:
                    t1=Thread(target=sendEmailTosub,args=(new,user,))
                    t1.daemon=True
                    t1.start()
                    

    except Exception as ex:
        print("ex",ex)
    return dict