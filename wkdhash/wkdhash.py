# MIT License
#
# Copyright (c) 2025 Gregor Vollmer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import zbase32
from hashlib import sha1


# Match User ID in the form 'Janette Doe <j.doe@example.com>'
reUSER_ID = re.compile(r"^[^<]*<(([^@]+)@([^@>]+))>")


def mailbox_from_userid(userid: str, subaddress: bool = False) -> str:
    # Closely implements algorithm from:
    # gnupg/common/mbox-util.c:mailbox_from_userid()
    m = reUSER_ID.match(userid)
    if m:
        mailbox = m.group(1)
    elif userid.count("@") == 1:
        mailbox = userid
    else:
        raise ValueError(f"User ID {repr(userid)} has invalid format")
    local_part, _, domain = mailbox.partition("@")
    if not local_part:
        raise ValueError(f"User ID {repr(userid)} mailbox local-part is empty")
    if not domain:
        raise ValueError(f"User ID {repr(userid)} mailbox domain is empty")
    if domain.startswith("..") or domain.endswith("."):
        raise ValueError(f"Domain {repr(domain)} is invalid")
    if " " in mailbox:
        raise ValueError("Mailbox must not contain spaces")
    if subaddress:
        sub_addresses = local_part.split("+")
        if len(sub_addresses) == 2:
            mailbox = sub_addresses[1] + "@" + domain
    return mailbox


def userid_to_wkd_hash(userid: str, include_domain: bool = False) -> str:
    # Returns a tuple (hash, domain) for the given userid
    mailbox = mailbox_from_userid(userid)
    local_part, _, domain = mailbox.partition("@")
    # GnuPG uses a very simple implementation to convert the local part to a
    # lower case string, which completely ignores any non-ASCII characters.
    # Therefore, we apply the lower()-operation only to characters with a
    # Unicode code-point below 128.
    # Yikes.
    local_part_lower = "".join(
            map(
                lambda char: char if ord(char) > 127 else char.lower(),
                local_part
            ))
    hu = zbase32.encode(sha1(local_part_lower.encode("utf-8")).digest())
    if include_domain:
        return hu + "@" + domain
    return hu
