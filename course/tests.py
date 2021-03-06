from django.test import Client
from django.test import TestCase
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pineapple.settings")
from exercise import populate


class ServerTestCase(TestCase):

    def setUp(self):
        # Must be run, else crash
        django.setup()
        self.client = Client()
        # Create test lecturer and the corresponding lecturer group.
        populate.add_user_group('Lecturer')
        populate.add_user(
            username='theTeach',
            email='teach@me.com',
            password='schooled',
            course_list=[],
            pers_exercise_list=[],
            result_pk_list=[],
            group_name_list=['Lecturer']
        )
        # Create test course to select later
        populate.add_course(
            name='TDTT3st',
            full_name='T3h L33t3st C0urse',
            admin_list=['theTeach'],
            material_list=[],
            description='For testing purposes'
        )
        # Create test student and the corresponding user group
        populate.add_user_group('Student')
        populate.add_user(
            username='theMan',
            email='the@man.no',
            password='thePa$$word',
            course_list=[],
            pers_exercise_list=[],
            result_pk_list=[],
            group_name_list=['Student']
        )
        # Create test question and an exercise
        populate.add_question(
            title='test Q',
            question='Will this humble test bless us by working as intended?',
            alternative_list=['hell yeah!', 'over my dead body', 'Never!', 'define "working"'],
            correct_num=4,
            tag_list=[],
            belongs_to='TDTT3st',
            is_worth=1000000,
        )
        populate.add_exercise(title='test E',question_list=['test Q'], course='TDTT3st')

    def test_stud_exercise_sel(self):
        # Login and start with the a course page
        self.client.login(username='theMan', password='thePa$$word')
        resp = self.client.get('/course/TDTT3st/')
        self.assertEqual(200, resp.status_code)
        # Select an exercise
        resp = self.client.post('/course/TDTT3st/', {'exercise_select': 'testE'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/exercise/testE/', resp.url)

    def test_lect_exercise_sel(self):
        # Login and start with the a course page
        self.client.login(username='theTeach', password='schooled')
        resp = self.client.get('/course/TDTT3st/')
        self.assertEqual(200, resp.status_code)
        # Select an exercise
        resp = self.client.post('/course/TDTT3st/', {'exercise_select': 'testE'})
        self.assertEqual(302, resp.status_code)
        self.assertEqual('/exercise/testE/', resp.url)