from .models import Projeto, ProjetoArea, ProjetoIntegrante, path_and_rename_projeto
from mainApp.models import Area
from .forms import ProjectCreateForm, UserEditForm, ProjectEditForm
from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from .views import  projects, home, create_project, profile, edit_profile
from django.urls import resolve
import copy

TEACHER = ('jonas.teixeira', 'senhajonas')
OTHER_TEACHER = ('william.garcia', 'senhawilliam')
STUDENT = ('marquinhos', 'senhamarquinhos')
ADMIN = ('admin', 'senhaadmin')

SAMPLE_PROJECT = {
    'titulo': 'Meu Projeto',
    'descricao': 'Minha Descricao',
    'sigla': 'MP',
    'inicio': '2019-01-01',
    'termino': '2020-05-05',
    'agencia': 'CNPq',
    'programa': 'Meu Programa',
    'natureza': 'Natureza',
    'situacao': 'EM PROGRESSO',
    'processo': '12345679',
    'resolucao': '12344-ABC'
}

SAMPLE_PROJECT2 = {
    'titulo': 'Meu Projeto2',
    'descricao': 'Minha Descricao2',
    'sigla': 'MP2',
    'inicio': '2019-01-02',
    'termino': '2020-05-06',
    'agencia': 'CNPq2',
    'programa': 'Meu Programa2',
    'natureza': 'Natureza2',
    'situacao': 'EM PROGRESSO2',
    'processo': '123456792',
    'resolucao': '12344-ABC-2'
}

SAMPLE_USER_FORM = {
    'first_name': 'Marinho',
    'last_name': 'Brigs',
    'email': 'marinhobrigs@gmail.com',
    'phone': '31993844822'
}

SAMPLE_AREA = {
    'nome': 'Computer Vision'
}

SAMPLE_AREA_2 = {
    'nome': 'Data Mining'
}

class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.teacher = CustomUser.objects.create_user(
            username=TEACHER[0],
            first_name='Jonas Teixeira',
            last_name='da Silva',
            email='jonas@gmail.com',
            phone='31972334125',
            profile='PROFESSOR',
            title='prof',
            is_active=True,
            is_admin=False
        )

        self.other_teacher = CustomUser.objects.create_user(
            username=OTHER_TEACHER[0],
            first_name='William',
            last_name='Garcia',
            email='williamg@gmail.com',
            phone='31975534125',
            profile='PROFESSOR',
            title='prof',
            is_active=True,
            is_admin=False
        )

        self.student = CustomUser.objects.create_user(
            username=STUDENT[0],
            first_name='Marcos',
            last_name='Lucca',
            email='marcolucca@gmail.com',
            phone='31972534125',
            profile='ESTUDANTE',
            title='grad-cc',
            is_active=True,
            is_admin=False
        )

        self.admin = CustomUser.objects.create_user(
            username=ADMIN[0],
            first_name='Admin',
            last_name='',
            email='admin@gmail.com',
            phone='31972334125',
            profile='',
            title='admin',
            is_active=True,
            is_admin=True
        )

        self.teacher.set_password(TEACHER[1])
        self.student.set_password(STUDENT[1])
        self.admin.set_password(ADMIN[1])

        self.teacher.save()
        self.student.save()
        self.admin.save()
    def test_area_attributes(self):
        self.assertTrue(hasattr(Area, 'nome'))

    def test_projeto_integrante_attributes(self):
        self.assertTrue(hasattr(ProjetoIntegrante, 'projeto'))
        self.assertTrue(hasattr(ProjetoIntegrante, 'integrante'))

    def test_projeto_area_attributes(self):
        self.assertTrue(hasattr(ProjetoArea, 'projeto'))
        self.assertTrue(hasattr(ProjetoArea, 'area'))

    def test_projeto_attributes(self):
        self.assertTrue(hasattr(Projeto, 'titulo'))
        self.assertTrue(hasattr(Projeto, 'descricao'))
        self.assertTrue(hasattr(Projeto, 'inicio'))
        self.assertTrue(hasattr(Projeto, 'termino'))
        self.assertTrue(hasattr(Projeto, 'coordenador'))
        self.assertTrue(hasattr(Projeto, 'agencia'))
        self.assertTrue(hasattr(Projeto, 'programa'))
        self.assertTrue(hasattr(Projeto, 'natureza'))
        self.assertTrue(hasattr(Projeto, 'situacao'))
        self.assertTrue(hasattr(Projeto, 'processo'))
        self.assertTrue(hasattr(Projeto, 'resolucao'))

    def test_user_attributes(self):
        self.assertTrue(hasattr(CustomUser, 'first_name'))
        self.assertTrue(hasattr(CustomUser, 'last_name'))
        self.assertTrue(hasattr(CustomUser, 'email'))
        self.assertTrue(hasattr(CustomUser, 'phone'))
        self.assertTrue(hasattr(CustomUser, 'profile'))
        self.assertTrue(hasattr(CustomUser, 'title'))
        self.assertTrue(hasattr(CustomUser, 'is_active'))
        self.assertTrue(hasattr(CustomUser, 'is_admin'))

    def test_profile_accessible_by_teacher(self):
        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_accessible_by_student(self):
        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_accessible_by_teacher(self):
        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_accessible_by_student(self):
        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_students_can_edit_their_profiles(self):
        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.post(reverse('edit_profile'), data=SAMPLE_USER_FORM)

        self.assertEqual(response.status_code, 302)

    def test_teachers_can_edit_their_profiles(self):
        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.post(reverse('edit_profile'), data=SAMPLE_USER_FORM)

        self.assertEqual(response.status_code, 302)

    def test_edit_user_form_works_for_student(self):
        self.client.login(username=STUDENT[0], password=STUDENT[1])
        self.client.post(reverse('edit_profile'), data=SAMPLE_USER_FORM)

        student = CustomUser.objects.get(pk=self.student.pk)
        updated_student = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'phone': student.phone
        }

        self.assertEqual(updated_student, SAMPLE_USER_FORM)

    def test_edit_user_form_works_for_teacher(self):
        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.post(reverse('edit_profile'), data=SAMPLE_USER_FORM)

        teacher = CustomUser.objects.get(pk=self.teacher.pk)
        updated_teacher = {
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'email': teacher.email,
            'phone': teacher.phone
        }

        self.assertEqual(updated_teacher, SAMPLE_USER_FORM)

    def test_projects_accessible_by_teacher(self):
        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)

    def test_projects_accessible_by_student(self):
        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)

    def test_project_creation_accessible_by_teacher(self):
        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('create_project'))
        self.assertEqual(response.status_code, 200)

    def test_project_creation_inaccessible_by_student(self):
        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.get(reverse('create_project'))
        self.assertRedirects(response, reverse('admin:index'), target_status_code=302)

    def test_user_edit_form_validation(self):
        form = UserEditForm(SAMPLE_USER_FORM)
        self.assertTrue(form.is_valid())

    def test_project_creation_form_validation(self):
        form = ProjectCreateForm(SAMPLE_PROJECT, owner_pk=self.teacher.pk)
        self.assertTrue(form.is_valid())

    def test_project_removal_works_for_teacher(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)

        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('delete_project', kwargs={'pk': project.pk}))

        self.assertRaises(Projeto.DoesNotExist, Projeto.objects.get, coordenador=project.pk)

    def test_project_removal_does_not_work_for_student(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)

        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.get(reverse('delete_project', kwargs={'pk': project.pk}))

        self.assertRaises(Projeto.DoesNotExist, Projeto.objects.get, coordenador=project.pk)

    def test_project_removal_does_not_work_for_other_teacher(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.other_teacher)

        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('delete_project', kwargs={'pk': project.pk}))

        self.assertEqual(response.status_code, 302)

    def test_edit_project_accessible_by_teacher(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)

        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('edit_project', kwargs={ 'pk': project.pk }))
        self.assertEqual(response.status_code, 200)

    def test_edit_project_inaccessible_by_student(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)

        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.get(reverse('edit_project', kwargs={ 'pk': project.pk }))
        self.assertNotEqual(response.status_code, 200)

    def test_project_edit_does_not_work_for_other_teacher(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.other_teacher)

        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.get(reverse('edit_project', kwargs={ 'pk': project.pk }))
        self.assertRedirects(response, reverse('admin:index'), target_status_code=302)

    def test_project_edit_form_validation(self):
        edited_project = copy.deepcopy(SAMPLE_PROJECT)

        edited_project['situacao'] = "CONCLUÍDO"
        form = ProjectEditForm(edited_project)
        self.assertTrue(form.is_valid())

    def test_project_edit_form_should_contain_title(self):
        edited_project = ProjectTestCase.generate_custom_form(SAMPLE_PROJECT, ['titulo'])

        form = ProjectEditForm(edited_project)
        self.assertFalse(form.is_valid())

    def test_project_edit_form_should_contain_begin_date(self):
        edited_project = ProjectTestCase.generate_custom_form(SAMPLE_PROJECT, ['inicio'])
        edited_project = copy.deepcopy(SAMPLE_PROJECT)
        del edited_project['titulo']

        form = ProjectEditForm(edited_project)
        self.assertFalse(form.is_valid())

    def test_user_edit_form_should_contain_first_name(self):
        edited_user = ProjectTestCase.generate_custom_form(SAMPLE_USER_FORM, ['first_name'])

        form = UserEditForm(edited_user)
        self.assertFalse(form.is_valid())

    def test_user_edit_form_should_contain_last_name(self):
        edited_user = ProjectTestCase.generate_custom_form(SAMPLE_USER_FORM, ['last_name'])

        form = UserEditForm(edited_user)
        self.assertFalse(form.is_valid())

    def test_user_edit_form_should_contain_email(self):
        edited_user = ProjectTestCase.generate_custom_form(SAMPLE_USER_FORM, ['email'])

        form = UserEditForm(edited_user)
        self.assertFalse(form.is_valid())

    def test_logout_should_redirect(self):
        self.client.login(username=STUDENT[0], password=STUDENT[1])
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_project_str_should_be_the_title(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        self.assertEqual(str(project), 'Meu Projeto')

    def test_admin_page_accessible_to_admin(self):
        self.client.login(username=ADMIN[0], password=ADMIN[1])
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_area_str_should_be_area_name(self):
        area = Area.objects.create(**SAMPLE_AREA)

        self.assertEqual(str(area), 'Computer Vision')

    def test_project_area_str_should_be_area_name(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        area = Area.objects.create(**SAMPLE_AREA)
        project_area = ProjetoArea.objects.create(projeto=project, area=area)

        self.assertEqual(str(project_area), 'Computer Vision')

    def test_project_member_str_should_be_member_and_project_name(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project_member = ProjetoIntegrante.objects.create(projeto=project, integrante=self.student)

        self.assertEqual(str(project_member), 'Marcos Lucca - Meu Projeto')

    def test_upload_file_name(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        path = path_and_rename_projeto(project, '.png')

        self.assertEqual(path, f'imagem_projeto/2019/{project.pk}.png')


    def test_any_user_can_only_see_projects_the_user_participates_of_or_coordinate(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project2 = Projeto.objects.create(**SAMPLE_PROJECT2, coordenador=self.other_teacher)

        ProjetoIntegrante.objects.create(projeto=project2, integrante=self.teacher)

        user_projects = list(Projeto.objects.filter(coordenador=self.teacher))
        projects_user_is_in = list(map(
            lambda x: x.projeto,
            ProjetoIntegrante.objects.filter(integrante=self.teacher)))

        teacher_projects = set(user_projects + projects_user_is_in)

        self.assertEqual(teacher_projects, set([project, project2]))


    def test_teachers_can_edit_their_projects(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)

        self.client.login(username=TEACHER[0], password=TEACHER[1])
        response = self.client.post(reverse('edit_project', kwargs={ 'pk': project.pk }), data=SAMPLE_PROJECT2)

        self.assertEqual(response.status_code, 302)

    def test_teachers_can_create_projects(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)

        self.assertIsNotNone(Projeto.objects.filter(pk=project.pk))


    def test_list_of_owned_projects_is_succesfully_returned_for_teacher(self):
        project1 = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project2 = Projeto.objects.create(**SAMPLE_PROJECT2, coordenador=self.teacher)

        user_owned_projects = list(Projeto.objects.filter(coordenador=self.teacher))

        self.assertEqual(user_owned_projects, [project1, project2])

    def test_list_of_projects_user_is_in_is_succesfully_returned_for_student(self):
        project1 = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project2 = Projeto.objects.create(**SAMPLE_PROJECT2, coordenador=self.teacher)

        ProjetoIntegrante.objects.create(projeto=project1, integrante=self.student)
        ProjetoIntegrante.objects.create(projeto=project2, integrante=self.student)

        projects_student_is_in = list(map(
            lambda x: x.projeto,
            ProjetoIntegrante.objects.filter(integrante=self.student)
        ))

        self.assertEqual(projects_student_is_in, [project1, project2])

    def test_project_objects_are_unique_even_with_the_same_info(self):
        project1 = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project2 = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)

        self.assertFalse(project1 == project2)

    def test_project_object_supports_inequality(self):
        project1 = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project2 = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.student)

        self.assertTrue(project1 != project2)

    def test_project_area_objects_are_unique_even_with_the_same_info(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        area = Area.objects.create(**SAMPLE_AREA)
        project_area1 = ProjetoArea.objects.create(projeto=project, area=area)
        project_area2 = ProjetoArea.objects.create(projeto=project, area=area)

        self.assertFalse(project_area1 == project_area2)

    def test_project_area_object_supports_inequality(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project2 = Projeto.objects.create(**SAMPLE_PROJECT2, coordenador=self.teacher)
        area = Area.objects.create(**SAMPLE_AREA)
        project_area1 = ProjetoArea.objects.create(projeto=project, area=area)
        project_area2 = ProjetoArea.objects.create(projeto=project2, area=area)

        self.assertTrue(project_area1 != project2)

    def test_project_member_objects_are_unique_even_with_the_same_info(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project_member1 = ProjetoIntegrante.objects.create(projeto=project, integrante=self.student)
        project_member2 = ProjetoIntegrante.objects.create(projeto=project, integrante=self.student)

        self.assertFalse(project_member1 == project_member2)

    def test_project_member_object_supports_inequality(self):
        project = Projeto.objects.create(**SAMPLE_PROJECT, coordenador=self.teacher)
        project2 = Projeto.objects.create(**SAMPLE_PROJECT2, coordenador=self.teacher)
        project_member1 = ProjetoIntegrante.objects.create(projeto=project, integrante=self.student)
        project_member2 = ProjetoIntegrante.objects.create(projeto=project, integrante=self.student)

        self.assertTrue(project_member1 != project_member2)

    def test_area_objects_are_unique_even_with_the_same_info(self):
        area = Area.objects.create(**SAMPLE_AREA)
        area2 = Area.objects.create(**SAMPLE_AREA)

        self.assertFalse(area == area2)

    def test_area_object_supports_inequality(self):
        area = Area.objects.create(**SAMPLE_AREA)
        area2 = Area.objects.create(**SAMPLE_AREA_2)

        self.assertTrue(area != area2)

    def test_area_objects_pks_are_unique(self):
        pks = [x.pk for x in Area.objects.all()]

        self.assertEqual(len(pks), len(set(pks)))

    def test_project_objects_pks_are_unique(self):
        pks = [x.pk for x in Projeto.objects.all()]

        self.assertEqual(len(pks), len(set(pks)))

    def test_project_area_objects_pks_are_unique(self):
        pks = [x.pk for x in ProjetoArea.objects.all()]

        self.assertEqual(len(pks), len(set(pks)))

    def test_project_members_objects_pks_are_unique(self):
        pks = [x.pk for x in ProjetoIntegrante.objects.all()]

        self.assertEqual(len(pks), len(set(pks)))

    def test_projects_url_resolves_projects_view(self):
        view = resolve('/projectsApp/projects/')
        self.assertEquals(view.func, projects)

    def test_create_project_url_resolves_create_project_view(self):
        view = resolve('/projectsApp/projects/create')
        self.assertEquals(view.func, create_project)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_profile_url_resolves_profile_view(self):
        view = resolve('/projectsApp/profile/')
        self.assertEquals(view.func, profile)

    def test_edit_profile_url_resolves_edit_profile_view(self):
        view = resolve('/projectsApp/profile/edit')
        self.assertEquals(view.func, edit_profile)

    # --------- Auxiliar methods ---------
    @staticmethod
    def generate_custom_form(base_form, fields_to_delete):
        custom_form = copy.deepcopy(base_form)

        for field in fields_to_delete:
            if field in custom_form:
                del custom_form[field]

        return custom_form
