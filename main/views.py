from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, NewReplyForm
from django.http import HttpResponse
# Create your views here.

def registerPage(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def loginPage(request):
    form = LoginForm()

    if request.method == 'POST':
        try:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'login.html', context)

@login_required(login_url='register')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='register')
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'new-question.html', context)

def homePage(request):
    questions = Question.objects.all().order_by('-created_at')
    context = {
        'questions': questions
    }
    return render(request, 'homepage.html', context)

def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question(id=id)
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'question.html', context)


@login_required(login_url='register')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('index')

def question_page_view(request):
    # Retrieve the search query from the request parameters
    query = request.GET.get('query')

    # Perform the search logic
    if query:
        # Perform your search operations using the query
        results = perform_search(query)
    else:
        results = None  # No query provided, display all results or an empty state

    # Other code for rendering the page
    context = {
        'question': question,
        'user': request.user,
        'results': results  # Pass the search results to the template
    }
    return render(request, 'question.html', context)

# def search(request):
#     mydata = Question.object.filter().values()
#     template = loader.get_template('question.html')
#     context = {
#         "questions":mydata,
#     }
#     return HttpResponse(template.render(context, request))


# def question_detail(request, question_id):
#     question = Question.objects.get(id=question_id)
#     response_form = ResponseForm()

#     # Handle search functionality
#     search_query = request.GET.get('search_query')
#     if search_query:
#         # Perform search operation based on the search_query
#         # Update the question object or retrieve filtered responses
#         # and pass the filtered data to the template

#     context = {
#         'question': question,
#         'response_form': response_form,
#     }
#     return render(request, 'question_detail.html', context)
