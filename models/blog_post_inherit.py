from odoo import fields, models, _,api
from odoo.tools.translate import html_translate


class BlogPostInherit(models.Model):
    _inherit = "blog.post"

    # Here is the default function for Ai content Html field
    def get_ai_content(self):
        self.ai_content = '''<p>Hello</p>'''

    # Here is the fields for our inherited model "blog.post"
    ai_content = fields.Html('AI Content', translate=html_translate, sanitize=False, default=get_ai_content)
    ai_content_with_buttons = fields.Html('AI Content with update buttons', translate=html_translate, sanitize=False, default=get_ai_content)
    is_ai_content_generated = fields.Boolean('Is AI Content Generated', default=False)
    # is_ai_content_updated = fields.Boolean('Is AI Content Updated', default=False)
