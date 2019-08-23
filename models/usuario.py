from sql_alchemy import banco
from flask import request, url_for
from requests import post


MAILGUN_DOMAIN = "sandboxabd8b1ae931345198a1443bbb3c9cc88.mailgun.org"
MAILGUN_API_KEY = "9b80b2f65ed6b29a786844b68fa540a1-2ae2c6f3-51e6ddd8"
FROM_TITLE = "NO-REPLY"
FROM_EMAIL = "noreply@restapi.com"


class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(100), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def send_confirmation_email(self):
        link = request.url_root[:-1] + \
            url_for('userconfirm', user_id=self.user_id)
        return post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={
                        "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                        "to": self.email,
                        "subject": "Confirmação de cadastro",
                        "text": f"Confirme seu cadastro clicando no link a seguir: {link}",
                        "html": f"<html><p>\
                                    Confirme seu cadastro clicando no link a seguir: <a href={link}>CONFIRMAR EMAIL</a> \
                                </p></html>",
                    }
                    )

    def toJson(self):
        return {
            "user_id": self.user_id,
            "login": self.login,
            "email": self.email,
            "ativado": self.ativado,
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        login = cls.query.filter_by(login=login).first()
        if login:
            return login
        return None

    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email=email).first()
        if email:
            return email
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
