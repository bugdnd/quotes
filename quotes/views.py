import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from .models import Quote, Source, Like
from .forms import QuoteForm


def home(request):
    # Получаем случайную цитату с учетом веса
    quotes = Quote.objects.all()
    if quotes.exists():
        weights = [quote.weight for quote in quotes]
        random_quote = random.choices(quotes, weights=weights)[0]
        random_quote.views_count += 1
        random_quote.save()
        
        # Получаем статистику лайков для цитаты
        likes_count = Like.objects.filter(quote=random_quote, is_like=True).count()
        dislikes_count = Like.objects.filter(quote=random_quote, is_like=False).count()
        
        # Проверяем, голосовал ли пользователь
        user_ip = request.META.get('REMOTE_ADDR')
        user_vote = None
        if user_ip:
            vote = Like.objects.filter(quote=random_quote, ip_address=user_ip).first()
            if vote:
                user_vote = 'like' if vote.is_like else 'dislike'
    else:
        random_quote = None
        likes_count = 0
        dislikes_count = 0
        user_vote = None
    
    context = {
        'quote': random_quote,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_vote': user_vote,
    }
    return render(request, 'quotes/home.html', context)


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Проверяем дубликат
            if Quote.objects.filter(text=form.cleaned_data['text'], 
                                  source=form.cleaned_data['source']).exists():
                messages.error(request, 'Такая цитата уже существует!')
            else:
                # Проверяем лимит цитат для источника
                source_quotes_count = Quote.objects.filter(source=form.cleaned_data['source']).count()
                if source_quotes_count >= 3:
                    messages.error(request, 'У этого источника уже максимальное количество цитат (3)!')
                else:
                    form.save()
                    messages.success(request, 'Цитата успешно добавлена!')
                    return redirect('home')
    else:
        form = QuoteForm()
    
    return render(request, 'quotes/add_quote.html', {'form': form})


def popular_quotes(request):
    # Получаем 10 самых популярных цитат по лайкам
    quotes = Quote.objects.annotate(
        likes_count=Count('like', filter=Q(like__is_like=True))
    ).order_by('-likes_count', '-views_count')[:10]
    
    return render(request, 'quotes/popular.html', {'quotes': quotes})


@csrf_exempt
@require_POST
def vote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    is_like = request.POST.get('is_like') == 'true'
    user_ip = request.META.get('REMOTE_ADDR')
    
    if not user_ip:
        return JsonResponse({'error': 'Не удалось определить IP адрес'}, status=400)
    
    # Удаляем предыдущий голос пользователя, если есть
    Like.objects.filter(quote=quote, ip_address=user_ip).delete()
    
    # Создаем новый голос
    Like.objects.create(quote=quote, is_like=is_like, ip_address=user_ip)
    
    # Возвращаем обновленную статистику
    likes_count = Like.objects.filter(quote=quote, is_like=True).count()
    dislikes_count = Like.objects.filter(quote=quote, is_like=False).count()
    
    return JsonResponse({
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_vote': 'like' if is_like else 'dislike'
    })