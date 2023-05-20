from django.shortcuts import render, redirect


def addfunds(request):
    if request.method == 'POST':
        request.user.credit.credit += float(request.POST['amount'])
        request.user.credit.save()
        return redirect('addfunds')
    context = {
        "user": request.user,
    }
    return render(request, 'users/addfunds.html', context)
