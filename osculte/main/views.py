from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from accounts.forms import CustomUserCreationForm

from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
import random
from .models import Review, Message, BoiteDeReception,envoyer_message
from .forms import MessageForm
from django.db.models import Q
from django.db.models import Max





def index(request):
    form = CustomUserCreationForm(request.POST, request.FILES)
    return render(request, 'main/index.html', context={"form":form})

@login_required
def all_users(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')  # Récupérez l'ID du destinataire depuis le formulaire
        # Redirigez l'utilisateur vers la page d'envoi de message avec le recipient_id
        return redirect('envoyer_message', recipient_id=recipient_id)
    else:
        users = list(CustomUser.objects.exclude(id=request.user.id))
        random.shuffle(users)  # Exclure l'utilisateur connecté
        return render(request, 'main/all_users.html', {'users': users})
    
def news(request):
    reviews = Review.objects.all().order_by("-created_at")  # Récupère tous les messages.
    return render(request, 'main/news.html', {"reviews": reviews})

# La vue pour ajouter un message (bio).
@login_required
def ajouter_news(request):
    if request.method == "POST":
        bio = request.POST.get('bio')
        color = request.POST.get("color")
        user = request.user
        Review.objects.create(user=user, bio=bio, color=color)
        return redirect('news')
    return render(request, "main/ajouter_news.html")

# La vue pour supprimer un message (bio).
@login_required
def delete_news(request, pk):
    review = Review.objects.get(pk=pk)
    
    # Vérifie si l'utilisateur actuel est le propriétaire du message avant de supprimer.
    if review.user == request.user:
        review.bio = ""
        review.save()
    
    return redirect('news')



@login_required
def delete_message(request, pk):
    message = Message.objects.get(pk=pk)
    
    # Vérifie si l'utilisateur actuel est le propriétaire du message avant de supprimer.
    if message.user == request.user:
        message.bio = ""
        message.save()
    
    return redirect('message')






login_required
def delete_conversation(request, pk):
    # Récupérer le message à supprimer
    message = envoyer_message.objects.get(pk=pk)
    
    # Vérifier si l'utilisateur actuel est le propriétaire du message avant de supprimer.
    if message.sender == request.user:
        # Effacer le contenu du message
        message.content = ""
        message.save()
    
    # Rediriger vers la vue 'conversation' avec l'argument 'recipient_id'
    return redirect('conversation', kwargs={'sender_id': message.sender.id})







@login_required
def profil(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'main/profil.html', {'user': user})


@login_required
def message(request):
    if request.method == "POST":
        bio = request.POST.get('bio')
        user = request.user
        Message.objects.create(user=user, bio=bio)
        
    # Récupérez les messages existants après les avoir créés ou en dehors du bloc POST.
    messages = Message.objects.all().order_by("-created_at")
    
    return render(request, 'main/message.html', {"messages": messages})





# Dans votre vue boite_reception
@login_required
def conversation(request, recipient_id):
    recipient = get_object_or_404(CustomUser, id=recipient_id)
    
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            envoyer_message.objects.create(content=content, sender=sender, recipient=recipient)
            return redirect('conversation', recipient_id=recipient_id)
    else:
        form = MessageForm()

    messages = envoyer_message.objects.filter(sender=request.user, recipient=recipient).order_by("-created_at") | envoyer_message.objects.filter(sender=recipient, recipient=request.user).order_by("-created_at")
    
    return render(request, "main/conversation.html", {"recipient": recipient, "form": form, "messages": messages})



@login_required
def boite_reception(request):
    user = request.user

    # Récupérez tous les utilisateurs avec lesquels l'utilisateur a eu une conversation (envoyé ou reçu un message)
    users_with_messages = CustomUser.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct()

    # Mettez à jour la date du dernier message pour chaque utilisateur dans la boîte de réception
    for user_with_messages in users_with_messages:
        boite_de_reception, created = BoiteDeReception.objects.get_or_create(user=user_with_messages)
        last_message_date = envoyer_message.objects.filter(
            Q(sender=user, recipient=user_with_messages) | Q(sender=user_with_messages, recipient=user)
        ).aggregate(Max('created_at'))['created_at__max']
        user_with_messages.boitedereception.last_message_date = last_message_date
        user_with_messages.boitedereception.save()

    # Tri des utilisateurs en fonction de la date du dernier message
    users_with_messages = users_with_messages.order_by('-boitedereception__last_message_date')
    return render(request, 'main/boite_reception.html', {'users_with_messages': users_with_messages})


