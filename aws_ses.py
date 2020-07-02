import boto.ses
from jinja2 import Environment, PackageLoader
import multiscript_config as msc

class Email(object):
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None

    def _render(self, filename, context):
        template = env.get_template(filename)
        return template.render(name = 'Nikhil', linklist = context)

    def html(self, filename, context):
        self._html = self._render(filename, context)

    def send(self, from_addr=None):
        body = self._html
        if isinstance(self.to, str):
            self.to = [self.to]
        if not from_addr:
            from_addr = 'support@easemylearning.com'
        if not self._html and not self._text:
            raise Exception('You must provide a text or html body.')
        if not self._html:
            body = self._text
        connection = boto.ses.connect_to_region( msc.AWS_REGION,aws_access_key_id=msc.AWS_ACCESS_KEY, 
            aws_secret_access_key=msc.AWS_SECRET_KEY )
        return connection.send_email( from_addr, self.subject, None, self.to,
            text_body=self._text, html_body=self._html )

env = Environment(loader=PackageLoader('aws_ses', 'templates'))
email = Email(to='niknair31898@gmail.com', subject='AWS SES Test')
linklist = ['1','2','3']
email.html('email.html', linklist)
email.send()