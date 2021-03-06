from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# import hashlib
from .models import Board, Comment
from .forms import BoardForm, CommentForm

# Create your views here.
def index(request):
    # 템플릿에 해야 효율적임
    # if request.user.is_authenticated:
    #     gravatar_url = hashlib.md5(request.user.email.strip().lower().encode('utf-8')).hexdigest()
        
    # else:
    #     gravatar_url = None
    
    boards = get_list_or_404(Board.objects.order_by('-pk'))
    # boards = Board.objects.order_by('-pk')
    context = {
        'boards':boards,
        # 'gravatar_url':gravatar_url, 
    }
    return render(request, 'boards/index.html', context)
    
# def create(request):
#     # POST 요청이면 FORM 데이터를 처리한다.
#     if request.method == 'POST':
#         # 이 처리과정은 "binding" 으로 불리는데, 폼의 유효성 체크를 할수있도록 해준다.
#         form = BoardForm(request.POST)
#         # form 유효성 체크
#         if form.is_valid():
#             title =form.cleaned_data.get('title')
#             content = form.cleaned_data.get('content')
#             #검증을 통과한 깨끗한 데이터를 form에서 가져와서  board 를만든다.
#             board = Board.objects.create(title=title, content=content)
#             return redirect('boards:detail', board.pk)
#     # GET 요청(혹은 다른 메서드)이면 기본 폼을 생성한다.
#     else:
#         form = BoardForm()
#     context = {'form' : form}
#     return render(request, 'boards/create.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False) # board 를 바로 저장하지 않고, 현재 user 를 넣고 저장
            #실제 DB 반영 전까지의 단계를 진행하고, 그 중간에 user 정보를 requser.user 에서 가져와서 그 후에 저장한다.
            board.user = request.user
            board.save()
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm()
    context = {'form' : form}
    return render(request, 'boards/form.html', context)


def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    comment_form = CommentForm(instance = board)
    context = {'board':board,
                'comment_form' : comment_form,
    }
    return render(request, 'boards/detail.html', context)
    
    
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')
        
        
        
# def update(request, board_pk):
#     board = get_object_or_404(Board, pk=board_pk)
#     if request.method == 'POST':
#         form = BoardForm(request.POST)
#         if form.is_valid():
#             board.title = form.cleaned_data.get('title')
#             board.content = form.cleaned_data.get('content')
#             board.save()
#             return redirect('boards:detail', board.pk)
#     #GET 요청이면(수정하기 버튼을 눌렀을 때)        
#     else:
#         #BoardForm 을 초기화(사용자 입력 값을 넣어준 상태로)
        
#         # form = BoardForm(initial={'title':board.title, 'content':board.content})
#         form = BoardForm(initial=board.__dict__)
    
#     # 1. POST : 요청에서 검증에 실패하였을 때, 오류메세지가 포함된 상태
#     # 2. GET : 요청에서 초기화된 상태
    
#     context = {'form':form}
#     return render(request, 'boards/create.html', context)
@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            form = BoardForm(request.POST, instance=board)  # 1
            if form.is_valid():
                board = form.save()                         # 2
                return redirect('boards:detail', board.pk)
                
        else:
            form = BoardForm(instance=board)                 # 3
    else:
        return redirect('boards:index')
    context = {
        'form' : form,
        'board' : board,
    }
    return render(request, 'boards/form.html', context)
    
    
@require_POST
@login_required
def comments_create(request, board_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # 쿼리 없이 객체로가져오면 다음과같이 쓴다.
        comment.user = request.user
        # 객체로가져오면 쿼리 하나 더 생기기 때문에  다음과같이 쓴다.
        comment.board_id = board_pk
        comment.save()

    return redirect('boards:detail', board_pk)
    
@require_POST
@login_required
def comments_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('boards:detail', board_pk)
        
