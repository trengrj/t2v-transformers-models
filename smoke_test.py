import unittest
import requests
import time


class SmokeTest(unittest.TestCase):
    def _waitForStartup(self):
        url = 'http://localhost:8000/.well-known/ready'

        for i in range(0, 100):
            try:
                res = requests.get(url)
                if res.status_code == 204:
                    return
                else:
                    raise Exception(
                            "status code is {}".format(res.status_code))
            except Exception as e:
                print("Attempt {}: {}".format(i, e))
                time.sleep(1)

        raise Exception("did not start up")

    def testVectorizing(self):
        self._waitForStartup()
        url = 'http://localhost:8000/vectors/'
        req_body = {'text': 'The London Eye is a ferris wheel at the River Thames.'}

        res = requests.post(url, json=req_body)
        resBody = res.json()

        self.assertEqual(200, res.status_code)

        # below tests that what we deem a reasonable vector is returned. We are
        # aware of 384 and 768 dim vectors, which should both fall in that
        # range
        self.assertTrue(len(resBody['vector']) > 100)


if __name__ == "__main__":
    unittest.main()
