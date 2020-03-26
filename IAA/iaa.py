from werkzeug.wrappers import Request, Response
from indy_agent import Indy
from indy import pool, wallet
import json
import sys
import jwt
import asyncio

conf = {}
wallet_handle = ""
pool_handle = ""

class IAA:
    @staticmethod
    def verify_token(type, token=None, as_public_key=None, target=None, tokens_expire = True, proof=None):
        if (type ==  "Bearer"):
            #decoded_token = jwt.decode(token, as_public_key, algorithms='RS256', audience=target, verify_expiration = False)
            try:
                decoded_token = jwt.decode(token, as_public_key, algorithms='RS256', audience=target, options={"verify_exp":tokens_expire})
                return 200, {'code':200,'message':'Success'}
            except:
                return 403, {'code':403,'message':'Token validation failed'}
        return 403, {'code':403, 'message':'Invalide token type'}
    

class IAAHandler():
    def __init__(self):
        with open('conf/iaa.conf') as f:
            self.conf = json.load(f)
        loop = asyncio.get_event_loop()
        self.wallet_handle = loop.run_until_complete(wallet.open_wallet(json.dumps(self.conf['wallet_config']), json.dumps(self.conf['wallet_credentials'])))
        self.pool_handle = None
    
    def wsgi_app(self, environ, start_response):
        req  = Request(environ)
        code = 403
        output = {'code':403, 'message':'Invalide or missing input parameters'}
        form = req.form
        type  = form.get("token-type")
        token = form.get("token")
        challenge = form.get("challenge")
        proof = form.get("proof")
        if (type == "Bearer"):
            with open(self.conf['as_public_key'], mode='rb') as file: 
                as_public_key = file.read()
            code, output = IAA.verify_token(type, token, as_public_key, self.conf['target'],self.conf['tokens_expire'])
        if (type == "DID"):
            loop = asyncio.get_event_loop()
            code, output = loop.run_until_complete(
                Indy.verify_did(token, challenge, proof, self.wallet_handle, self.pool_handle, True))
        response = Response(json.dumps(output).encode(), status=code, mimetype='application/json')
        return response(environ, start_response)
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app():
    app = IAAHandler()
    return app

def main(): 
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 9000, app)
    #loop.run_until_complete(wallet.close_wallet(wallet_handle))

if __name__ == '__main__':
    main()
