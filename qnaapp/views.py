from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def my_QA_page(request):
    import sqlite3
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("select * from default_QA_table")
    res = cur.fetchall()
    return render(request, 'QA.html', {'qas': res})


def add_QA_page(request):
    from .models import user_QA
    if request.method == "POST":
        entered_username = request.session["user_name"]
        entered_question = request.POST.get('question')
        print(entered_question)
        new_question = user_QA()
        new_question.username = entered_username
        new_question.Questions = entered_question
        new_question.save()
        return redirect(my_QA_page)
    else:
        return HttpResponse("Method Not Supported")



