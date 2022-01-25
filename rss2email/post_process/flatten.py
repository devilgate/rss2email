# Copyright (C) 2013-2021 Arun Persaud <apersaud@lbl.gov>
#                         Etienne Millon <me@emillon.org>
#                         Léo Gaspard <leo@gaspard.io>
#                         Profpatsch <mail@profpatsch.de>
#                         W. Trevor King <wking@tremily.us>
#                         Martin McCallion <martin@devilgate.org>
#
# This file is part of rss2email.
#
# rss2email is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) version 3 of
# the License.
#
# rss2email is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# rss2email.  If not, see <http://www.gnu.org/licenses/>.

"""A hook for converting digest messages from one message with all the
   submessages as attachments into a single message with the submessages
   in the body.
"""

from email.mime.multipart import MIMEMultipart


def flatten_message(message, **kwargs):
    """Flatten the message, converting attachments into body content.
    """
    if message.is_multipart():
        new_message = MIMEMultipart()
        new_message.set_charset(message.get_charset())
        new_message['Subject'] = message['Subject']
        new_message['From'] = message['From']
        new_message['To'] = message['To']
        new_message['Message-ID'] = message['Message-ID']
        new_message['User-Agent'] = message['User-Agent']
        new_message['List-ID'] = message['List-ID']
        new_message['List-Post'] = message['List-Post']
        new_message['X-RSS-Feed'] = message['X-RSS-Feed']
        new_message['X-RSS-ID'] = message['X-RSS-ID']
        new_message['X-RSS-URL'] = message['X-RSS-URL']
        new_message['X-RSS-TAGS'] = message['X-RSS-TAGS']

        payload = ''
        for part in message.walk():
            if part.get_content_type() in ('text/plain', 'text/html', 'message/rfc822'):
                payload = payload + '\n\n' + part.get_body()
        new_message.set_payload(payload)

    else:
        new_message = message
    return new_message
