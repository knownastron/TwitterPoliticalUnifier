# Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

from Config import cognito_config

region = cognito_config.REGION
userpool_id = cognito_config.USER_POOL_ID
app_client_id = cognito_config.APP_CLIENT_ID
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
with urllib.request.urlopen(keys_url) as f:
  response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']

def lambda_handler(event, context):
    token = event['token']
    # print(token)
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    # now we can use the claims
    print('Claim results:', claims)
    return claims

# the following is useful to make this script executable in both
# AWS Lambda and any other local environments
if __name__ == '__main__':
    # for testing locally you can enter the JWT ID Token here
    event = {'token': 'eyJraWQiOiJtdm90Y2JlWks3TWdyNFJqWEJoT2RWMDhRakNnYnZWbFdTczIzanRZeW5vPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmMTVlM2UyYS1kOGNhLTQ5YzMtOTg5Yi1jMzc1OGZlZjg1MWIiLCJhdWQiOiJlMHNwY3NqZDI2aWY0bW1lMTM0aXI1anFxIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV2ZW50X2lkIjoiMjVmYmU0NzEtNDE3Yy00MDBkLWExZGEtZmMwYjdhNmQxOGU0IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE1NzI5Mzc4NTYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yX3NObVBOOTVETCIsImNvZ25pdG86dXNlcm5hbWUiOiJmMTVlM2UyYS1kOGNhLTQ5YzMtOTg5Yi1jMzc1OGZlZjg1MWIiLCJleHAiOjE1NzI5NDE0NTYsImlhdCI6MTU3MjkzNzg1NiwiZW1haWwiOiJrbm93bmFzdHJvbkBnbWFpbC5jb20ifQ.PtAGF_fCltR7smt8StvbSFt5IiN6iZ-wcoV-d8r4wpdpHFsklHansH3vN0KkGFZh0juVBFG4NoJEqtRdpnBHwnjcWH6l1BRtSenzT6E1Q2I6nk17R9CDahuOQfkl9Kj2In8-T6lZrnho5mWsVh3tlCzB8kpUV9HSPXXtzNNrdi3TNtvqz8TNFmypBoSlY4_zMctmRdLURlv12IbS5_xO1NIY8RdlBQvVKVqn7_o5WxgbBOZWnHDaYYtS6Yk4UCeTWIKg8m-6OFyuJMgblUBEO45fvwv2DivH-0nnJYFh_fDSY0P0Q6Jc3JF4ALBeChmMJ3_BkWPYxO7PVCFwHcrArw'}
    lambda_handler(event, None)
