from django import contrib
from django.core.checks import messages
from django.forms.widgets import FileInput
from django.shortcuts import redirect, render
import wikipedia
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch 
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")    
    else:
        form=NotesForm()

    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model=Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks =Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f"Homework Added from {request.user.username}!!")
    else:
        form = HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context={'homeworks':homework,
             'homeworks_done':homework_done,
             'form':form,
             }
    return render(request,'dashboard/homework.html',context)

@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' :i['title'],
                'duration' :i['duration'],
                'thumbnail' :i['thumbnails'][0]['url'],
                'channel' :i['channel']['name'],
                'link' :i['link'],
                'views' :i['viewCount']['short'],
                'published' :i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)

            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardFom()
    context = {'form':form}
    return render(request,"dashboard/youtube.html",context)

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid:
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished =False
        todos = Todo(
            user = request.user,
            title = request.POST['title'],
            is_finished = finished
        )
        todos.save()
        messages.success(request,f'Todo Added from {request.user.username}!!')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,'dashboard/todo.html',context)

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished =True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []

        if 'items' in answer:
            for i in range(min(10, len(answer['items']))):
                book = answer['items'][i]['volumeInfo']
                result_dict = {
                    'title': book.get('title', 'No title available'),
                    'subtitle': book.get('subtitle'),
                    'description': book.get('description', 'No description available'),
                    'count': book.get('pageCount'),
                    'categories': book.get('categories'),
                    'rating': book.get('averageRating', 'No rating'),
                    'thumbnail': book.get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/150'),
                    'preview': book.get('previewLink')
                }
                result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        else:
            context = {
                'form': form,
                'error': f"No books found for '{text}'. Please try a different query."
            }

        return render(request, 'dashboard/books.html', context)

    else:
        form = DashboardFom()
        return render(request, "dashboard/books.html", {'form': form})

# def books(request):
#     if request.method == 'POST':
#         form = DashboardFom(request.POST)
#         text = request.POST['text']
#         url = "https://www.googleapis.com/books/v1/volumes?q="+text
#         r = requests.get(url)
#         answer = r.json()
#         result_list = []
#         for i in range(10):
#             result_dict = {
#                 'title' :answer['items'][i]['volumeInfo']['title'],
#                 'subtitle' :answer['items'][i]['volumeInfo'].get('subtitle'),
#                 'description' :answer['items'][i]['volumeInfo'].get('description'),
#                 'count' :answer['items'][i]['volumeInfo'].get('pageCount'),
#                 'categories' :answer['items'][i]['volumeInfo'].get('categories'),
#                 'rating' :answer['items'][i]['volumeInfo'].get('pageRating'),
#                 'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/150'),
#                 'preview' :answer['items'][i]['volumeInfo'].get('previewLink')
#             }

#             result_list.append(result_dict)

#             context = {
#                 'form':form,
#                 'results':result_list
#             }
#         return render(request,'dashboard/books.html',context)
#     else:
#         form = DashboardFom()
#     context = {'form':form}
#     return render(request,"dashboard/books.html",context)
# import requests
# from django.shortcuts import render

def dictionary(request):
    if request.method == 'POST':
        form = DashboardFom(request.POST)
        text = request.POST.get('text')
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        response = requests.get(url)
        
        if response.status_code == 200:
            try:
                answer = response.json()
                word_data = answer[0]

                phonetics = word_data.get('phonetics', [{}])[0].get('text', 'N/A')
                audio = word_data.get('phonetics', [{}])[0].get('audio', '')
                definition = word_data.get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'No definition found')
                example = word_data.get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', 'No example available')
                synonyms = word_data.get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms', [])

                context = {
                    'form': form,
                    'input': text,
                    'url': url,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms
                }
            except (IndexError, KeyError, TypeError):
                context = {
                    'form': form,
                    'input': text,
                    'error': "Unexpected data format from dictionary API."
                }
        else:
            context = {
                'form': form,
                'input': text,
                'error': "Word not found or API request failed."
            }

        return render(request, 'dashboard/dictionary.html', context)

    else:
        form = DashboardFom()
        return render(request, 'dashboard/dictionary.html', {'form': form})

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from django.shortcuts import render
from .forms import DashboardFom  # make sure the form is imported

def wiki(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        form = DashboardFom(request.POST)
        
        try:
            page = wikipedia.page(text)
            context = {
                'form': form,
                'title': page.title,
                'link': page.url,
                'details': page.summary
            }
        except DisambiguationError as e:
            options = e.options[:5]  # show only top 5 options
            context = {
                'form': form,
                'title': "Disambiguation Error",
                'link': '',
                'details': f"Your search term '{text}' is ambiguous. Possible options include: {', '.join(options)}. Please be more specific."
            }
        except PageError:
            context = {
                'form': form,
                'title': "Page Not Found",
                'link': '',
                'details': f"No page found for '{text}'."
            }
        except Exception as e:
            context = {
                'form': form,
                'title': "Error",
                'link': '',
                'details': str(e)
            }

        return render(request, "dashboard/wiki.html", context)

    else:
        form = DashboardFom()
        context = {
            'form': form
        }
        return render(request, "dashboard/wiki.html", context)

# def wiki(request):
#     if request.method == 'POST':
#         text = request.POST['text']
#         form = DashboardFom(request.POST)
#         search = wikipedia.page(text)
#         context = {
#             'form':form,
#             'title':search.title,
#             'link':search.url,
#             'details':search.summary,
#         }
#         return render(request,"dashboard/wiki.html",context)
#     else:
#         form = DashboardFom()
#         context = {
#             'form':form
#         }
#     return render(request,"dashboard/wiki.html",context)

def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input)>=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input)>=0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.2062} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:
        form = ConversionForm()
        context = {
            'form':form,
            'input':False
        }
    return render(request,"dashboard/conversion.html",context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        'form':form,
    }
    return render(request,'dashboard/register.html',context)


def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) ==0:
        homework_done = True
    else:
        homework_done = False
    if len(todos)==0:
        todos_done = True
    else:
        todos_done = False
    context ={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }  
    return render(request,'dashboard/profile.html',context)

def logout(request):
    return render(request,'dashboard/logout.html')
   
