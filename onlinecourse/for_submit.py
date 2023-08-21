def submit(request, course_id):
    template_name = 'onlinecourse/exam_result_bootstrap.html'
    course = Course.objects.get(pk=course_id)
    questions = Question.objects.filter(courses=course) #questions that related to the course
    questions_length = questions.count()   # count all questions related to the course
    the_result = extract_answers(request)  #variable for all selected choices by user
    printed_result = []       #what will be printed of results
    all_correct = []      # only correct choices
    counter = 0
    for question in questions:
        the_question = question.question_text
        choices = question.choice_set.all()
        for choice in choices:
            choice_id = choice.id  # Move this assignment inside the loop
            if choice_id in the_result:
                choice.selected_id = True #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #selected_ids = extract_answers(request) # what this line doing here !!??
                result, _ = question.is_get_score(selected_ids)
                all_correct.append({ 'choices': choice.choice_text,})
                printed_result.append({
                  'question': the_question,
                  'selected_choice': all_correct,
                })    
        if result:
            counter += 1
    grade = (counter / questions_length) * 100
    course_result = grade >= 80
    
    context = {
        'course': course,
        'grade': grade,
        'course_result': course_result,
        'exam_result': printed_result,
        'questions': the_question,
        'course_id': course_id,
    }
    
    return render(request, template_name, context)
===================================================================
def submit(request, course_id):
    template_name = 'onlinecourse/exam_result_bootstrap.html'
    course = Course.objects.get(pk=course_id)
    questions = Question.objects.filter(courses=course)
    questions_length = questions.count()   
    the_selected_id = extract_answers(request)
    printed_result = []
    all_correct = []
    counter = 0
    for question in questions:
        the_question = question.question_text
        choices = question.choice_set.all()
        for choice in choices:
            choice_id = choice.id  # Move this assignment inside the loop
            if choice_id in the_selected_id:
                choice.selected_id = True
                result, _ = question.is_get_score(selected_ids)
                all_correct.append({ 'choices': choice.choice_text,})
                selected_ids = extract_answers(request) # what this line doing here !!??
                printed_result.append({
                  #'question': the_question,
                  'selected_choice': all_correct,
                })    
        if result:
            counter += 1
    grade = (counter / questions_length) * 100
    course_result = grade >= 80
    
    context = {
        'course': course,
        'grade': grade,
        'course_result': course_result,
        'exam_result': printed_result,
        'questions': the_question,
        'course_id': course_id,
    }
    
    return render(request, template_name, context)
=====================================================================
the old:

def submit(request, course_id):
    print("yyyyyyyyyyyyyyyy",extract_answers(request),"yyyyyyyyyyyyyyyy")
    template_name = 'onlinecourse/exam_result_bootstrap.html'
    course = Course.objects.get(pk=course_id)
    questions = Question.objects.filter(courses=course)
    questions_length = questions.count()   
    selected_ids = extract_answers(request)
    printed_result = []
    all_correct = []
    counter = 0
    print("questions , questions_length" , questions,"this course got: ",questions_length," qustions..","selected by user: ", selected_ids)
    for question in questions:
        the_question = question.question_text
        choices = question.choice_set.all()
        print(choices,"ooooooooooooooooooo")
        for choice in choices:
            choice_id = choice.id  # Move this assignment inside the loop
            if choice_id in selected_ids:
                print(choice.selected_id,"----------")
                choice.selected_id = True
                result = question.is_get_score(selected_ids)  # need explain !!!!!!
                if result:
                    counter += 1
                print(choice.selected_id,"8888888888")
                print("choice...",choice.selected_id)
        all_correct.append({ 'choices': choice.choice_text,})
        printed_result.append({
                  'question': the_question,
                  'selected_choice': all_correct,
                })    
        print("vvvvvvv",counter,"vvvvvv")   
        
    print("pppppppp",counter,"pppppp") 
    grade = (counter / questions_length) * 100
    course_result = grade >= 80
    
    context = {
        'course': course,
        'grade': grade,
        'course_result': course_result,
        'exam_result': printed_result,
        'questions': the_question,
        'course_id': course_id,
    }
    counter = 0
    return render(request, template_name, context)
=====================================================================
 By chat GPT:

def submit(request, course_id):
    template_name = 'onlinecourse/exam_result_bootstrap.html'
    course = Course.objects.get(pk=course_id)
    questions = Question.objects.filter(courses=course)
    questions_length = questions.count()
    selected_ids = extract_answers(request)
    printed_result = []
    counter = 0
    for question in questions:
        the_question = question.question_text
        choices = question.choice_set.all()
        selected_choices = []  # Store selected choices for the current question       
        for choice in choices:
            choice_id = choice.id
            if choice_id in selected_ids:
                choice.selected_id = True
                selected_choices.append({'choices': choice.choice_text})
        result = question.is_get_score(selected_ids)
        if result:
            counter += 1        
        printed_result.append({
            'question': the_question,
            'selected_choice': selected_choices,
        })    
    grade = (counter / questions_length) * 100
    course_result = grade >= 80    
    context = {
        'course': course,
        'grade': grade,
        'course_result': course_result,
        'exam_result': printed_result,
        'course_id': course_id,
    }
    return render(request, template_name, context)
    ===================================================== 11:00  20-8-2023 befor major editing

    def submit(request, course_id):
    template_name = 'onlinecourse/exam_result_bootstrap.html'
    course = Course.objects.get(pk=course_id)
    questions = Question.objects.filter(courses=course)
    questions_length = questions.count()
    selected_ids = []
    print ("=====",selected_ids,"=====")
    how_many = len(selected_ids)
    printed_result = []
    selected_ids = extract_answers(request)
    counter = 0
    correct_count = 0
    default_result = False
    default_selected = False
    for question in questions:
        question.result = question.is_get_score(selected_ids)
        if question.result:
            counter += 1       
        print ("===after==",selected_ids,"==after===")
        the_question = question.question_text
        choices = question.choice_set.all()
        selected_choices = []  # Store selected choices for the current question       
        for choice in choices:           
            choice_id = choice.id
            if choice_id in selected_ids:
                choice.selected_id = True
                selected_choices.append({'choices': choice.choice_text,})
                if choice.is_correct:
                    print(choice.choice_text, "is correct")
                    correct_count +=1
                print(selected_choices,"///", counter)
                                          
        print(how_many,"xxxxxxxxxxx",correct_count )        
        printed_result.append({
            'question': the_question,
            'selected_choice': selected_choices,
        })  
    print("counter is:  ", counter,"<<<<>>>>")  
    grade = (counter / questions_length) * 100
    course_result = grade >= 80    
    context = {
        'course': course,
        'grade': grade,
        'course_result': course_result,
        'exam_result': printed_result,
        'course_id': course_id,
    }
    counter = 0
    for question in questions:
        print(question.question_text,"Before>>",question.result)
        question.result = default_result
        question.save()
        print(question.question_text,"After>>",question.result)
    for choice in choices:
        print(choice.selected_id,"Before>>",choice.selected_id)
        choice.selected_id = default_selected
        choice.save()
        print(choice.selected_id,"After>>",choice.selected_id)    
    return render(request, template_name, context)
============================
check if I need these:

    for question in questions:
        print(question.question_text,"Before>>",question.result)
        question.result = default_result
        question.save()
        print(question.question_text,"After>>",question.result)
    for choice in choices:
        print(choice.selected_id,"Before>>",choice.selected_id)
        choice.selected_id = default_selected
        choice.save()
        print(choice.selected_id,"After>>",choice.selected_id)
