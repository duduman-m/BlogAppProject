from django.contrib.auth.models import Permission
from django.test import TestCase, Client

from articles.models import Article
from users.models import Writer


class ApprovalViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "TestCasePass"
        self.editor = Writer.objects.create_user(
            username="editor", first_name="Test",
            last_name="Editor", is_editor=True, password=self.password)
        self.not_editor = Writer.objects.create_user(
            username="not_editor", first_name="Test",
            last_name="Not Editor", is_editor=False, password=self.password)
        self.instance = Article.objects.create(
            title="Test Case", content="Test Content", written_by=self.editor)

    def test_access_not_with_editor(self):
        self.client.login(username="not_editor", password=self.password)
        response = self.client.get('/article-approval/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        for mess in response.context['messages']:
            self.assertEqual(mess.message, "You are not an editor")

    def test_access_with_editor(self):
        self.editor.user_permissions.set(Permission.objects.all())
        self.client.login(username="editor", password=self.password)
        response = self.client.get('/article-approval/', follow=True)
        self.assertIn(self.instance, response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/approval.html")

    def test_access_with_editor_without_permission(self):
        self.client.login(username="editor", password=self.password)
        response = self.client.get('/article-approval/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        for mess in response.context['messages']:
            self.assertEqual(mess.message, "You do not have the permission to "
                                           "approve/reject articles")


class AddArticleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "TestCasePass"
        self.editor = Writer.objects.create_user(
            username="editor", first_name="Test", last_name="Editor",
            is_editor=True, password=self.password)

    def test_access_with_permission(self):
        self.editor.user_permissions.set(Permission.objects.all())
        self.client.login(username="editor", password=self.password)
        response = self.client.get('/article/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/add.html")

    def test_post_with_no_data(self):
        self.editor.user_permissions.set(Permission.objects.all())
        self.client.login(username="editor", password=self.password)
        response = self.client.post('/article/add/', {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title',
                             'This field is required.')
        self.assertFormError(response, 'form', 'content',
                             'This field is required.')

    def test_post_with_data(self):
        self.editor.user_permissions.set(Permission.objects.all())
        self.client.login(username="editor", password=self.password)
        data = {
            'title': 'Test Case Article',
            'content': 'Content'
        }
        response = self.client.post('/article/add/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        Article.objects.filter(title='Test Case Article').first().delete()

    def test_access_without_permission(self):
        self.client.login(username="editor", password=self.password)
        response = self.client.get('/article/add/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        for mess in response.context['messages']:
            self.assertEqual(mess.message, "You do not have the permission "
                                           "to add articles")


class EditArticleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "TestCasePass"
        self.editor = Writer.objects.create_user(
            username="editor", first_name="Test", last_name="Editor",
            is_editor=True, password=self.password)
        self.not_editor = Writer.objects.create_user(
            username="not_editor", first_name="Test", last_name="Not Editor",
            is_editor=False, password=self.password)
        self.instance = Article.objects.create(
            title="Test Case", content="Test Content", written_by=self.editor)

    def test_access_with_permission(self):
        self.editor.user_permissions.set(Permission.objects.all())
        self.client.login(username="editor", password=self.password)
        response = self.client.get(
            f'/article/{self.instance.pk}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/edit.html")

    def test_post_with_no_data(self):
        self.editor.user_permissions.set(Permission.objects.all())
        self.client.login(username="editor", password=self.password)
        response = self.client.post(
            f'/article/{self.instance.pk}/', {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'title', 'This field is required.')
        self.assertFormError(
            response, 'form', 'content', 'This field is required.')

    def test_post_with_data(self):
        self.editor.user_permissions.set(Permission.objects.all())
        self.client.login(username="editor", password=self.password)
        data = {
            'title': 'Test Case Article',
            'content': 'Content'
        }
        response = self.client.post(
            f'/article/{self.instance.pk}/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(
            Article.objects.get(title='Test Case Article'), self.instance)

    def test_access_without_permission(self):
        self.client.login(username="editor", password=self.password)
        response = self.client.get(
            f'/article/{self.instance.pk}/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        for mess in response.context['messages']:
            self.assertEqual(mess.message, "You do not have the permission "
                                           "to edit articles")
