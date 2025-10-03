
class No:

    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:

    def __init__(self):
        self.raiz = None

    def inserir(self, chave, valor):
        if self.raiz is None:
            self.raiz = No(chave, valor)
        else:
            self._inserir_recursivo(self.raiz,chave,valor)

    def _inserir_recursivo(self, no_atual, chave, valor):
        if chave < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(chave, valor)
            else:
                self._inserir_recursivo(no_atual.esquerda, chave, valor)
        elif chave > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = No(chave, valor)
            else:
                self._inserir_recursivo(no_atual.direita, chave, valor)
        else:
            no_atual.valor = valor

    def buscar(self, chave):
        return self._buscar_recursivo(self.raiz, chave)

    def _buscar_recursivo(self, no_atual, chave):
        if no_atual is None or no_atual.chave == chave:
            return no_atual.valor if no_atual else None

        if chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, chave)
        else:
            return self._buscar_recursivo(no_atual.direita, chave)

    def remover(self,chave):
        self.raiz = self._remover_recursivo(self.raiz, chave)

    def _remover_recursivo(self, no_atual, chave):
        if no_atual is None:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._remover_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._remover_recursivo(no_atual.direita, chave)
        else:
            if no_atual.esquerda is None:
                return no_atual.direita
            elif no_atual.direita is None:
                return no_atual.esquerda

            no_sucessor = self._encontrar_minimo(no_atual.direita)
            no_atual.chave = no_sucessor.chave
            no_atual.valor = no_sucessor.valor
            no_atual.direita = self._remover_recursivo(no_atual.direita, no_sucessor.chave)
        return no_atual

    def _encontrar_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def em_ordem(self):
        resultado = []
        self._em_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _em_ordem_recursivo(self, no_atual, resultado):
        if no_atual:
            self._em_ordem_recursivo(no_atual.esquerda, resultado)
            resultado.append((no_atual.chave, no_atual.valor))
            self._em_ordem_recursivo(no_atual.direita, resultado)

