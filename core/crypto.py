from base64 import b64decode,b64encode

def decode_token(token):
    token_2=b64decode(b64decode(token))
    user,passwd=token_2.split("*")
    user=b64decode(user[::-1]).split("-")
    user=user[1]+"-"+user[0]
    passwd=b64decode(passwd)[::-1]
    return [user,passwd]

def enconde_token(user,password):
    btoa=b64encode
    password=b64encode(password[::-1])
    user=user.split("-")[::-1]
    user="-".join(user)
    user=b64encode(user)[::-1]
    token = btoa(btoa (user+"*"+password))
    return token

