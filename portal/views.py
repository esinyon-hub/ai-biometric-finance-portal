from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile, AuditLog, Budget, Expense, Transaction
from .biometric import capture_face, compare_faces

# ---------------- LOGIN / REGISTER ----------------
def login_register(request):
    context = {}

    if request.method == "POST":

        # ------------------------ LOGIN ------------------------
        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            try:
                user = UserProfile.objects.get(username=username)
                password_valid = check_password(password, user.password)
                face_match = False
                liveness = False

                if password_valid:
                    face_match = compare_faces(username)
                    liveness = True
                    if face_match and liveness:
                        request.session['username'] = username
                        user.last_login = timezone.now()
                        user.save()
                        AuditLog.objects.create(
                            username=username,
                            password_check=True,
                            face_match=True,
                            liveness=True
                        )
                        return redirect('dashboard')

                # Failed login
                AuditLog.objects.create(
                    username=username,
                    password_check=password_valid,
                    face_match=face_match,
                    liveness=liveness
                )
                context["login_error"] = "Login failed: Face not recognized or password incorrect"

            except UserProfile.DoesNotExist:
                context["login_error"] = "Login failed: User does not exist"

        # ------------------------ REGISTER ------------------------
        elif "register" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            role = request.POST.get("role")
            if UserProfile.objects.filter(username=username).exists():
                context["register_error"] = "Username already exists"
            else:
                UserProfile.objects.create(
                    username=username,
                    password=make_password(password),
                    role=role
                )
                capture_face(username)
                context["login_error"] = "Registration successful! Please login."

    return render(request, "portal/biometric_login.html", context)


# ---------------- DASHBOARD ----------------
def dashboard(request):
    username = request.session.get("username")
    if not username:
        return redirect('biometric_login')

    # if Guest, create a temporary user object
    if username == "Guest":
        user = type("User", (object,), {"username": "Guest", "role": "Guest"})()
    else:
        user = UserProfile.objects.get(username=username)

    transactions = Transaction.objects.all().order_by('-date')
    budgets = Budget.objects.all()
    expenses = Expense.objects.all()
    logs = AuditLog.objects.order_by('-timestamp')[:10]

    return render(request, "portal/dashboard.html", {
        "user": user,
        "transactions": transactions,
        "budgets": budgets,
        "expenses": expenses,
        "logs": logs
    })


# ---------------- BYPASS LOGIN ----------------
def bypass_login(request):
    # set session for Guest
    request.session['username'] = "Guest"
    return redirect('dashboard')


# ---------------- ADD BUDGET ----------------
def add_budget(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        Budget.objects.create(name=name, total_amount=amount)
    return redirect('dashboard')


# ---------------- ADD EXPENSE ----------------
def add_expense(request):
    if request.method == "POST":
        budget_id = request.POST.get("budget")
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        budget = Budget.objects.get(id=budget_id)
        Expense.objects.create(budget=budget, description=description, amount=amount)
    return redirect('dashboard')