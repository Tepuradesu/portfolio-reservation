import base64
import qrcode
from io import BytesIO
import onetimepass


def get_secret(user):
    #base32形式にエンコードした文字列をASCIIに直してリターンする。
    return base64.b32encode(
        (user.email + str(user.date_of_birth)).encode()
    ).decode()


def get_auth_url(email, secret, issuer='ProjectName'):
    """
    下に書いてあるURLフォーマットで設定する必要がある。
    最初の「isr」「uid」は、Google認証システムのアプリ上にも表示されるから、プロジェクト名とメールアドレスを突っ込むのが無難だと思う。
    """
    url_template = 'otpauth://totp/{isr}:{uid}?secret={secret}&issuer={isr}'
    return url_template.format(
        uid=email,
        secret=secret,
        isr=issuer)
#
def get_image_b64(url):
    qr = qrcode.make(url)
    img = BytesIO()
    qr.save(img)
    return base64.b64encode(img.getvalue()).decode()


def get_token(user):
    return str(onetimepass.get_totp(get_secret(user)))