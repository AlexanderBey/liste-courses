from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q


from .models import ListeCourses, Article
from .forms import ListeForm, ArticleForm, RegisterForm

@login_required
def home(request):
    # Liste des listes où l'utilisateur est soit le créateur, soit membre
    listes = ListeCourses.objects.filter(
        Q(utilisateur= request.user) | Q(membres=request.user)
    ).distinct() # distinct() évite les doublons si un user est à la fois créateur et membre
    
    return render(request, 'home.html', {'listes': listes})


@login_required
def creer_liste(request):
    form = ListeForm(request.POST or None)  # ← astuce très pratique

    if form.is_valid():
        liste = form.save(commit=False)
        liste.utilisateur = request.user
        liste.save()
        return redirect('detail_liste', pk=liste.pk)

    return render(request, 'creer_liste.html', {'form': form})

@login_required
def detail_liste(request, pk):
    liste = get_object_or_404(
        ListeCourses,
        Q(utilisateur=request.user) | Q(membres=request.user),
        pk=pk
    )
    
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.liste = liste
            article.save()
            return redirect('detail_liste', pk=pk)

    else:
        form = ArticleForm()
    return render(request, 'detail_liste.html', {'liste': liste, 'form': form})

@login_required 
def toggle_achete(request, pk):
    article = get_object_or_404(Article, pk=pk, liste__utilisateur=request.user)
    article.achete = not article.achete
    article.save()
    return redirect('detail_liste', pk=article.liste.pk)


@login_required
def supprimer_liste(request, pk):
    liste = get_object_or_404(ListeCourses, pk=pk, utilisateur=request.user)
    liste.delete()
    return redirect('home')

@login_required
def supprimer_article(request, pk):
    article = get_object_or_404(Article, pk=pk, liste__utilisateur=request.user)
    liste_pk = article.liste.pk
    article.delete()
    return redirect('detail_liste', pk=liste_pk)

@login_required
def rejoindre_par_code(request):
    if request.method == 'POST':
        code = request.POST.get('share_code', '').strip().upper()
        if not code:
            messages.error(request, "Entre un code")
            return redirect('home')
        try:
            liste = ListeCourses.objects.get(share_code=code)
        except ListeCourses.DoesNotExist:
            messages.error(request, f"Aucun code trouvé: {code}")
            return redirect('home')

        if request.user == liste.utilisateur:
            messages.info(request,"C'est ta liste")
        elif request.user in liste.membres.all():
            messages.info(request, "T'est déjà dedans !")
        else: 
            liste.membres.add(request.user)
            messages.success(request, f"Tu as rejoint « {liste.nom} » ! 🛒")
        
        return redirect('detail_liste', pk=liste.pk)
    
    return redirect('home')

    
def register(request):
    form = RegisterForm(request.POST or None)   # ← astuce élégante
    
    if form.is_valid():
        user = form.save()
        login(request, user) #connexion automatique après inscription
        messages.success(request, f"Compte crée ! Bienvenue {user.username} 🎉")
        return redirect('home')

    return render(request, 'register.html', {'form': form})