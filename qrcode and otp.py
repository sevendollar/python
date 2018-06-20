import pyotp
import qrcode
from flask import Flask, send_file

app = Flask(__name__)
s = pyotp.random_base32()
totp = pyotp.TOTP(s)


@app.route('/api/otp/')
def otp_():
    img = qrcode.make(pyotp.TOTP(s).provisioning_uri('jef@google.com', issuer_name='Secure App'))
    img.save('qrcode.png')
    return send_file('qrcode.png', mimetype='image/png'), 200


@app.route('/api/otp/<string:num>/')
def otp_input(num):
    if totp.verify(num):
        return 'yes', 200
    return 'wrong', 202


if __name__ == '__main__':
    app.run(debug=True)
