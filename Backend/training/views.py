from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from training.models import Profile, QuizResult, SimulationResult
from training.serializers import QuizResultSerializer, SimulationResultSerializer





def home_view(request):
    return render(request, 'home.html')


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


def guidelines_view(request):
    return render(request, 'guidelines.html')


@login_required(login_url='/login/')
def quiz_view(request):
    return render(request, 'quiz.html')


@login_required(login_url='/login/')
def crane_view(request):
    return render(request, 'crane.html')


@login_required(login_url='/login/')
def forklift_view(request):
    return render(request, 'forklift.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            error = "Please enter both username and password."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = f"Username '{username}' is already taken."
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {username}.")
            return redirect('home')

    return render(request, 'signup.html', {'error': error})


def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('home')

    error = None
    next_url = request.GET.get('next', '') or request.POST.get('next', '')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")

            if next_url and next_url.startswith('/'):
                return redirect(next_url)

            if hasattr(user, 'profile') and user.profile.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            error = "Invalid username or password."

    return render(request, 'login.html', {'error': error, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('login')


@login_required(login_url='/login/')
def admin_dashboard_view(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        messages.error(request, "Access restricted to administrators.")
        return redirect('home')

    users = User.objects.select_related('profile').all().order_by('-date_joined')
    trainees = []

    for u in users:
        latest_quiz = u.quiz_results.order_by('-taken_at').first()
        quiz_score = latest_quiz.score_percent if latest_quiz else None
        quiz_passed = latest_quiz.passed if latest_quiz else None

        crane_sims = u.simulation_results.filter(simulator_type='crane')
        crane_best = crane_sims.order_by('time_taken_seconds').first()
        crane_time = crane_best.time_taken_seconds if crane_best else None

        forklift_sims = u.simulation_results.filter(simulator_type='forklift')
        forklift_best = forklift_sims.order_by('time_taken_seconds').first()
        forklift_time = forklift_best.time_taken_seconds if forklift_best else None

        if quiz_passed and crane_time is not None and forklift_time is not None:
            overall_status = 'Fully Unlocked'
            status_code = 'unlocked'
        elif quiz_passed:
            overall_status = 'Quiz Passed'
            status_code = 'quiz_passed'
        elif quiz_score is not None:
            overall_status = 'Quiz Failed'
            status_code = 'quiz_failed'
        else:
            overall_status = 'Pending'
            status_code = 'pending'

        crane_str = f"{int(crane_time//60):02d}:{int(crane_time%60):02d}" if crane_time is not None else "N/A"
        forklift_str = f"{int(forklift_time//60):02d}:{int(forklift_time%60):02d}" if forklift_time is not None else "N/A"

        trainees.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.profile.role if hasattr(u, 'profile') else 'user',
            'quiz_score': round(quiz_score, 1) if quiz_score is not None else None,
            'quiz_passed': quiz_passed,
            'crane_time_raw': crane_time,
            'crane_time_str': crane_str,
            'forklift_time_raw': forklift_time,
            'forklift_time_str': forklift_str,
            'overall_status': overall_status,
            'status_code': status_code,
            'date_joined': u.date_joined.strftime('%Y-%m-%d'),
        })

    leaderboard_qs = SimulationResult.objects.select_related('user').order_by('time_taken_seconds')
    leaderboard = []
    for idx, sim in enumerate(leaderboard_qs, start=1):
        t_sec = sim.time_taken_seconds
        t_str = f"{int(t_sec//60):02d}:{int(t_sec%60):02d}"
        leaderboard.append({
            'rank': idx,
            'user_id': sim.user.id,
            'username': sim.user.username,
            'simulator_type': sim.simulator_type.capitalize(),
            'sim_key': sim.simulator_type,
            'time_taken_seconds': round(t_sec, 2),
            'time_str': t_str,
            'score': round(sim.score, 1),
            'passed': sim.passed,
            'completed_at': sim.completed_at.strftime('%Y-%m-%d %H:%M'),
        })

    context = {
        'trainees': trainees,
        'leaderboard': leaderboard,
    }
    return render(request, 'admin_dashboard.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_user_detail_api(request, user_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({'error': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    quiz_results = QuizResultSerializer(user_obj.quiz_results.all().order_by('-taken_at'), many=True).data
    sim_results = SimulationResultSerializer(user_obj.simulation_results.all().order_by('-completed_at'), many=True).data

    return Response({
        'id': user_obj.id,
        'username': user_obj.username,
        'email': user_obj.email,
        'role': user_obj.profile.role if hasattr(user_obj, 'profile') else 'user',
        'date_joined': user_obj.date_joined.strftime('%Y-%m-%d %H:%M'),
        'quiz_results': quiz_results,
        'simulation_results': sim_results,
    })


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def admin_user_edit_api(request, user_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({'error': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    new_role = request.data.get('role')
    new_username = request.data.get('username')

    if new_role and new_role in ['user', 'admin']:
        if hasattr(user_obj, 'profile'):
            user_obj.profile.role = new_role
            user_obj.profile.save()

    if new_username and new_username.strip():
        clean_name = new_username.strip()
        if User.objects.filter(username=clean_name).exclude(id=user_obj.id).exists():
            return Response({'error': f"Username '{clean_name}' is already taken."}, status=status.HTTP_400_BAD_REQUEST)
        user_obj.username = clean_name
        user_obj.save()

    return Response({
        'message': 'User updated successfully.',
        'id': user_obj.id,
        'username': user_obj.username,
        'role': user_obj.profile.role if hasattr(user_obj, 'profile') else 'user'
    })


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def admin_user_delete_api(request, user_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({'error': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    if request.user.id == user_id:
        return Response({'error': 'You cannot delete your own logged-in admin account.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_obj = User.objects.get(id=user_id)
        deleted_username = user_obj.username
        user_obj.delete()
        return Response({'message': f"User '{deleted_username}' and all associated results deleted successfully."})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz_api(request):
    try:
        score_percent = float(request.data.get('score_percent'))
    except (ValueError, TypeError):
        return Response({'error': 'Invalid or missing score_percent value'}, status=status.HTTP_400_BAD_REQUEST)

    passed = score_percent > 60
    quiz_result = QuizResult.objects.create(
        user=request.user,
        score_percent=score_percent,
        passed=passed
    )

    serializer = QuizResultSerializer(quiz_result)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_simulation_api(request):
    simulator_type = request.data.get('simulator_type')
    if simulator_type not in ['crane', 'forklift']:
        return Response({'error': "simulator_type must be 'crane' or 'forklift'"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        time_taken_seconds = float(request.data.get('time_taken_seconds'))
        score = float(request.data.get('score'))
        passed = bool(request.data.get('passed'))
    except (ValueError, TypeError):
        return Response({'error': 'Invalid or missing simulation payload'}, status=status.HTTP_400_BAD_REQUEST)

    sim_result = SimulationResult.objects.create(
        user=request.user,
        simulator_type=simulator_type,
        time_taken_seconds=time_taken_seconds,
        score=score,
        passed=passed
    )

    serializer = SimulationResultSerializer(sim_result)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



