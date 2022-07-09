from django.shortcuts import render
from .forms import VacancyForm
from .func.hh import to_count_elements_in_list, get_vacancy_skills


# Create your views here.

def index(request):
    if request.method == 'POST':
        vacancy_name = request.POST.get('vacancy_name')
        skills = to_count_elements_in_list(get_vacancy_skills(vacancy_name))
        return render(request, "get_skills/result.html",
                      context={"skills": skills})
    else:
        form = VacancyForm()
        if not form.is_valid():
            print(form.errors)
        return render(request, "get_skills/index.html", context={'form': form})


def result(request, data):
    return render(request, "get_skills/result.html", context=data)
