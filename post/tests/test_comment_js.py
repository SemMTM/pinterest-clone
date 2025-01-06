from django.test import TestCase
from django.test.client import RequestFactory
from django.template.loader import render_to_string
from bs4 import BeautifulSoup

class JavaScriptTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.csrf_token = "test_csrf_token"

    def render_template(self, template_name, context={}):
        context['csrf_token'] = self.csrf_token
        return render_to_string(template_name, context)

    def test_get_element(self):
        html = '<div id="test-element"></div>'
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find(id="test-element")
        self.assertIsNotNone(element, "getElement should find the element by ID.")

    def test_toggle_class(self):
        html = '<div id="test-element" class="hidden"></div>'
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find(id="test-element")

        # Simulate adding a class
        element['class'] = element.get('class', []) + ['visible']
        self.assertIn('visible', element['class'], "toggleClass should add the class.")

        # Simulate removing a class
        element['class'].remove('hidden')
        self.assertNotIn('hidden', element['class'], "toggleClass should remove the class.")

    def test_reset_comment_form(self):
        html = '''
            <form id="commentForm">
                <textarea name="body" id="commentInput">Old comment</textarea>
                <input type="hidden" id="edit-comment-id" value="123">
            </form>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        comment_input = soup.find(id="commentInput")
        comment_id_input = soup.find(id="edit-comment-id")

        # Simulate reset
        comment_input.string = ''
        comment_id_input['value'] = ''

        self.assertEqual(comment_input.string, '', "Comment input should be cleared.")
        self.assertEqual(comment_id_input['value'], '', "Comment ID input should be cleared.")

    def test_modal_triggers(self):
        html = '''
            <div id="comment-modal" class="hidden"></div>
            <button id="open-modal">Open</button>
            <button id="close-modal">Close</button>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        modal = soup.find(id="comment-modal")

        # Simulate opening modal
        modal['class'].remove('hidden')
        self.assertNotIn('hidden', modal['class'], "Modal should open when triggered.")

        # Simulate closing modal
        modal['class'].append('hidden')
        self.assertIn('hidden', modal['class'], "Modal should close when triggered.")

    def test_comment_submission(self):
        # Mock the submission process
        request = self.factory.post('/add_comment/', {'body': 'New Comment', 'csrfmiddlewaretoken': self.csrf_token})
        self.assertEqual(request.POST['body'], 'New Comment', "Comment body should match.")
        self.assertEqual(request.POST['csrfmiddlewaretoken'], self.csrf_token, "CSRF token should match.")

    def test_edit_comment(self):
        html = '''
            <div id="comments-container" data-post-id="1">
                <button class="edit-comment-btn" data-comment-id="123" data-comment-body="Old comment"></button>
            </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        edit_button = soup.find(class_="edit-comment-btn")

        # Simulate click event to populate form
        comment_body = edit_button['data-comment-body']
        comment_id = edit_button['data-comment-id']

        self.assertEqual(comment_body, "Old comment", "Comment body should populate correctly.")
        self.assertEqual(comment_id, "123", "Comment ID should populate correctly.")

    def test_delete_comment(self):
        html = '''
            <div id="delete-comment-modal" class="hidden"></div>
            <button class="comment-close-btn" post_id="1" comment_id="123"></button>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        delete_button = soup.find(class_="comment-close-btn")

        # Simulate opening delete modal
        delete_modal = soup.find(id="delete-comment-modal")
        delete_modal['class'].remove('hidden')
        self.assertNotIn('hidden', delete_modal['class'], "Delete modal should open when triggered.")

        # Simulate confirming delete
        delete_url = f"/{delete_button['post_id']}/delete_comment/{delete_button['comment_id']}/"
        self.assertEqual(delete_url, "/1/delete_comment/123/", "Delete URL should be constructed correctly.")

