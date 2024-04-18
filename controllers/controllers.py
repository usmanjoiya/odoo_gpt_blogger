# -*- coding: utf-8 -*-
import itertools
import pytz
import babel.dates
from collections import OrderedDict
from odoo import http, fields, tools
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.tools.misc import get_lang
from odoo.tools import sql
from bs4 import BeautifulSoup


class OdooGptBlogger(http.Controller):

    # Odoo Base "website_blog" Module Function
    def nav_list(self, blog=None):
        dom = blog and [('blog_id', '=', blog.id)] or []
        if not request.env.user.has_group('website.group_website_designer'):
            dom += [('post_date', '<=', fields.Datetime.now())]
        groups = request.env['blog.post']._read_group_raw(
            dom,
            ['name', 'post_date'],
            groupby=["post_date"], orderby="post_date desc")
        for group in groups:
            (r, label) = group['post_date']
            start, end = r.split('/')
            group['post_date'] = label
            group['date_begin'] = start
            group['date_end'] = end

            locale = get_lang(request.env).code
            start = pytz.UTC.localize(fields.Datetime.from_string(start))
            tzinfo = pytz.timezone(request.context.get('tz', 'utc') or 'utc')

            group['month'] = babel.dates.format_datetime(start, format='MMMM', tzinfo=tzinfo, locale=locale)
            group['year'] = babel.dates.format_datetime(start, format='yyyy', tzinfo=tzinfo, locale=locale)

        return OrderedDict(
            (year, [m for m in months]) for year, months in itertools.groupby(groups, lambda g: g['year']))

    # Here is the function for generating the AI content
    def ai_content_generator(self, blog, blog_post, content_field, add_buttons=False):
        ai_soup = BeautifulSoup(content_field, 'html.parser')
        ai_document = ai_soup.findAll()

        seq = 1
        for tag in ai_document:
            if tag.name == 'p' and tag.attrs or tag.name != 'p':
                pass
                # if tag.name == 'li':
                #     i = 1
                #     while i < len(tag.contents):
                #         tag.contents[i] = 'Hiiiiii'
                #         i = i + 1

            else:
                ai_content = "On a clear night, you can observe breathtaking details of the lunar surface while simply stargazing in your backyard. As your passion for astronomy deepens, you'll discover numerous celestial bodies that captivate your interest. Yet, the moon often remains our initial astronomical love due to its exceptional status as a distant celestial object that orbits in close proximity to Earth, and moreover, because it's a place where humans have had the remarkable opportunity to set foot."
                new_tag = ai_soup.new_tag('p')
                new_tag.string = ai_content
                tag.replace_with(new_tag)

                if add_buttons:
                    button = ai_soup.new_tag('button')
                    button.string = "Update?"
                    button['class'] = 'btn btn-outline-success btn-floating btn-sm'
                    button['id'] = 'update_button_' + str(seq)
                    button['onclick'] = 'myFun(this)'
                    button['data-blog-id'] = blog.id
                    button['data-blog-post-id'] = blog_post.id
                    new_tag.insert(0, button)
                    # new_tag.insert_after(button)
                seq = seq + 1

        modified_content = ai_soup.prettify()
        return modified_content

    # Controller for Blog Content vs AI Content
    @http.route('/gptBlog/<int:blog>/<int:blog_post>',
                auth='public', type='http', website=True)
    def ai_content_comparison_button(self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post):
        blog = request.env['blog.blog'].search([("id", '=', blog)])
        blog_post = request.env['blog.post'].search([("id", '=', blog_post)])
        BlogPost = request.env['blog.post']
        date_begin, date_end = post.get('date_begin'), post.get('date_end')

        domain = request.website.website_domain()
        blogs = blog.search(domain, order="create_date, id asc")

        tag = None
        if tag_id:
            tag = request.env['blog.tag'].browse(int(tag_id))
        blog_url = QueryURL('', ['blog', 'tag'], blog=blog_post.blog_id, tag=tag, date_begin=date_begin,
                            date_end=date_end)

        if not blog_post.blog_id.id == blog.id:
            return request.redirect("/blog/%s/%s" % (slug(blog_post.blog_id), slug(blog_post)), code=301)

        tags = request.env['blog.tag'].search([])

        # Find next Post
        blog_post_domain = [('blog_id', '=', blog.id)]
        if not request.env.user.has_group('website.group_website_designer'):
            blog_post_domain += [('post_date', '<=', fields.Datetime.now())]

        all_post = BlogPost.search(blog_post_domain)

        if blog_post not in all_post:
            return request.redirect("/blog/%s" % (slug(blog_post.blog_id)))

        # should always return at least the current post
        all_post_ids = all_post.ids
        current_blog_post_index = all_post_ids.index(blog_post.id)
        nb_posts = len(all_post_ids)
        next_post_id = all_post_ids[(current_blog_post_index + 1) % nb_posts] if nb_posts > 1 else None
        next_post = next_post_id and BlogPost.browse(next_post_id) or False

        # Custom code starts from here
        # if blog_post.is_ai_content_generated:
        #     blog_post.is_ai_content_generated = True

        blog_post.ai_content_with_buttons = blog_post.content
        blog_post.ai_content = blog_post.content

        # Here we call the function for generating AI Content
        blog_post.ai_content_with_buttons = self.ai_content_generator(blog, blog_post,
                                                                      blog_post.ai_content_with_buttons, True)
        blog_post.ai_content = self.ai_content_generator(blog, blog_post, blog_post.ai_content)

        values = {
            'tags': tags,
            'tag': tag,
            'blog': blog,
            'blog_post': blog_post,
            'blogs': blogs,
            'main_object': blog_post,
            'nav_list': self.nav_list(blog),
            'enable_editor': enable_editor,
            'next_post': next_post,
            'date': date_begin,
            'blog_url': blog_url,
        }
        # Calling our AI and Blog Comparison Template
        response = request.render("odoo_gpt_blogger.blog_post_complete_inherit", values)

        if blog_post.id not in request.session.get('posts_viewed', []):
            if sql.increment_fields_skiplock(blog_post, 'visits'):
                if not request.session.get('posts_viewed'):
                    request.session['posts_viewed'] = []
                request.session['posts_viewed'].append(blog_post.id)
                request.session.modified = True
        return response

    # This function is for updating AI Content in Paragraphs Chunks of blog
    @http.route('/update/blogBlock/', auth='public', type='json')
    def update_blog_block(self, **kw):
        button_id = kw.get('button_id')[-1]
        ai_content = kw.get('ai_content')
        blog_id = kw.get('blog_id')
        blog_post_id = kw.get('blog_post_id')
        blog = request.env['blog.blog'].search([("id", '=', blog_id)])
        blog_post = request.env['blog.post'].search([("id", '=', blog_post_id)])

        # Updating Paragraphs of AI content using Beautiful Soap Library
        blog_soup = BeautifulSoup(blog_post.content, 'html.parser')
        blog_document = blog_soup.findAll()
        seq = 1
        for tag in blog_document:
            if tag.name == 'p' and tag.attrs or tag.name != 'p':
                pass
            else:
                if seq == int(button_id):
                    new_tag = blog_soup.new_tag('p')
                    new_tag.string = ai_content
                    tag.replace_with(new_tag)
                    modified_content = blog_soup.prettify()
                    blog_post.content = modified_content
                    break
                else:
                    seq = seq + 1
        return {'message': 'wow'}

    # Base controller for Blog Page
    @http.route(['''/blog/<model("blog.blog"):blog>/<model("blog.post", "[('blog_id','=',blog.id)]"):blog_post>''', ],
                type='http', auth="public", website=True, sitemap=True)
    def blog_post(self, blog, blog_post, all_content_update=False, tag_id=None, page=1, enable_editor=None, **post):
        BlogPost = request.env['blog.post']
        date_begin, date_end = post.get('date_begin'), post.get('date_end')

        # Update the overall blog with AI content
        if all_content_update:
            blog_post.content = blog_post.ai_content
            # blog_post.is_ai_content_updated = True

        domain = request.website.website_domain()
        blogs = blog.search(domain, order="create_date, id asc")

        tag = None
        if tag_id:
            tag = request.env['blog.tag'].browse(int(tag_id))
        blog_url = QueryURL('', ['blog', 'tag'], blog=blog_post.blog_id, tag=tag, date_begin=date_begin,
                            date_end=date_end)

        if not blog_post.blog_id.id == blog.id:
            return request.redirect("/blog/%s/%s" % (slug(blog_post.blog_id), slug(blog_post)), code=301)

        tags = request.env['blog.tag'].search([])

        # Find next Post
        blog_post_domain = [('blog_id', '=', blog.id)]
        if not request.env.user.has_group('website.group_website_designer'):
            blog_post_domain += [('post_date', '<=', fields.Datetime.now())]

        all_post = BlogPost.search(blog_post_domain)

        if blog_post not in all_post:
            return request.redirect("/blog/%s" % (slug(blog_post.blog_id)))

        # should always return at least the current post
        all_post_ids = all_post.ids
        current_blog_post_index = all_post_ids.index(blog_post.id)
        nb_posts = len(all_post_ids)
        next_post_id = all_post_ids[(current_blog_post_index + 1) % nb_posts] if nb_posts > 1 else None
        next_post = next_post_id and BlogPost.browse(next_post_id) or False

        values = {
            'tags': tags,
            'tag': tag,
            'blog': blog,
            'blog_post': blog_post,
            'blogs': blogs,
            'main_object': blog_post,
            'nav_list': self.nav_list(blog),
            'enable_editor': enable_editor,
            'next_post': next_post,
            'date': date_begin,
            'blog_url': blog_url
        }
        response = request.render("website_blog.blog_post_complete", values)

        if blog_post.id not in request.session.get('posts_viewed', []):
            if sql.increment_fields_skiplock(blog_post, 'visits'):
                if not request.session.get('posts_viewed'):
                    request.session['posts_viewed'] = []
                request.session['posts_viewed'].append(blog_post.id)
                request.session.modified = True
        return response
