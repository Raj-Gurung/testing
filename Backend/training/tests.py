from django.test import TestCase, Client
from django.contrib.auth.models import User
from training.models import Profile, QuizResult, SimulationResult


class LandingPageAndGuestAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='normal_user', password='password123')
        self.admin = User.objects.create_user(username='admin_user', password='password123')
        self.admin.profile.role = 'admin'
        self.admin.profile.save()

    def test_root_landing_page_unauthenticated(self):
        """Root URL shows landing page with Login, Sign Up, and Browse as Guest for unauthenticated visitors."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Browse as Guest')
        self.assertContains(response, '/login/')
        self.assertContains(response, '/signup/')
        self.assertContains(response, '/home/')

    def test_public_pages_accessible_to_guests(self):
        """Public pages (home, about, guidelines, contact) are accessible without logging in."""
        for path in ['/home/', '/about/', '/guidelines/', '/contact/']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_protected_pages_redirect_guests_to_login(self):
        """Quiz and simulators require login; unauthenticated visitors are redirected to /login/."""
        for path in ['/quiz/', '/crane/', '/forklift/', '/admin-dashboard/']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 302)
                self.assertIn('/login/', response.url)

    def test_root_landing_page_redirects_authenticated_users(self):
        """Authenticated users visiting root are redirected to home or admin dashboard."""
        self.client.login(username='normal_user', password='password123')
        response = self.client.get('/')
        self.assertRedirects(response, '/home/')

        self.client.login(username='admin_user', password='password123')
        response = self.client.get('/')
        self.assertRedirects(response, '/admin-dashboard/')


class AdminDashboardAttemptCountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin_boss', password='adminpass123')
        self.admin.profile.role = 'admin'
        self.admin.profile.save()

        self.trainee = User.objects.create_user(username='trainee_bob', password='bobpassword')
        QuizResult.objects.create(user=self.trainee, score_percent=50.0, passed=False)
        QuizResult.objects.create(user=self.trainee, score_percent=80.0, passed=True)
        SimulationResult.objects.create(user=self.trainee, simulator_type='crane', time_taken_seconds=45.0, score=90.0, passed=True)
        SimulationResult.objects.create(user=self.trainee, simulator_type='crane', time_taken_seconds=39.0, score=98.0, passed=True)
        SimulationResult.objects.create(user=self.trainee, simulator_type='forklift', time_taken_seconds=55.0, score=85.0, passed=True)

    def test_admin_dashboard_table_attempt_counts(self):
        """Admin dashboard displays dedicated Attempt Counts section and tabs."""
        self.client.login(username='admin_boss', password='adminpass123')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tab-btn-attempts')
        self.assertContains(response, 'view-attempts')
        self.assertContains(response, 'Quiz Attempts')
        self.assertContains(response, 'Total Sim Attempts')

    def test_admin_detail_api_attempt_counts(self):
        """Admin user detail API returns precise counts for quiz and simulation attempts."""
        self.client.login(username='admin_boss', password='adminpass123')
        response = self.client.get(f'/api/admin/users/{self.trainee.id}/detail/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['quiz_attempts_count'], 2)
        self.assertEqual(data['sim_attempts_count'], 3)
        self.assertEqual(data['crane_attempts_count'], 2)
        self.assertEqual(data['forklift_attempts_count'], 1)


class LoginWhitespaceSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='security_user', password='secure_password')

    def test_username_leading_trailing_whitespace_trimmed_on_login(self):
        """Username leading/trailing whitespace is trimmed during login lookup."""
        response = self.client.post('/login/', {
            'username': '   security_user   ',
            'password': 'secure_password'
        })
        self.assertRedirects(response, '/home/')

    def test_password_leading_trailing_whitespace_not_ignored(self):
        """Passwords with extra leading or trailing spaces are NOT stripped and must fail authentication."""
        # Leading space in password
        res_leading = self.client.post('/login/', {
            'username': 'security_user',
            'password': ' secure_password'
        })
        self.assertEqual(res_leading.status_code, 200)
        self.assertContains(res_leading, 'Invalid username or password')

        # Trailing space in password
        res_trailing = self.client.post('/login/', {
            'username': 'security_user',
            'password': 'secure_password '
        })
        self.assertEqual(res_trailing.status_code, 200)
        self.assertContains(res_trailing, 'Invalid username or password')

    def test_signup_whitespace_handling(self):
        """Signup trims username but preserves exact password character sequence."""
        res = self.client.post('/signup/', {
            'username': '  new_trainee_user  ',
            'password': ' exact password ',
            'confirm_password': ' exact password '
        })
        self.assertRedirects(res, '/home/')

        created_user = User.objects.get(username='new_trainee_user')
        self.assertEqual(created_user.username, 'new_trainee_user')

        # Logging in without spaces in password must fail
        self.client.logout()
        res_fail = self.client.post('/login/', {
            'username': 'new_trainee_user',
            'password': 'exact password'
        })
        self.assertEqual(res_fail.status_code, 200)
        self.assertContains(res_fail, 'Invalid username or password')

        # Logging in with exact spaced password must succeed
        res_success = self.client.post('/login/', {
            'username': 'new_trainee_user',
            'password': ' exact password '
        })
        self.assertRedirects(res_success, '/home/')
