import boto.ses
import multiscript_config as msc

class Email(object):
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None
        self._format = 'html'
    def html(self, html):
        self._html = html
    def text(self, text):
        self._text = text
    def send(self, from_addr=None):
        body = self._html
        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
            from_addr = 'me@example.com'
        if not self._html and not self._text:
            raise Exception('You must provide a text or html body.')
        if not self._html:
            self._format = 'text'
            body = self._text
        connection = boto.ses.connect_to_region( 'us-east-1', aws_access_key_id=msc.AWS_ACCESS_KEY, 
            aws_secret_access_key=msc.AWS_SECRET_KEY )
        return connection.send_email( from_addr, self.subject, None, self.to, format=self._format, 
            text_body=self._text, html_body=self._html )

email = Email(to='niknair31898@gmail.com', subject='You are HTML Awesome')
email.text('This is a text body. Foo bar.')
# email.html('<html><body>This is a text body. <strong>Foo bar.</strong></body></html>')  # Optional
email.send()