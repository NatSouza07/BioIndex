class NoArvore:
    def __init__(self, chave, num_linha):
        self.chave = chave
        self.num_linha = num_linha
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, num_linha):
            if self.raiz is None:
                self.raiz = NoArvore(chave, num_linha)
            else:
                self._inserir_recursivo(self.raiz, chave, num_linha)

    def buscar(self, chave):
            return self._buscar_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave, num_linha):
        if chave < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = NoArvore(chave, num_linha)
            else:
                self._inserir_recursivo(no_atual.esquerda, chave, num_linha)
        elif chave > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = NoArvore(chave, num_linha)
            else:
                self._inserir_recursivo(no_atual.direita, chave, num_linha)
        elif chave == no_atual.chave:
            raise ValueError(f"A chave '{chave}' já existe e a inserção duplicada não é permitida.")

    def _buscar_recursivo(self, no_atual, chave):
        if no_atual is None:
            return None

        if chave == no_atual.chave:
            return no_atual.num_linha

        elif chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, chave)
        else:
            return self._buscar_recursivo(no_atual.direita, chave)

    def remover(self, chave):
        if self.raiz is None:
            return False
        self.raiz = self._remover_recursivo(self.raiz, chave)
        return True

    def _remover_recursivo(self, no_atual, chave):
        if no_atual is None:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._remover_recursivo(no_atual.esquerda, chave)
            return no_atual
        elif chave > no_atual.chave:
            no_atual.direita = self._remover_recursivo(no_atual.direita, chave)
            return no_atual

        else:
            if no_atual.esquerda is None:
                return no_atual.direita
            elif no_atual.direita is None:
                return no_atual.esquerda

            sucessor = self._encontrar_minimo(no_atual.direita)

            no_atual.chave = sucessor.chave
            no_atual.num_linha = sucessor.num_linha

            no_atual.direita = self._remover_recursivo(no_atual.direita, sucessor.chave)

            return no_atual

    @staticmethod
    def _encontrar_minimo(no_atual):
        while no_atual.esquerda is not None:
            no_atual = no_atual.esquerda
        return no_atual