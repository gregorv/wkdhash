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
from wkdhash import userid_to_wkd_hash


class TestUserIdToWkd(unittest.TestCase):
    def test_convert(self: Self) -> None:
        # Determined hashes with GPG from test.asc
        uid_hu_list = [
            ("mail@example.com", "dizb37aqa5h4skgu7jf1xjr4q71w4paq"),
            ("这是一个测试@example.com", "s7jptwpu5w579nbbz3f1xw8f6pwkikc9"),
            ("very_good_test@example.com", "x1m4a1ne1o656bzdnk31zqotsi8gcasb"),
            ("märklin_müller_öhler@example.com", "tfx9i999foj8iyfsxkcr5qe6rq55zapy"),  # noqa: E501
            # Mixed-case non-ASCII characters are treated specially!
            ("cÄse_SäNsItViTy@example.com", "hkeqc1bix6ftp4wyuhjuhrtajuijg6mb"),  # noqa: E501
        ]
        for uid, hu in uid_hu_list:
            with self.subTest(msg=f"UID {uid}"):
                self.assertEqual(
                    userid_to_wkd_hash(uid),
                    hu)


if __name__ == "__main__":
    unittest.main()
