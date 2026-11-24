# src/rbac.py
# RBAC (controlo de acesso por perfil) — Lab 5
# Baseado no código sugerido pelo professor

from functools import wraps

import jwt

from services.auth_service import SECRET_KEY, EMISSOR

# Mapa de permissões do LinguaViva
# direcao    -> tudo (alunos, matrículas, presenças, notas, certificados, relatórios)
# secretaria -> alunos (registar/arquivar), matrículas, presenças
# professor  -> presenças (das suas turmas), notas (das suas turmas)


def require_perfil(*perfis_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(token, *args, **kwargs):
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], issuer=EMISSOR)
            except jwt.ExpiredSignatureError:
                raise PermissionError("Sessão expirada. Faça login novamente.")
            except jwt.InvalidTokenError:
                raise PermissionError("Token inválido.")

            if payload["perfil"] not in perfis_permitidos:
                raise PermissionError("Sem permissão. Esta operação requer: " + ", ".join(perfis_permitidos))

            return func(token, *args, **kwargs)
        return wrapper
    return decorator


# Exemplos de uso:
# @require_perfil("direcao")
# def emitir_certificado(token, aluno_id): ...
#
# @require_perfil("direcao", "secretaria")
# def registar_aluno(token, dados_aluno): ...
#
# @require_perfil("direcao", "professor")
# def registar_nota(token, aluno_id, nota): ...
