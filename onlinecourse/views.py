from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Course, Enrollment, Question, Choice, Lesson
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses
#QuestionsListView:
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    context_object_name = 'courses'
class LessonDetailView(generic.DetailView):
    model = Lesson
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    context_object_name = 'lesson'
class QuestionListView(generic.ListView):
    model = Question
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        course_id = self.kwargs['course_id']  # This to Retrieve the course_id from URL, intresting!!
        course = get_object_or_404(Course, pk=course_id)
        #user = self.request.user
        questions = Question.objects.filter(courses=course)  # Filter questions by the related course
        return questions 
'''class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    context_object_name = 'question'
    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs['pk']  # Retrieve the course_id from URL parameters
        course = get_object_or_404(Course, pk=course_id)
        
        if user.is_authenticated and check_if_enrolled(user, course):
            question = Question.objects.all()
        else:
            question = []  # Empty list when user is not authenticated or not enrolled           
        return question'''

class ChoiceListView(generic.ListView):
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    context_object_name = 'choice_list'
    def get_queryset(self):
        user = self.request.user
        choices = Choice.objects.all()
        return choices

def enroll(request, course_id):
    model = Choice
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
         # Get user and course object, then get the associated enrollment object created when the user enrolled the course
         # Create a submission object referring to the enrollment
         # Collect the selected choices from exam form
         # Add each selected choice object to the submission object
         # Redirect to show_exam_result with the submission id


# <HINT> A example method to collect the selected choices from the exam form from the request object
def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwsers.append(choice_id)
    return submitted_anwsers

def submit(request, course_id):
    # What I understand is: submit method is to take collected answers from 'extract_answers' function
    # then fill Choice model with it, then bring 'Passed' questions from Question model 
    # and calculate the grade for the Course (>= 80 pass else failud):
    template_name = 'onlinecourse/exam_result_bootstrap.html'
    #course = get_object_or_404(Course, pk=course_id)
    course = Course.objects.get(pk=course_id)
    #question = get_object_or_404(Question, pk=question_id)
    questions = Question.objects.filter(courses=course)
    questions_length = questions.count()   
    #choice = Choice.objects.get(pk=course_id) 
    for question in questions:
        choices = question.choice_set.all()  # Get all choices related to the current question
        for choice in choices:
            choice_id = choice.id
    for answered in extract_answers(request):
        if choice_id == answered:
            choice.selected_ids = True  # To fill 'selected_ids' field in Choice model
    counter = 0
    for question in  questions:
        selected_ids = extract_answers(request)
        result, _ = question.is_get_score(selected_ids)
        if result:
            counter +=1
    grade = (counter/questions_length)*100
    course_result = grade >= 80  # if grade >= 80 course_result output is True, usefull..!!
    context = {
        'course':course,
        'grade': grade,
        'course_result': course_result,
    }
    return render(request, template_name, context)


# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question,
# you may implement it based on the following logic:
        # Get course and submission based on their ids
        # Get the selected choice ids from the submission record
        # For each selected choice, check if it is a correct answer or not
        # Calculate the total score
#def show_exam_result(request, course_id, submission_id):



