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

import unittest
from typing import Self
from wkdhash import mailbox_from_userid


class TestUserIdToMailbox(unittest.TestCase):
    def test_valid_userids(self: Self) -> None:
        self.assertEqual(
                mailbox_from_userid("Janette Doe <j.doe@example.com>"),
                "j.doe@example.com")
        self.assertEqual(
                mailbox_from_userid(
                    "Lorem Ipsom dorosit <lid@sub.foo.bar.example.com>"),
                "lid@sub.foo.bar.example.com")

    def test_mailbox_only(self: Self) -> None:
        mailboxes = (
                "j.doe@example.com",
                "lid@sub.foo.bar.example.com",
            )
        for mbox in mailboxes:
            self.assertEqual(
                    mailbox_from_userid(mbox),
                    mbox)

    def test_invalid_user_ids(self: Self) -> None:
        test_data_list = (
                "John Doe <foo@example.com",
                "John Doe <foo@..example.com>",
                "John Doe <foo@example.com.>",
                "Jack Fruit <vegan@pulled@pork.com>",
                "stand alone_email@example.com",
            )
        for userid in test_data_list:
            with self.subTest(msg=f"UserID {repr(userid)}"):
                self.assertRaises(
                        ValueError,
                        mailbox_from_userid,
                        userid)


if __name__ == "__main__":
    unittest.main()
