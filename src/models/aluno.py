from __future__ import annotations

from datetime import date 

class Aluno: 
    def __init__(self, id: int, nome: str, nif: str, dataNasc: date,
                 telefone: str = "", email: str = "", morada: str = "",
                 consentimentoRGPD: bool = False, ativo: bool = True):
        self._id = id
        self._nome = nome
        self._nif = nif
        self._dataNasc = dataNasc
        self._telefone = telefone
        self._email = email
        self._morada = morada
        self._consentimentoRGPD = consentimentoRGPD
        self._ativo = ativo
        self._id_encarregado: EncarregadoEducacao | None = None
        self._matriculas: list[Matricula] = [] 

    def __str__(self): 
        return f"Aluno({self.id}: {self.nome} [NIF {self.nif}])" 

    @property 
    def idade_anos(self): 
        delta = date.today() - self.data_nasc 
        return delta.days // 365 

  

    @property 
    def e_menor(self): 
        return self.idade_anos < 18 

    def getHistorico(self) -> list[Matricula]:
        return list(self._matriculas)

    def arquivar(self) -> None:
        self._ativo = False
